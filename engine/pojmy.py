"""
Pojmy a vzorce slovenského účtovníctva — Central Validation Truth.

Všetky výpočty používajú Decimal pre presnosť (NUMERIC(19,2)).
Zaokrúhľovanie: ROUND_HALF_UP na 2 desatinné miesta (§ 26 Z. 222/2004 Z.z.).
Terminológia: presne podľa zákona 222/2004 Z.z. a 431/2002 Z.z.
"""

import json
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING
from pathlib import Path
from typing import Union

_TWO_PLACES = Decimal("0.01")
_POJMY_PATH = Path(__file__).parent / "pojmy.json"

NumType = Union[Decimal, int, float, str]


def _to_decimal(value: NumType) -> Decimal:
    """Konvertuje vstup na Decimal. Nikdy nepoužíva float konverziu priamo."""
    if isinstance(value, Decimal):
        return value
    if isinstance(value, float):
        return Decimal(str(value))
    return Decimal(value)


def _zaokruhli(hodnota: Decimal) -> Decimal:
    """Zaokrúhlenie na 2 des. miesta, ROUND_HALF_UP (§ 26 Z. 222/2004 Z.z.)."""
    return hodnota.quantize(_TWO_PLACES, rounding=ROUND_HALF_UP)


# ---------------------------------------------------------------------------
# 1. Výpočty DPH
# ---------------------------------------------------------------------------

def dan(zaklad_dane: NumType, sadzba: NumType) -> Decimal:
    """§ 22-27 Z. 222/2004 Z.z. — Daň (daňová suma).

    daň = základ dane × sadzba / 100
    """
    zd = _to_decimal(zaklad_dane)
    s = _to_decimal(sadzba)
    vysledok = _zaokruhli(zd * s / 100)
    if vysledok < 0:
        raise ValueError(f"Daň musí byť >= 0, dostali sme {vysledok}")
    return vysledok


def celkova_vyska(zaklad_dane: NumType, dan_suma: NumType) -> Decimal:
    """§ 22 Z. 222/2004 Z.z. — Celková výška úhrady.

    celková výška = základ dane + daň
    """
    zd = _to_decimal(zaklad_dane)
    d = _to_decimal(dan_suma)
    return _zaokruhli(zd + d)


def zaklad_dane_z_uhrady(celkova: NumType, sadzba: NumType) -> Decimal:
    """§ 26 Z. 222/2004 Z.z. — Základ dane z celkovej výšky (spätný výpočet).

    základ dane = celková výška / (1 + sadzba / 100)
    """
    c = _to_decimal(celkova)
    s = _to_decimal(sadzba)
    if s <= 0:
        raise ValueError("Sadzba musí byť > 0 pre spätný výpočet")
    vysledok = _zaokruhli(c / (1 + s / 100))
    if vysledok <= 0:
        raise ValueError(f"Základ dane musí byť > 0, dostali sme {vysledok}")
    return vysledok


def dan_z_uhrady(celkova: NumType, zaklad: NumType) -> Decimal:
    """§ 26 Z. 222/2004 Z.z. — Daň z celkovej výšky.

    daň = celková výška - základ dane
    """
    c = _to_decimal(celkova)
    zd = _to_decimal(zaklad)
    vysledok = _zaokruhli(c - zd)
    if vysledok < 0:
        raise ValueError(f"Daň musí byť >= 0, dostali sme {vysledok}")
    return vysledok


def pomerny_odpocet(
    zdanitelne_plnenia: NumType,
    oslobodene_plnenia: NumType,
    vylucene: NumType = 0,
) -> Decimal:
    """§ 50 Z. 222/2004 Z.z. — Pomerný odpočet (koeficient).

    koeficient = zdaniteľné / (zdaniteľné + oslobodené - vylúčené)
    Zaokrúhľuje sa NAHOR na 2 desatinné miesta.
    """
    zp = _to_decimal(zdanitelne_plnenia)
    op = _to_decimal(oslobodene_plnenia)
    vy = _to_decimal(vylucene)
    menovatel = zp + op - vy
    if menovatel <= 0:
        raise ValueError("Menovateľ koeficientu musí byť > 0")
    koef = zp / menovatel
    # CEIL na 2 des. miesta (§ 50)
    vysledok = (koef * 100).to_integral_value(rounding=ROUND_CEILING) / 100
    if not (Decimal("0") <= vysledok <= Decimal("1")):
        raise ValueError(
            f"Koeficient musí byť medzi 0 a 1, dostali sme {vysledok}"
        )
    return vysledok


def odpocitatelna_dan(vstupna_dan: NumType, koeficient: NumType) -> Decimal:
    """§ 49-50 Z. 222/2004 Z.z. — Odpočítateľná daň.

    odpočítateľná daň = vstupná daň × koeficient
    """
    vd = _to_decimal(vstupna_dan)
    k = _to_decimal(koeficient)
    vysledok = _zaokruhli(vd * k)
    if vysledok > vd:
        raise ValueError(f"Odpočítateľná daň ({vysledok}) > vstupná daň ({vd})")
    return vysledok


def bez_prava_na_odpocet(vstupna_dan: NumType, koeficient: NumType) -> Decimal:
    """§ 49-50 Z. 222/2004 Z.z. — Daň bez práva na odpočet.

    bez práva = vstupná daň × (1 - koeficient)
    Pripočítava sa k obstarávacej cene majetku.
    """
    vd = _to_decimal(vstupna_dan)
    k = _to_decimal(koeficient)
    vysledok = _zaokruhli(vd * (1 - k))
    if vysledok > vd:
        raise ValueError(f"Daň bez práva ({vysledok}) > vstupná daň ({vd})")
    return vysledok


def zaklad_dane_pri_dovoze(colna_hodnota: NumType, clo: NumType) -> Decimal:
    """§ 24 Z. 222/2004 Z.z. — Základ dane pri dovoze.

    základ dane = colná hodnota + clo
    """
    ch = _to_decimal(colna_hodnota)
    c = _to_decimal(clo)
    vysledok = _zaokruhli(ch + c)
    if vysledok <= ch:
        raise ValueError(f"Základ dane pri dovoze ({vysledok}) musí byť > colná hodnota ({ch})")
    return vysledok


def osobitny_rezim_marza(
    predajna_cena: NumType,
    nadobudacia_cena: NumType,
    sadzba: NumType,
) -> Decimal:
    """§ 65-66 Z. 222/2004 Z.z. — Osobitný režim — zdanenie marže.

    daň = (predajná cena - nadobúdacia cena) × sadzba / 100
    """
    pc = _to_decimal(predajna_cena)
    nc = _to_decimal(nadobudacia_cena)
    s = _to_decimal(sadzba)
    marza = pc - nc
    if marza < 0:
        raise ValueError(f"Marža musí byť >= 0 (predaj {pc} - nadobudnutie {nc})")
    vysledok = _zaokruhli(marza * s / 100)
    return vysledok


# ---------------------------------------------------------------------------
# 2. Samozdanenie
# ---------------------------------------------------------------------------

def samozdanenie(zaklad_dane: NumType, sadzba: NumType) -> tuple[Decimal, Decimal]:
    """§ 69 Z. 222/2004 Z.z. — Samozdanenie (prenos daňovej povinnosti).

    Výstupná daň = vstupná daň = základ dane × sadzba / 100.
    Čistý efekt = 0 pri plnom odpočte.

    Returns:
        (vystupna_dan, vstupna_dan) — obe rovnaké hodnoty
    """
    d = dan(zaklad_dane, sadzba)
    return (d, d)


# ---------------------------------------------------------------------------
# 3. Invarianty
# ---------------------------------------------------------------------------

def podvojne_uctovnictvo(sum_ma_dat: NumType, sum_dal: NumType) -> bool:
    """§ 4 Z. 431/2002 Z.z. — Podvojné účtovníctvo.

    SUM(má dať) == SUM(dal) pre každý účtovný zápis.
    """
    md = _to_decimal(sum_ma_dat)
    d = _to_decimal(sum_dal)
    return md == d


def suvaha_rovnica(aktiva: NumType, pasiva: NumType) -> bool:
    """§ 18 Z. 431/2002 Z.z. — Súvaha: Aktíva = Pasíva."""
    a = _to_decimal(aktiva)
    p = _to_decimal(pasiva)
    return a == p


def ucet_ziskov_a_strat(vynosy: NumType, naklady: NumType) -> Decimal:
    """§ 18 Z. 431/2002 Z.z. — Účet ziskov a strát (účet 710).

    Výsledok hospodárenia = výnosy - náklady.
    """
    v = _to_decimal(vynosy)
    n = _to_decimal(naklady)
    return _zaokruhli(v - n)


# ---------------------------------------------------------------------------
# 4. Zaokrúhľovanie
# ---------------------------------------------------------------------------

def zaokruhlenie_dane(hodnota: NumType) -> Decimal:
    """§ 26 Z. 222/2004 Z.z. — Zaokrúhlenie dane.

    2 desatinné miesta, ROUND_HALF_UP.
    """
    return _zaokruhli(_to_decimal(hodnota))


def zaokruhlenie_prepocet(suma_v_cudzej_mene: NumType, kurz_ecb: NumType) -> Decimal:
    """§ 26 ods. 1 Z. 222/2004 Z.z. — Prepočet cudzej meny.

    suma v EUR = suma v cudzej mene × kurz ECB
    Kurz ECB vyhlásený deň pred dňom dodania.
    """
    s = _to_decimal(suma_v_cudzej_mene)
    k = _to_decimal(kurz_ecb)
    return _zaokruhli(s * k)


def zaokruhlenie_koeficient(koeficient: NumType) -> Decimal:
    """§ 50 Z. 222/2004 Z.z. — Zaokrúhlenie koeficientu.

    CEIL na 2 desatinné miesta (zaokrúhľuje sa nahor).
    """
    k = _to_decimal(koeficient)
    return (k * 100).to_integral_value(rounding=ROUND_CEILING) / 100


# ---------------------------------------------------------------------------
# 5. Prahy — konštanty
# ---------------------------------------------------------------------------

def nacitaj_prahy() -> dict[str, Decimal]:
    """Načíta všetky prahy z pojmy.json a vráti slovník {id: hodnota}."""
    with open(_POJMY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    prahy = {}
    for pojem in data["pojmy"]:
        if "hodnota" in pojem and pojem["hodnota"] is not None:
            prahy[pojem["id"]] = Decimal(str(pojem["hodnota"]))
    return prahy


def nacitaj_sadzby() -> dict[str, Decimal]:
    """Načíta sadzby dane z pojmy.json."""
    with open(_POJMY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    sadzby = {}
    for pojem in data["pojmy"]:
        if pojem["kategoria"] == "sadzba_dane":
            sadzby[pojem["id"]] = Decimal(str(pojem["hodnota"]))
    return sadzby


# ---------------------------------------------------------------------------
# 6. Generický dispatcher
# ---------------------------------------------------------------------------

_FUNKCIE = {
    "dan": dan,
    "celkova_vyska": celkova_vyska,
    "zaklad_dane_z_uhrady": zaklad_dane_z_uhrady,
    "dan_z_uhrady": dan_z_uhrady,
    "pomerny_odpocet": pomerny_odpocet,
    "odpocitatelna_dan": odpocitatelna_dan,
    "bez_prava_na_odpocet": bez_prava_na_odpocet,
    "zaklad_dane_pri_dovoze": zaklad_dane_pri_dovoze,
    "osobitny_rezim_marza": osobitny_rezim_marza,
    "samozdanenie": samozdanenie,
    "podvojne_uctovnictvo": podvojne_uctovnictvo,
    "suvaha_rovnica": suvaha_rovnica,
    "ucet_ziskov_a_strat": ucet_ziskov_a_strat,
    "zaokruhlenie_dane": zaokruhlenie_dane,
    "zaokruhlenie_prepocet": zaokruhlenie_prepocet,
    "zaokruhlenie_koeficient": zaokruhlenie_koeficient,
}


def vypocitaj(pojem_id: str, **vstupy: NumType) -> Union[Decimal, bool, tuple]:
    """Generický dispatcher — vypočíta ľubovoľný pojem podľa ID."""
    if pojem_id not in _FUNKCIE:
        raise ValueError(f"Neznámy pojem: {pojem_id}")
    return _FUNKCIE[pojem_id](**vstupy)
