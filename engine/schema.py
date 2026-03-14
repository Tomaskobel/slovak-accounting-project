"""
Execution Rule Schema — the contract between the regulatory model and the engine.

Derived from 10 common s.r.o. transaction types extracted from Slovak law.
Every field maps to a real regulatory concept from Zákon 222/2004 Z.z.
or Opatrenie MF SR 23054/2002-92.

This module defines the data structures. The engine interprets them.
"""

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Enums — exact legal terminology
# ---------------------------------------------------------------------------

class SmerTransakcie(str, Enum):
    """Smer transakcie — purchase vs sale."""
    NAKUP = "nakup"          # Nákup (purchase/receipt)
    PREDAJ = "predaj"        # Predaj (sale/supply)
    OPRAVA = "oprava"        # Oprava (correction — credit/charge note)
    PREDDAVOK = "preddavok"  # Preddavok (advance payment)


class TypPlnenia(str, Enum):
    """Typ plnenia — what is being supplied (§ 8-9 Z. 222/2004)."""
    TOVAR = "tovar"              # Tovar (goods)
    SLUZBA = "sluzba"            # Služba (service)
    MATERIAL = "material"        # Materiál (raw material)
    DLHODOBY_MAJETOK = "dhm"     # Dlhodobý hmotný majetok (fixed asset)
    ENERGIA = "energia"          # Energia (energy/utilities)


class KrajinaDodavatela(str, Enum):
    """Krajina dodávateľa/odberateľa."""
    SK = "SK"                    # Tuzemsko (domestic)
    EU = "EU"                    # Iný členský štát EÚ
    TRETIA_KRAJINA = "non_EU"    # Tretia krajina (non-EU)


class DphTreatment(str, Enum):
    """Typ DPH zaobchádzania — how VAT is handled (§ 49-69 Z. 222/2004)."""
    VSTUPNA_DAN = "vstupna_dan"                        # Standard input deduction
    VYSTUPNA_DAN = "vystupna_dan"                      # Standard output liability
    SAMOZDANENIE = "samozdanenie"                      # Self-assessment (§ 69 ods. 3)
    PRENOS_DANOVEJ_POVINNOSTI = "prenos"               # Domestic reverse charge (§ 69 ods. 12)
    OSLOBODENIE_S_ODPOCTOM = "oslobodene_s_odpoctom"   # Exempt with deduction (§ 43, § 47)
    OSLOBODENIE_BEZ_ODPOCTU = "oslobodene_bez"         # Exempt without deduction (§ 28-41)
    OPRAVA_VSTUPNEJ = "oprava_vstupnej"                # Credit note — input reduction (§ 53)
    OPRAVA_VYSTUPNEJ = "oprava_vystupnej"              # Credit note — output reduction (§ 25)
    PREDDAVKOVA = "preddavkova"                        # Advance payment DPH (§ 19 ods. 2)
    BEZ_DPH = "bez_dph"                                # No DPH (non-VAT payer transaction)


class KvDphSekcia(str, Enum):
    """Sekcia kontrolného výkazu DPH (Metodický pokyn FS SR)."""
    A1 = "A1"    # Vydané faktúry — štandardné dodanie
    A2 = "A2"    # Vydané faktúry — prenos daňovej povinnosti
    B1 = "B1"    # Prijaté faktúry — odberateľ platí daň (§ 69)
    B2 = "B2"    # Prijaté faktúry — štandardný odpočet
    B3 = "B3"    # Iné vstupné doklady (zjednodušené faktúry)
    C1 = "C1"    # Opravné faktúry vydané
    C2 = "C2"    # Opravné faktúry prijaté
    D1 = "D1"    # Pokladničné doklady z e-kasy
    D2 = "D2"    # Ostatné dodania bez faktúry
    ZIADNA = "ziadna"  # Nevykazuje sa v KV DPH


class StranaUctu(str, Enum):
    """Strana účtu — debit or credit."""
    MA_DAT = "MD"   # Má dať (debit)
    DAL = "D"       # Dal (credit)


class VzorecSumy(str, Enum):
    """Vzorec pre výpočet sumy na riadku účtovného zápisu.

    References formulas from engine/pojmy.py.
    """
    ZAKLAD_DANE = "zaklad_dane"          # Tax base (from input or calculated)
    DAN = "dan"                          # VAT amount = základ × sadzba / 100
    CELKOVA_VYSKA = "celkova_vyska"      # Total = základ + daň
    NADOBUDACIA_CENA = "nadobudacia_cena"  # Acquisition cost (for COGS/assets)
    PREDDAVKOVA_SUMA = "preddavkova_suma"  # Advance payment amount
    ZAKLAD_Z_UHRADY = "zaklad_z_uhrady"   # Reverse-calculated base from gross


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RiadokZapisu:
    """Riadok účtovného zápisu — one line of a journal entry.

    Each posting rule produces multiple lines. Each line specifies:
    - which account (číslo účtu)
    - which side (MD/D)
    - how to compute the amount (vzorec referencing pojmy.py)
    """
    ucet: str                    # Account code (e.g., "112", "343", "321")
    strana: StranaUctu           # MD (debit) or D (credit)
    vzorec_sumy: VzorecSumy     # Formula reference for amount calculation
    popis: str                   # Description (Slovak)


@dataclass(frozen=True)
class Podmienky:
    """Podmienky pre zhodu pravidla — conditions for rule matching.

    All conditions must be satisfied (AND logic).
    None = any value accepted (wildcard).
    """
    smer: SmerTransakcie
    typ_plnenia: Optional[TypPlnenia] = None
    krajina_dodavatela: Optional[KrajinaDodavatela] = None
    platitel_dph_kupujuci: Optional[bool] = None
    platitel_dph_dodavatel: Optional[bool] = None
    forma_uhrady: Optional[str] = None     # "faktura", "hotovost", "preddavok", "banka"
    metoda_zasob: Optional[str] = None     # "A" (perpetual) or "B" (periodic)
    tuzemsky_prenos: Optional[bool] = None  # § 69 ods. 12 — domestic reverse charge


@dataclass(frozen=True)
class Pravidlo:
    """Pravidlo účtovania — declarative booking rule.

    The central artifact. Defines what happens when conditions match:
    - Which posting lines to generate
    - Which DPH treatment applies
    - Which KV DPH section to report in
    - What inputs are required
    - What legal source authorizes this rule
    """
    id: str                                  # Unique rule ID
    nazov: str                               # Rule name (Slovak)
    name_en: str                             # Rule name (English, documentation only)
    podmienky: Podmienky                     # Matching conditions
    riadky: tuple[RiadokZapisu, ...]         # Posting lines (ordered)
    dph_treatment: DphTreatment              # How DPH is handled
    sadzba_dane_id: Optional[str] = None     # Reference to sadzba in pojmy.json (e.g., "sadzba_dane_23")
    kv_dph_sekcia: KvDphSekcia = KvDphSekcia.ZIADNA  # KV DPH section
    povinne_vstupy: tuple[str, ...] = ()     # Required input field names
    pravny_zdroj: str = ""                   # Legal source (§ reference)
    priorita: int = 100                      # Priority (higher = more specific, wins conflicts)
    platne_od: str = "2025-01-01"            # Valid from (ISO date)
    platne_do: Optional[str] = None          # Valid to (None = still active)
    poznamky: Optional[str] = None           # Notes
    dovera: str = "high"                     # Confidence: high (from example), medium (from law), low (inferred)

    # --- Multi-step support ---
    krok: int = 1                            # Step number (1 = default, 2/3 = subsequent steps)
    celkovo_krokov: int = 1                  # Total steps in sequence


# ---------------------------------------------------------------------------
# Rule conflict resolution
# ---------------------------------------------------------------------------

def priorita_pravidla(pravidlo: Pravidlo) -> tuple[int, int]:
    """Priorita pre riešenie konfliktov.

    Higher tuple = wins.
    Resolution order:
    1. Explicit priority (higher wins)
    2. Number of non-None conditions (more specific wins)
    """
    podmienky = pravidlo.podmienky
    specificnost = sum(1 for v in [
        podmienky.typ_plnenia,
        podmienky.krajina_dodavatela,
        podmienky.platitel_dph_kupujuci,
        podmienky.platitel_dph_dodavatel,
        podmienky.forma_uhrady,
        podmienky.metoda_zasob,
        podmienky.tuzemsky_prenos,
    ] if v is not None)
    return (pravidlo.priorita, specificnost)


def vyriesit_konflikty(pravidla: list[Pravidlo]) -> Pravidlo:
    """Vyriešiť konflikty — vráti pravidlo s najvyššou prioritou.

    Raises ValueError if two rules have identical priority and specificity.
    """
    if not pravidla:
        raise ValueError("Žiadne pravidlá sa nezhodujú s podmienkami")
    if len(pravidla) == 1:
        return pravidla[0]

    zoradene = sorted(pravidla, key=priorita_pravidla, reverse=True)

    # Check for tie
    if len(zoradene) >= 2:
        p1 = priorita_pravidla(zoradene[0])
        p2 = priorita_pravidla(zoradene[1])
        if p1 == p2:
            raise ValueError(
                f"Konflikt pravidiel s rovnakou prioritou: "
                f"{zoradene[0].id} vs {zoradene[1].id} "
                f"(priorita={p1})"
            )

    return zoradene[0]
