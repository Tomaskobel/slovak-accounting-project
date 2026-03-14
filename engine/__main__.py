"""
CLI for the accounting engine.

Usage:
    python3 -m engine classify "Faktúra za IT služby od ACME s.r.o., základ 2000 EUR, DPH 23%"
    python3 -m engine classify "Bankový poplatok 15 EUR"
    python3 -m engine classify --context "Sme platiteľ DPH" "Nákup kancelárskych potrieb 120 EUR"
"""

import argparse
import logging

from engine.klasifikator import klasifikuj, klasifikuj_a_zauctuj, KlasifikaciaVysledok
from engine.schema import StranaUctu

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)


def cmd_classify(args: argparse.Namespace) -> None:
    """Classify and optionally book a transaction."""
    popis = args.popis
    kontext = args.context

    if args.book:
        klas, zapis = klasifikuj_a_zauctuj(popis, kontext)
    else:
        klas = klasifikuj(popis, kontext)
        zapis = None

    # Print classification result
    status_icon = {
        KlasifikaciaVysledok.USPESNA: "✓",
        KlasifikaciaVysledok.NEISTA: "?",
        KlasifikaciaVysledok.NEZNAMA: "✗",
    }

    print(f"\n{'='*60}")
    print(f"  Klasifikácia: {status_icon[klas.vysledok]} {klas.vysledok.value} (istota: {klas.dovera:.0%})")
    print(f"{'='*60}")
    print(f"\n  Zdôvodnenie: {klas.zdovodnenie}")

    if klas.transakcia:
        t = klas.transakcia
        print(f"\n  Transakcia:")
        print(f"    Smer:              {t.smer.value}")
        print(f"    Typ plnenia:       {t.typ_plnenia.value if t.typ_plnenia else '—'}")
        print(f"    Krajina:           {t.krajina_dodavatela.value if t.krajina_dodavatela else '—'}")
        print(f"    Platiteľ DPH (my): {t.platitel_dph_kupujuci}")
        print(f"    Platiteľ DPH (dd): {t.platitel_dph_dodavatel}")
        if t.forma_uhrady:
            print(f"    Forma úhrady:      {t.forma_uhrady}")
        if t.tuzemsky_prenos:
            print(f"    Tuzemský prenos:   {t.tuzemsky_prenos}")
        if t.zaklad_dane:
            print(f"    Základ dane:       {t.zaklad_dane}")
        if t.celkova_suma:
            print(f"    Celková suma:      {t.celkova_suma}")
        if t.sadzba_dane:
            print(f"    Sadzba dane:       {t.sadzba_dane}%")

    if klas.pravidlo_id:
        print(f"\n  Pravidlo: {klas.pravidlo_id}")

    if klas.alternativy:
        print(f"\n  Alternatívy:")
        for alt in klas.alternativy:
            print(f"    - {alt.get('smer', '?')}/{alt.get('typ_plnenia', '?')} "
                  f"(istota: {alt.get('dovera', 0):.0%}) — {alt.get('zdovodnenie', '')}")

    if zapis:
        print(f"\n  {'─'*56}")
        print(f"  Účtovný zápis (pravidlo: {zapis.pravidlo_id}):")
        print(f"  {'─'*56}")
        print(f"  {'Účet':<8} {'Strana':<6} {'Suma':>12}   Popis")
        print(f"  {'─'*56}")
        for r in zapis.riadky:
            strana = "MD" if r.strana == StranaUctu.MA_DAT else "D"
            print(f"  {r.ucet:<8} {strana:<6} {r.suma:>12,.2f}   {r.popis}")
        print(f"  {'─'*56}")
        print(f"  {'MD celkom:':<14} {zapis.suma_ma_dat:>12,.2f}")
        print(f"  {'D celkom:':<14} {zapis.suma_dal:>12,.2f}")
        print(f"  Vyvážený: {'✓' if zapis.je_vyvazeny else '✗'}")
        if zapis.suma_dph:
            print(f"  DPH: {zapis.suma_dph:,.2f} ({zapis.sadzba_dane}%)")
        print(f"  KV DPH: {zapis.kv_dph_sekcia.value}")
        print(f"  Právny zdroj: {zapis.pravny_zdroj}")

    print()


def main():
    parser = argparse.ArgumentParser(description="Slovak Accounting Engine CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_classify = subparsers.add_parser("classify", help="Classify a transaction")
    p_classify.add_argument("popis", help="Transaction description (Slovak or English)")
    p_classify.add_argument("--context", help="Additional context (e.g., VAT status)")
    p_classify.add_argument("--book", action="store_true", help="Also generate journal entry")
    p_classify.set_defaults(func=cmd_classify)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
