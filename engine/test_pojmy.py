"""
Testy pre pojmy a vzorce slovenského účtovníctva.

Testové prípady vychádzajú z practical_examples.json a overených hodnôt
podľa Zákona 222/2004 Z.z. a Opatrenia MF SR 23054/2002-92.
"""

import pytest
from decimal import Decimal

from engine.pojmy import (
    dan,
    celkova_vyska,
    zaklad_dane_z_uhrady,
    dan_z_uhrady,
    pomerny_odpocet,
    odpocitatelna_dan,
    bez_prava_na_odpocet,
    zaklad_dane_pri_dovoze,
    osobitny_rezim_marza,
    samozdanenie,
    podvojne_uctovnictvo,
    suvaha_rovnica,
    ucet_ziskov_a_strat,
    zaokruhlenie_dane,
    zaokruhlenie_prepocet,
    zaokruhlenie_koeficient,
    nacitaj_prahy,
    nacitaj_sadzby,
    vypocitaj,
)


# ===========================================================================
# 1. Výpočty DPH — základné scenáre
# ===========================================================================

class TestDan:
    """§ 22-27 Z. 222/2004 Z.z. — Daň (daňová suma)."""

    def test_standardna_sadzba_23(self):
        """Štandardný nákup: základ 1000 EUR × 23 % = 230 EUR."""
        assert dan(1000, 23) == Decimal("230.00")

    def test_znizena_sadzba_19(self):
        """Reštauračné služby: základ 500 EUR × 19 % = 95 EUR."""
        assert dan(500, 19) == Decimal("95.00")

    def test_znizena_sadzba_5(self):
        """Základné potraviny: základ 200 EUR × 5 % = 10 EUR."""
        assert dan(200, 5) == Decimal("10.00")

    def test_nulova_sadzba(self):
        """Vývoz: základ 5000 EUR × 0 % = 0 EUR."""
        assert dan(5000, 0) == Decimal("0.00")

    def test_zaokruhlenie(self):
        """Overenie zaokrúhlenia: 123.45 × 23 % = 28.3935 → 28.39."""
        assert dan("123.45", 23) == Decimal("28.39")

    def test_zaokruhlenie_half_up(self):
        """ROUND_HALF_UP: 100.00 × 23 % = 23.00 (presné)."""
        assert dan(100, 23) == Decimal("23.00")

    def test_male_sumy(self):
        """Malá suma: 1.50 × 23 % = 0.345 → 0.35 (ROUND_HALF_UP)."""
        assert dan("1.50", 23) == Decimal("0.35")

    def test_decimal_vstup(self):
        """Funguje s Decimal vstupmi."""
        assert dan(Decimal("1000"), Decimal("23")) == Decimal("230.00")


class TestCelkovaVyska:
    """§ 22 Z. 222/2004 Z.z. — Celková výška úhrady."""

    def test_zaklad_plus_dan(self):
        """1000 + 230 = 1230."""
        assert celkova_vyska(1000, 230) == Decimal("1230.00")

    def test_nulova_dan(self):
        """Oslobodenie: 5000 + 0 = 5000."""
        assert celkova_vyska(5000, 0) == Decimal("5000.00")


class TestZakladDaneZUhrady:
    """§ 26 Z. 222/2004 Z.z. — Spätný výpočet základu dane."""

    def test_spatny_vypocet_23(self):
        """1230 / 1.23 = 1000.00."""
        assert zaklad_dane_z_uhrady(1230, 23) == Decimal("1000.00")

    def test_spatny_vypocet_19(self):
        """595 / 1.19 = 500.00."""
        assert zaklad_dane_z_uhrady(595, 19) == Decimal("500.00")

    def test_spatny_vypocet_5(self):
        """210 / 1.05 = 200.00."""
        assert zaklad_dane_z_uhrady(210, 5) == Decimal("200.00")

    def test_preddavok(self):
        """Preddavok 2460 EUR vrátane DPH 23 %: základ = 2000.00."""
        assert zaklad_dane_z_uhrady(2460, 23) == Decimal("2000.00")

    def test_zaokruhlenie_spatny(self):
        """120 / 1.23 = 97.56 (zaokrúhlené)."""
        assert zaklad_dane_z_uhrady(120, 23) == Decimal("97.56")


class TestDanZUhrady:
    """§ 26 Z. 222/2004 Z.z. — Daň z celkovej výšky."""

    def test_dan_z_celku(self):
        """1230 - 1000 = 230."""
        assert dan_z_uhrady(1230, 1000) == Decimal("230.00")


# ===========================================================================
# 2. Koeficient a pomerný odpočet
# ===========================================================================

class TestPomernyOdpocet:
    """§ 50 Z. 222/2004 Z.z. — Pomerný odpočet (koeficient)."""

    def test_plny_odpocet(self):
        """100 % zdaniteľné → koeficient = 1.00."""
        assert pomerny_odpocet(100000, 0) == Decimal("1.00")

    def test_polovicny(self):
        """50/50 → koeficient = 0.50 (presné, CEIL nemení)."""
        assert pomerny_odpocet(50000, 50000) == Decimal("0.50")

    def test_80_20(self):
        """80k zdaniteľné, 20k oslobodené → 0.80."""
        assert pomerny_odpocet(80000, 20000) == Decimal("0.80")

    def test_zaokruhlenie_nahor(self):
        """CEIL: 70000 / (70000 + 30000) = 0.70 (presné).
        73000 / 100000 = 0.73 (presné).
        73001 / 100000 = 0.73001 → CEIL → 0.74."""
        assert pomerny_odpocet(73001, 26999) == Decimal("0.74")

    def test_s_vylucenymi(self):
        """S vylúčenými: 80k / (80k + 20k - 5k) = 80k / 95k = 0.8421 → CEIL → 0.85."""
        assert pomerny_odpocet(80000, 20000, 5000) == Decimal("0.85")


class TestOdpocitatelna:
    """§ 49-50 Z. 222/2004 Z.z. — Odpočítateľná daň."""

    def test_plny_odpocet(self):
        """Koeficient 1.0: odpočítateľná = vstupná."""
        assert odpocitatelna_dan(230, "1.00") == Decimal("230.00")

    def test_pomerny(self):
        """Koeficient 0.80: 230 × 0.80 = 184.00."""
        assert odpocitatelna_dan(230, "0.80") == Decimal("184.00")


class TestBezPravaNaOdpocet:
    """§ 49-50 Z. 222/2004 Z.z. — Daň bez práva na odpočet."""

    def test_pomerny(self):
        """Koeficient 0.80: 230 × 0.20 = 46.00."""
        assert bez_prava_na_odpocet(230, "0.80") == Decimal("46.00")

    def test_kontrola_suctu(self):
        """odpočítateľná + bez práva = vstupná."""
        vstupna = Decimal("230.00")
        koef = Decimal("0.80")
        odp = odpocitatelna_dan(vstupna, koef)
        bez = bez_prava_na_odpocet(vstupna, koef)
        assert odp + bez == vstupna


# ===========================================================================
# 3. Dovoz a osobitný režim
# ===========================================================================

class TestZakladPriDovoze:
    """§ 24 Z. 222/2004 Z.z. — Základ dane pri dovoze."""

    def test_dovoz_s_clom(self):
        """Colná hodnota 5000 + clo 200 = 5200."""
        assert zaklad_dane_pri_dovoze(5000, 200) == Decimal("5200.00")


class TestOsobitnyRezim:
    """§ 65-66 Z. 222/2004 Z.z. — Zdanenie marže."""

    def test_marza_cestovna_kancelaria(self):
        """Predaj 1000, nadobudnutie 800, sadzba 23 %: marža 200 × 0.23 = 46."""
        assert osobitny_rezim_marza(1000, 800, 23) == Decimal("46.00")


# ===========================================================================
# 4. Samozdanenie
# ===========================================================================

class TestSamozdanenie:
    """§ 69 Z. 222/2004 Z.z. — Samozdanenie (prenos daňovej povinnosti)."""

    def test_nadobudnutie_z_eu(self):
        """IC nadobudnutie 2500 EUR × 23 %: výstupná = vstupná = 575, čistý efekt = 0."""
        vystupna, vstupna = samozdanenie(2500, 23)
        assert vystupna == Decimal("575.00")
        assert vstupna == Decimal("575.00")
        assert vystupna - vstupna == Decimal("0.00")

    def test_tuzemsky_prenos_stavebne_prace(self):
        """Stavebné práce 10000 EUR × 23 %: výstupná = vstupná = 2300."""
        vystupna, vstupna = samozdanenie(10000, 23)
        assert vystupna == Decimal("2300.00")
        assert vystupna == vstupna


# ===========================================================================
# 5. Invarianty
# ===========================================================================

class TestInvarianty:
    """§ 4 Z. 431/2002 Z.z. — Podvojné účtovníctvo a súvaha."""

    def test_podvojny_zapis_spravny(self):
        """MD 1230 == D 1230 → True."""
        assert podvojne_uctovnictvo(1230, 1230) is True

    def test_podvojny_zapis_nespravny(self):
        """MD 1230 != D 1000 → False."""
        assert podvojne_uctovnictvo(1230, 1000) is False

    def test_suvaha(self):
        """Aktíva 500000 == Pasíva 500000 → True."""
        assert suvaha_rovnica(500000, 500000) is True

    def test_suvaha_nespravna(self):
        """Aktíva 500000 != Pasíva 499000 → False."""
        assert suvaha_rovnica(500000, 499000) is False

    def test_vysledok_hospodarenia(self):
        """Výnosy 100000 - Náklady 80000 = VH 20000."""
        assert ucet_ziskov_a_strat(100000, 80000) == Decimal("20000.00")

    def test_strata(self):
        """Výnosy 50000 - Náklady 80000 = VH -30000."""
        assert ucet_ziskov_a_strat(50000, 80000) == Decimal("-30000.00")


# ===========================================================================
# 6. Zaokrúhľovanie
# ===========================================================================

class TestZaokruhlenie:
    """§ 26 Z. 222/2004 Z.z. — Zaokrúhľovanie."""

    def test_dane_half_up(self):
        """0.005 → 0.01 (ROUND_HALF_UP)."""
        assert zaokruhlenie_dane("0.005") == Decimal("0.01")

    def test_dane_presne(self):
        """230.00 → 230.00."""
        assert zaokruhlenie_dane("230.00") == Decimal("230.00")

    def test_dane_tri_desatinne(self):
        """28.3935 → 28.39."""
        assert zaokruhlenie_dane("28.3935") == Decimal("28.39")

    def test_prepocet_cudzej_meny(self):
        """1000 USD × 0.92 = 920.00 EUR."""
        assert zaokruhlenie_prepocet(1000, "0.92") == Decimal("920.00")

    def test_prepocet_zaokruhlenie(self):
        """1234.56 USD × 0.9187 = 1134.18..."""
        vysledok = zaokruhlenie_prepocet("1234.56", "0.9187")
        assert vysledok == Decimal("1134.19")

    def test_koeficient_ceil(self):
        """0.7301 → CEIL → 0.74."""
        assert zaokruhlenie_koeficient("0.7301") == Decimal("0.74")

    def test_koeficient_presny(self):
        """0.80 → 0.80 (CEIL nemení presné)."""
        assert zaokruhlenie_koeficient("0.80") == Decimal("0.80")


# ===========================================================================
# 7. Prahy a sadzby z pojmy.json
# ===========================================================================

class TestPrahy:
    """Overenie prahov podľa Z. 222/2004 Z.z. (2025 hodnoty)."""

    @pytest.fixture
    def prahy(self) -> dict[str, Decimal]:
        return nacitaj_prahy()

    def test_registracia_obrat(self, prahy):
        assert prahy["prah_registracia_obrat"] == Decimal("50000")

    def test_registracia_dodavka(self, prahy):
        assert prahy["prah_registracia_dodavka"] == Decimal("62500")

    def test_nadobudnutie_eu(self, prahy):
        assert prahy["prah_nadobudnutie_tovaru"] == Decimal("14000")

    def test_zjednodusena_faktura_2025(self, prahy):
        """Od 2025: 400 EUR (predtým 100 EUR)."""
        assert prahy["prah_zjednodusena_faktura"] == Decimal("400")

    def test_stvrtrocne_obdobie(self, prahy):
        assert prahy["prah_stvrtrocne_obdobie"] == Decimal("100000")

    def test_rezim_prijatia_platby_2025(self, prahy):
        """Od 2025: 100 000 EUR (predtým 150 000 EUR)."""
        assert prahy["prah_rezim_prijatia_platby"] == Decimal("100000")

    def test_investicny_majetok_2025(self, prahy):
        """Od 2025: 1 700 EUR (predtým 5 000 EUR)."""
        assert prahy["prah_investicny_majetok"] == Decimal("1700")

    def test_zasielkovy_predaj(self, prahy):
        assert prahy["prah_zasielkovy_predaj"] == Decimal("10000")

    def test_prenos_elektronika(self, prahy):
        assert prahy["prah_prenos_elektronika"] == Decimal("5000")

    def test_dar_dodanie(self, prahy):
        assert prahy["prah_dodanie_sa_povazuje"] == Decimal("17")

    def test_vratenie_dane(self, prahy):
        assert prahy["prah_vratenie_dane"] == Decimal("100")

    def test_suhrnny_vykaz(self, prahy):
        assert prahy["prah_suhrnny_vykaz"] == Decimal("50000")

    def test_danova_zaruka_min(self, prahy):
        assert prahy["prah_danova_zaruka_min"] == Decimal("1000")

    def test_danova_zaruka_max(self, prahy):
        assert prahy["prah_danova_zaruka_max"] == Decimal("500000")

    def test_kv_ine_vstupne_doklady(self, prahy):
        """B.3 prah: 3 000 EUR."""
        assert prahy["prah_kv_ine_vstupne_doklady"] == Decimal("3000")

    def test_kv_prenos_elektronika(self, prahy):
        """A.2 prah: 5 000 EUR (základ dane)."""
        assert prahy["prah_kv_prenos_elektronika"] == Decimal("5000")


class TestSadzby:
    """Overenie sadzieb dane (2025 hodnoty)."""

    @pytest.fixture
    def sadzby(self) -> dict[str, Decimal]:
        return nacitaj_sadzby()

    def test_sadzba_23(self, sadzby):
        assert sadzby["sadzba_dane_23"] == Decimal("23")

    def test_sadzba_19(self, sadzby):
        assert sadzby["sadzba_dane_19"] == Decimal("19")

    def test_sadzba_5(self, sadzby):
        assert sadzby["sadzba_dane_5"] == Decimal("5")

    def test_sadzba_0(self, sadzby):
        assert sadzby["sadzba_dane_0"] == Decimal("0")


# ===========================================================================
# 8. Generický dispatcher
# ===========================================================================

class TestVypocitaj:
    """Generický dispatcher — vypocitaj()."""

    def test_dan(self):
        assert vypocitaj("dan", zaklad_dane=1000, sadzba=23) == Decimal("230.00")

    def test_neznamy_pojem(self):
        with pytest.raises(ValueError, match="Neznámy pojem"):
            vypocitaj("neexistuje", x=1)


# ===========================================================================
# 9. Integračné scenáre z practical_examples.json
# ===========================================================================

class TestIntegracneScenare:
    """End-to-end výpočty podľa practical_examples.json."""

    def test_nakup_telekom_sluzby_tuzemsko(self):
        """Nákup telekomunikačných služieb, tuzemský dodávateľ, 23 %.
        Celková suma 120 EUR → základ 97.56, DPH 22.44.
        Overenie: MD 518 (97.56) + MD 343 (22.44) = D 321 (120.00).
        """
        zaklad = zaklad_dane_z_uhrady(120, 23)
        d = dan_z_uhrady(120, zaklad)
        assert zaklad == Decimal("97.56")
        assert d == Decimal("22.44")
        assert zaklad + d == Decimal("120.00")
        assert podvojne_uctovnictvo(zaklad + d, Decimal("120.00")) is True

    def test_predaj_tovaru_23(self):
        """Predaj tovaru za 1000 EUR + 23 % DPH.
        DPH = 230, celkom = 1230.
        MD 311 (1230) = D 604 (1000) + D 343 (230).
        """
        d = dan(1000, 23)
        celkom = celkova_vyska(1000, d)
        assert d == Decimal("230.00")
        assert celkom == Decimal("1230.00")
        assert podvojne_uctovnictvo(celkom, Decimal("1000") + d) is True

    def test_nadobudnutie_eu_samozdanenie(self):
        """IC nadobudnutie tovaru z EÚ: 2500 EUR základ, 23 %.
        Samozdanenie: výstupná = vstupná = 575 EUR. Čistý efekt = 0.
        """
        vystupna, vstupna = samozdanenie(2500, 23)
        assert vystupna == Decimal("575.00")
        assert vystupna == vstupna
        # Overenie účtovného zápisu:
        # MD 112: 2500, MD 349: 575, MD 343: 575, D 321: 2500, D 349: 575, D 343: 575
        suma_md = Decimal("2500") + Decimal("575") + Decimal("575")
        suma_d = Decimal("2500") + Decimal("575") + Decimal("575")
        assert podvojne_uctovnictvo(suma_md, suma_d) is True

    def test_dovoz_z_tretej_krajiny(self):
        """Dovoz: colná hodnota 5000, clo 4 % = 200, DPH základ = 5200.
        DPH = 5200 × 23 % = 1196.
        """
        zaklad = zaklad_dane_pri_dovoze(5000, 200)
        d = dan(zaklad, 23)
        assert zaklad == Decimal("5200.00")
        assert d == Decimal("1196.00")

    def test_preddavok_z_celkovej_sumy(self):
        """Preddavok 2460 EUR vrátane DPH 23 %.
        Základ = 2000, DPH = 460.
        """
        zaklad = zaklad_dane_z_uhrady(2460, 23)
        d = dan_z_uhrady(2460, zaklad)
        assert zaklad == Decimal("2000.00")
        assert d == Decimal("460.00")

    def test_pomerny_odpocet_80_20(self):
        """Firma: 80k zdaniteľné, 20k oslobodené.
        Koeficient = 0.80. Vstupná DPH 1000 EUR.
        Odpočítateľná = 800, bez práva = 200.
        """
        koef = pomerny_odpocet(80000, 20000)
        odp = odpocitatelna_dan(1000, koef)
        bez = bez_prava_na_odpocet(1000, koef)
        assert koef == Decimal("0.80")
        assert odp == Decimal("800.00")
        assert bez == Decimal("200.00")
        assert odp + bez == Decimal("1000.00")

    def test_marza_pouzity_tovar(self):
        """Použitý tovar: kúpa 800, predaj 1000, sadzba 23 %.
        Marža = 200, DPH z marže = 46.
        """
        d = osobitny_rezim_marza(1000, 800, 23)
        assert d == Decimal("46.00")
