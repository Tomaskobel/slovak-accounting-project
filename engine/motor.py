"""
Motor účtovania — the deterministic execution engine.

Pipeline: transakcia → zhoda pravidla → výpočet súm → generovanie zápisu → validácia

No LLM. No AI. Pure deterministic execution.
Same input + same rules = same output.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from engine.pojmy import dan, celkova_vyska, zaklad_dane_z_uhrady, nacitaj_sadzby
from engine.schema import (
    Pravidlo, Podmienky, RiadokZapisu,
    SmerTransakcie, TypPlnenia, KrajinaDodavatela,
    DphTreatment, KvDphSekcia, StranaUctu, VzorecSumy,
    vyriesit_konflikty,
)
from engine.pravidla import VSETKY_PRAVIDLA


# ---------------------------------------------------------------------------
# Input: Transakcia
# ---------------------------------------------------------------------------

@dataclass
class Transakcia:
    """Vstupná transakcia — what happened in the real world."""
    smer: SmerTransakcie
    typ_plnenia: Optional[TypPlnenia] = None
    krajina_dodavatela: Optional[KrajinaDodavatela] = None
    platitel_dph_kupujuci: Optional[bool] = None
    platitel_dph_dodavatel: Optional[bool] = None
    forma_uhrady: Optional[str] = None
    metoda_zasob: Optional[str] = None
    tuzemsky_prenos: Optional[bool] = None

    # Amounts
    zaklad_dane: Optional[Decimal] = None
    celkova_vyska_uhrady: Optional[Decimal] = None
    celkova_suma: Optional[Decimal] = None  # Direct total (for non-DPH transactions)
    sadzba_dane: Optional[Decimal] = None
    nadobudacia_cena: Optional[Decimal] = None
    preddavkova_suma: Optional[Decimal] = None

    # Metadata
    datum: Optional[str] = None
    popis: Optional[str] = None


# ---------------------------------------------------------------------------
# Output: Účtovný zápis
# ---------------------------------------------------------------------------

@dataclass
class RiadokUctovnehoZapisu:
    """One line of the generated journal entry."""
    ucet: str
    strana: StranaUctu
    suma: Decimal
    popis: str


@dataclass
class UctovnyZapis:
    """Complete journal entry — the engine's output."""
    pravidlo_id: str
    pravidlo_nazov: str
    riadky: list[RiadokUctovnehoZapisu]
    dph_treatment: DphTreatment
    kv_dph_sekcia: KvDphSekcia
    pravny_zdroj: str
    suma_ma_dat: Decimal
    suma_dal: Decimal
    je_vyvazeny: bool

    # DPH detail
    zaklad_dane: Optional[Decimal] = None
    suma_dph: Optional[Decimal] = None
    sadzba_dane: Optional[Decimal] = None


# ---------------------------------------------------------------------------
# Step 1: Match — find rules that match the transaction
# ---------------------------------------------------------------------------

def _podmienka_zodpoveda(hodnota_pravidla, hodnota_transakcie) -> bool:
    """Check if a single condition matches. None in rule = wildcard (matches anything)."""
    if hodnota_pravidla is None:
        return True
    return hodnota_pravidla == hodnota_transakcie


def najdi_zhody(transakcia: Transakcia, pravidla: Optional[list[Pravidlo]] = None) -> list[Pravidlo]:
    """Nájdi všetky pravidlá, ktoré sa zhodujú s transakciou."""
    if pravidla is None:
        pravidla = VSETKY_PRAVIDLA

    zhody = []
    for p in pravidla:
        pod = p.podmienky
        if not _podmienka_zodpoveda(pod.smer, transakcia.smer):
            continue
        if not _podmienka_zodpoveda(pod.typ_plnenia, transakcia.typ_plnenia):
            continue
        if not _podmienka_zodpoveda(pod.krajina_dodavatela, transakcia.krajina_dodavatela):
            continue
        if not _podmienka_zodpoveda(pod.platitel_dph_kupujuci, transakcia.platitel_dph_kupujuci):
            continue
        if not _podmienka_zodpoveda(pod.platitel_dph_dodavatel, transakcia.platitel_dph_dodavatel):
            continue
        if not _podmienka_zodpoveda(pod.forma_uhrady, transakcia.forma_uhrady):
            continue
        if not _podmienka_zodpoveda(pod.metoda_zasob, transakcia.metoda_zasob):
            continue
        if not _podmienka_zodpoveda(pod.tuzemsky_prenos, transakcia.tuzemsky_prenos):
            continue
        zhody.append(p)

    return zhody


# ---------------------------------------------------------------------------
# Step 2: Resolve — pick the best rule if multiple match
# ---------------------------------------------------------------------------

def vyber_pravidlo(transakcia: Transakcia, pravidla: Optional[list[Pravidlo]] = None) -> Pravidlo:
    """Nájdi zhody a vyrieš konflikty. Vráti jedno pravidlo."""
    zhody = najdi_zhody(transakcia, pravidla)
    return vyriesit_konflikty(zhody)


# ---------------------------------------------------------------------------
# Step 3: Compute — calculate amounts per formula references
# ---------------------------------------------------------------------------

def _vypocitaj_sumu(
    vzorec: VzorecSumy,
    transakcia: Transakcia,
    sadzba: Optional[Decimal],
) -> Decimal:
    """Compute amount for a posting line based on formula reference."""

    if vzorec == VzorecSumy.ZAKLAD_DANE:
        if transakcia.zaklad_dane is not None:
            return transakcia.zaklad_dane
        if transakcia.celkova_vyska_uhrady is not None and sadzba is not None:
            return zaklad_dane_z_uhrady(transakcia.celkova_vyska_uhrady, sadzba)
        raise ValueError("Chýba základ dane alebo celková výška úhrady")

    if vzorec == VzorecSumy.DAN:
        zd = _vypocitaj_sumu(VzorecSumy.ZAKLAD_DANE, transakcia, sadzba)
        if sadzba is None:
            raise ValueError("Chýba sadzba dane pre výpočet DPH")
        return dan(zd, sadzba)

    if vzorec == VzorecSumy.CELKOVA_VYSKA:
        # Direct total for non-DPH transactions (bankové poplatky, cestovné, etc.)
        if transakcia.celkova_suma is not None and transakcia.zaklad_dane is None:
            return transakcia.celkova_suma
        zd = _vypocitaj_sumu(VzorecSumy.ZAKLAD_DANE, transakcia, sadzba)
        d = _vypocitaj_sumu(VzorecSumy.DAN, transakcia, sadzba)
        return celkova_vyska(zd, d)

    if vzorec == VzorecSumy.NADOBUDACIA_CENA:
        if transakcia.nadobudacia_cena is not None:
            return transakcia.nadobudacia_cena
        raise ValueError("Chýba nadobúdacia cena (COGS)")

    if vzorec == VzorecSumy.PREDDAVKOVA_SUMA:
        if transakcia.preddavkova_suma is not None:
            return transakcia.preddavkova_suma
        raise ValueError("Chýba preddavková suma")

    if vzorec == VzorecSumy.ZAKLAD_Z_UHRADY:
        if transakcia.celkova_vyska_uhrady is not None and sadzba is not None:
            return zaklad_dane_z_uhrady(transakcia.celkova_vyska_uhrady, sadzba)
        raise ValueError("Chýba celková výška úhrady a sadzba")

    raise ValueError(f"Neznámy vzorec: {vzorec}")


def _zisti_sadzbu(pravidlo: Pravidlo, transakcia: Transakcia) -> Optional[Decimal]:
    """Determine tax rate from rule reference or transaction input."""
    if transakcia.sadzba_dane is not None:
        return transakcia.sadzba_dane
    if pravidlo.sadzba_dane_id:
        sadzby = nacitaj_sadzby()
        return sadzby.get(pravidlo.sadzba_dane_id)
    return None


# ---------------------------------------------------------------------------
# Step 4: Generate — produce journal entry lines
# ---------------------------------------------------------------------------

def generuj_zapis(pravidlo: Pravidlo, transakcia: Transakcia) -> UctovnyZapis:
    """Generuj účtovný zápis z pravidla a transakcie."""

    sadzba = _zisti_sadzbu(pravidlo, transakcia)

    riadky_zapisu = []
    for riadok in pravidlo.riadky:
        suma = _vypocitaj_sumu(riadok.vzorec_sumy, transakcia, sadzba)
        riadky_zapisu.append(RiadokUctovnehoZapisu(
            ucet=riadok.ucet,
            strana=riadok.strana,
            suma=suma,
            popis=riadok.popis,
        ))

    # Compute totals
    suma_md = sum((r.suma for r in riadky_zapisu if r.strana == StranaUctu.MA_DAT), Decimal("0"))
    suma_d = sum((r.suma for r in riadky_zapisu if r.strana == StranaUctu.DAL), Decimal("0"))

    # DPH detail
    zaklad = None
    suma_dph = None
    try:
        zaklad = _vypocitaj_sumu(VzorecSumy.ZAKLAD_DANE, transakcia, sadzba)
        if sadzba and sadzba > 0:
            suma_dph = dan(zaklad, sadzba)
    except ValueError:
        pass

    return UctovnyZapis(
        pravidlo_id=pravidlo.id,
        pravidlo_nazov=pravidlo.nazov,
        riadky=riadky_zapisu,
        dph_treatment=pravidlo.dph_treatment,
        kv_dph_sekcia=pravidlo.kv_dph_sekcia,
        pravny_zdroj=pravidlo.pravny_zdroj,
        suma_ma_dat=suma_md,
        suma_dal=suma_d,
        je_vyvazeny=suma_md == suma_d,
        zaklad_dane=zaklad,
        suma_dph=suma_dph,
        sadzba_dane=sadzba,
    )


# ---------------------------------------------------------------------------
# Step 5: Validate — check invariants
# ---------------------------------------------------------------------------

def validuj_zapis(zapis: UctovnyZapis) -> list[str]:
    """Validácia účtovného zápisu — vráti zoznam chýb (prázdny = OK)."""
    chyby = []

    # Invariant 1: podvojné účtovníctvo
    if not zapis.je_vyvazeny:
        chyby.append(
            f"Nevyvážený zápis: MD {zapis.suma_ma_dat} != D {zapis.suma_dal}"
        )

    # Invariant 2: minimálne 2 riadky
    if len(zapis.riadky) < 2:
        chyby.append(
            f"Zápis musí mať minimálne 2 riadky, má {len(zapis.riadky)}"
        )

    # Invariant 3: všetky sumy > 0
    for r in zapis.riadky:
        if r.suma < 0:
            chyby.append(f"Záporná suma na účte {r.ucet}: {r.suma}")
        if r.suma == 0:
            chyby.append(f"Nulová suma na účte {r.ucet}")

    return chyby


# ---------------------------------------------------------------------------
# Full pipeline: transakcia → účtovný zápis
# ---------------------------------------------------------------------------

def zauctuj(transakcia: Transakcia, pravidla: Optional[list[Pravidlo]] = None) -> UctovnyZapis:
    """Kompletný pipeline: zhoda → výber → výpočet → generovanie → validácia.

    Raises ValueError if no rule matches or validation fails.
    """
    pravidlo = vyber_pravidlo(transakcia, pravidla)
    zapis = generuj_zapis(pravidlo, transakcia)
    chyby = validuj_zapis(zapis)
    if chyby:
        raise ValueError(
            f"Validácia zlyhala pre pravidlo '{pravidlo.id}': " +
            "; ".join(chyby)
        )
    return zapis
