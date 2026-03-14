"""
Testy pre motor účtovania — full pipeline tests.

Each test represents a real-world s.r.o. transaction,
verified against practical_examples.json expected outputs.
"""

import pytest
from decimal import Decimal

from engine.motor import Transakcia, zauctuj, najdi_zhody, generuj_zapis, validuj_zapis, vyber_pravidlo
from engine.schema import (
    SmerTransakcie, TypPlnenia, KrajinaDodavatela,
    DphTreatment, KvDphSekcia, StranaUctu,
)
from engine.pravidla import VSETKY_PRAVIDLA


# ===========================================================================
# 1. Nákup materiálu — tuzemsko
# ===========================================================================

class TestNakupMaterialu:
    """Nákup materiálu od tuzemského dodávateľa."""

    def test_metoda_a_zakladny(self):
        """Základ 1000, sadzba 23 %, celkom 1230.
        MD 112: 1000, MD 343: 230, D 321: 1230.
        """
        t = Transakcia(
            smer=SmerTransakcie.NAKUP,
            typ_plnenia=TypPlnenia.MATERIAL,
            krajina_dodavatela=KrajinaDodavatela.SK,
            platitel_dph_kupujuci=True,
            platitel_dph_dodavatel=True,
            metoda_zasob="A",
            zaklad_dane=Decimal("1000"),
            sadzba_dane=Decimal("23"),
        )
        zapis = zauctuj(t)

        assert zapis.je_vyvazeny
        assert zapis.pravidlo_id == "nakup_materialu_tuzemsko_a"
        assert zapis.dph_treatment == DphTreatment.VSTUPNA_DAN
        assert zapis.kv_dph_sekcia == KvDphSekcia.B2
        assert zapis.zaklad_dane == Decimal("1000.00")
        assert zapis.suma_dph == Decimal("230.00")
        assert len(zapis.riadky) == 3

        # Check posting lines
        md_112 = [r for r in zapis.riadky if r.ucet == "112" and r.strana == StranaUctu.MA_DAT]
        md_343 = [r for r in zapis.riadky if r.ucet == "343" and r.strana == StranaUctu.MA_DAT]
        d_321 = [r for r in zapis.riadky if r.ucet == "321" and r.strana == StranaUctu.DAL]

        assert md_112[0].suma == Decimal("1000.00")
        assert md_343[0].suma == Decimal("230.00")
        assert d_321[0].suma == Decimal("1230.00")

    def test_metoda_b(self):
        """Metóda B: priama spotreba → účet 501 namiesto 112."""
        t = Transakcia(
            smer=SmerTransakcie.NAKUP,
            typ_plnenia=TypPlnenia.MATERIAL,
            krajina_dodavatela=KrajinaDodavatela.SK,
            platitel_dph_kupujuci=True,
            platitel_dph_dodavatel=True,
            metoda_zasob="B",
            zaklad_dane=Decimal("500"),
            sadzba_dane=Decimal("23"),
        )
        zapis = zauctuj(t)

        assert zapis.pravidlo_id == "nakup_materialu_tuzemsko_b"
        ucty = [r.ucet for r in zapis.riadky if r.strana == StranaUctu.MA_DAT]
        assert "501" in ucty
        assert "112" not in ucty


# ===========================================================================
# 2. Nákup služieb — tuzemsko
# ===========================================================================

class TestNakupSluzieb:
    """Nákup služieb od tuzemského dodávateľa."""

    def test_zakladny(self):
        """Telekom služby: základ 97.56 (z celku 120 / 1.23)."""
        t = Transakcia(
            smer=SmerTransakcie.NAKUP,
            typ_plnenia=TypPlnenia.SLUZBA,
            krajina_dodavatela=KrajinaDodavatela.SK,
            platitel_dph_kupujuci=True,
            platitel_dph_dodavatel=True,
            zaklad_dane=Decimal("600"),
            sadzba_dane=Decimal("23"),
        )
        zapis = zauctuj(t)

        assert zapis.je_vyvazeny
        assert zapis.pravidlo_id == "nakup_sluzieb_tuzemsko"
        assert zapis.kv_dph_sekcia == KvDphSekcia.B2

        ucty_md = {r.ucet for r in zapis.riadky if r.strana == StranaUctu.MA_DAT}
        assert "518" in ucty_md
        assert "343" in ucty_md


# ===========================================================================
# 3. Predaj tovaru — tuzemsko
# ===========================================================================

class TestPredajTovaru:
    """Predaj tovaru tuzemskému odberateľovi."""

    def test_zakladny(self):
        """Predaj: základ 3000, DPH 690, celkom 3690, COGS 2200.
        MD 311: 3690, D 604: 3000, D 343: 690, MD 504: 2200, D 132: 2200.
        """
        t = Transakcia(
            smer=SmerTransakcie.PREDAJ,
            typ_plnenia=TypPlnenia.TOVAR,
            krajina_dodavatela=KrajinaDodavatela.SK,
            platitel_dph_dodavatel=True,
            zaklad_dane=Decimal("3000"),
            sadzba_dane=Decimal("23"),
            nadobudacia_cena=Decimal("2200"),
        )
        zapis = zauctuj(t)

        assert zapis.je_vyvazeny
        assert zapis.pravidlo_id == "predaj_tovaru_tuzemsko"
        assert zapis.dph_treatment == DphTreatment.VYSTUPNA_DAN
        assert zapis.kv_dph_sekcia == KvDphSekcia.A1

        # Revenue
        d_604 = [r for r in zapis.riadky if r.ucet == "604"]
        assert d_604[0].suma == Decimal("3000.00")

        # DPH
        d_343 = [r for r in zapis.riadky if r.ucet == "343"]
        assert d_343[0].suma == Decimal("690.00")

        # Receivable
        md_311 = [r for r in zapis.riadky if r.ucet == "311"]
        assert md_311[0].suma == Decimal("3690.00")

        # COGS
        md_504 = [r for r in zapis.riadky if r.ucet == "504"]
        assert md_504[0].suma == Decimal("2200.00")

        # Total: MD = 3690 + 2200 = 5890, D = 3000 + 690 + 2200 = 5890
        assert zapis.suma_ma_dat == Decimal("5890.00")
        assert zapis.suma_dal == Decimal("5890.00")


# ===========================================================================
# 4. Predaj služieb — tuzemsko
# ===========================================================================

class TestPredajSluzieb:
    """Predaj služieb tuzemskému odberateľovi."""

    def test_zakladny(self):
        """IT consulting: základ 2000, DPH 460, celkom 2460."""
        t = Transakcia(
            smer=SmerTransakcie.PREDAJ,
            typ_plnenia=TypPlnenia.SLUZBA,
            krajina_dodavatela=KrajinaDodavatela.SK,
            platitel_dph_dodavatel=True,
            zaklad_dane=Decimal("2000"),
            sadzba_dane=Decimal("23"),
        )
        zapis = zauctuj(t)

        assert zapis.je_vyvazeny
        assert zapis.kv_dph_sekcia == KvDphSekcia.A1

        d_602 = [r for r in zapis.riadky if r.ucet == "602"]
        assert d_602[0].suma == Decimal("2000.00")


# ===========================================================================
# 5. Nákup z EÚ — samozdanenie
# ===========================================================================

class TestNakupEU:
    """Nadobudnutie tovaru z EÚ — samozdanenie."""

    def test_samozdanenie(self):
        """IC nadobudnutie 2500 EUR, 23 %. Čistý efekt DPH = 0."""
        t = Transakcia(
            smer=SmerTransakcie.NAKUP,
            typ_plnenia=TypPlnenia.TOVAR,
            krajina_dodavatela=KrajinaDodavatela.EU,
            platitel_dph_kupujuci=True,
            platitel_dph_dodavatel=True,
            zaklad_dane=Decimal("2500"),
            sadzba_dane=Decimal("23"),
        )
        zapis = zauctuj(t)

        assert zapis.je_vyvazeny
        assert zapis.dph_treatment == DphTreatment.SAMOZDANENIE
        assert zapis.kv_dph_sekcia == KvDphSekcia.B1

        # Check samozdanenie: MD 349 = D 343 = 575
        md_349 = [r for r in zapis.riadky if r.ucet == "349" and r.strana == StranaUctu.MA_DAT]
        d_343 = [r for r in zapis.riadky if r.ucet == "343" and r.strana == StranaUctu.DAL]
        assert md_349[0].suma == Decimal("575.00")
        assert d_343[0].suma == Decimal("575.00")

        # Payable = base only (no DPH to EU supplier)
        d_321 = [r for r in zapis.riadky if r.ucet == "321"]
        assert d_321[0].suma == Decimal("2500.00")


# ===========================================================================
# 6. Prijatie služby z EÚ — prenos
# ===========================================================================

class TestPrijimanieSluzbyEU:
    """Prijatie služby z EÚ s prenosom daňovej povinnosti."""

    def test_reverse_charge(self):
        """Služba z DE: základ 3000, samozdanenie 23 % = 690."""
        t = Transakcia(
            smer=SmerTransakcie.NAKUP,
            typ_plnenia=TypPlnenia.SLUZBA,
            krajina_dodavatela=KrajinaDodavatela.EU,
            platitel_dph_kupujuci=True,
            zaklad_dane=Decimal("3000"),
            sadzba_dane=Decimal("23"),
        )
        zapis = zauctuj(t)

        assert zapis.je_vyvazeny
        assert zapis.dph_treatment == DphTreatment.SAMOZDANENIE
        assert zapis.kv_dph_sekcia == KvDphSekcia.B1

        # MD 518: 3000, D 321: 3000, MD 349: 690, D 343: 690
        assert zapis.suma_ma_dat == Decimal("3690.00")
        assert zapis.suma_dal == Decimal("3690.00")


# ===========================================================================
# 7. Nákup DHM — 2 kroky
# ===========================================================================

class TestNakupDHM:
    """Nákup dlhodobého hmotného majetku — 2-krokový proces."""

    def test_krok1_faktura(self):
        """Krok 1: prijatie faktúry za stroj. Základ 20000, DPH 4600."""
        t = Transakcia(
            smer=SmerTransakcie.NAKUP,
            typ_plnenia=TypPlnenia.DLHODOBY_MAJETOK,
            krajina_dodavatela=KrajinaDodavatela.SK,
            platitel_dph_kupujuci=True,
            platitel_dph_dodavatel=True,
            zaklad_dane=Decimal("20000"),
            sadzba_dane=Decimal("23"),
        )
        # Filter to step 1 only
        pravidla_krok1 = [p for p in VSETKY_PRAVIDLA if p.krok == 1]
        zapis = zauctuj(t, pravidla_krok1)

        assert zapis.je_vyvazeny
        assert zapis.kv_dph_sekcia == KvDphSekcia.B2

        md_042 = [r for r in zapis.riadky if r.ucet == "042"]
        assert md_042[0].suma == Decimal("20000.00")

        md_343 = [r for r in zapis.riadky if r.ucet == "343"]
        assert md_343[0].suma == Decimal("4600.00")


# ===========================================================================
# 8. Dobropis prijatý
# ===========================================================================

class TestDobropisPrijaty:
    """Dobropis od dodávateľa — zníženie nákupu."""

    def test_zakladny(self):
        """Dobropis: základ 300, DPH 69, celkom 369."""
        t = Transakcia(
            smer=SmerTransakcie.OPRAVA,
            krajina_dodavatela=KrajinaDodavatela.SK,
            platitel_dph_kupujuci=True,
            zaklad_dane=Decimal("300"),
            sadzba_dane=Decimal("23"),
        )
        zapis = zauctuj(t)

        assert zapis.je_vyvazeny
        assert zapis.dph_treatment == DphTreatment.OPRAVA_VSTUPNEJ
        assert zapis.kv_dph_sekcia == KvDphSekcia.C2

        # MD 321: 300 + 69 = 369 (zníženie záväzku)
        md_321 = [r for r in zapis.riadky if r.ucet == "321" and r.strana == StranaUctu.MA_DAT]
        suma_321 = sum(r.suma for r in md_321)
        assert suma_321 == Decimal("369.00")


# ===========================================================================
# 9. Dobropis vydaný
# ===========================================================================

class TestDobropisVydany:
    """Dobropis vydaný odberateľovi — zníženie predaja."""

    def test_zakladny(self):
        """Dobropis: základ 500, DPH 115, celkom 615."""
        t = Transakcia(
            smer=SmerTransakcie.OPRAVA,
            typ_plnenia=TypPlnenia.TOVAR,
            krajina_dodavatela=KrajinaDodavatela.SK,
            platitel_dph_dodavatel=True,
            zaklad_dane=Decimal("500"),
            sadzba_dane=Decimal("23"),
        )
        zapis = zauctuj(t)

        assert zapis.je_vyvazeny
        assert zapis.dph_treatment == DphTreatment.OPRAVA_VYSTUPNEJ
        assert zapis.kv_dph_sekcia == KvDphSekcia.C1


# ===========================================================================
# 10. Preddavok — krok 1 (platba)
# ===========================================================================

class TestPreddavok:
    """Preddavok s DPH — viacstupňový proces."""

    def test_krok1_platba(self):
        """Krok 1: platba preddavku 2460 EUR."""
        t = Transakcia(
            smer=SmerTransakcie.PREDDAVOK,
            krajina_dodavatela=KrajinaDodavatela.SK,
            platitel_dph_kupujuci=True,
            forma_uhrady="preddavok",
            preddavkova_suma=Decimal("2460"),
        )
        pravidla_krok1 = [p for p in VSETKY_PRAVIDLA if p.krok == 1]
        zapis = zauctuj(t, pravidla_krok1)

        assert zapis.je_vyvazeny
        assert zapis.dph_treatment == DphTreatment.BEZ_DPH

        md_314 = [r for r in zapis.riadky if r.ucet == "314"]
        assert md_314[0].suma == Decimal("2460.00")


# ===========================================================================
# Validácia — invarianty
# ===========================================================================

class TestValidacia:
    """Test validation rules."""

    def test_vyvazeny_zapis(self):
        """Vyvážený zápis: žiadne chyby."""
        t = Transakcia(
            smer=SmerTransakcie.NAKUP,
            typ_plnenia=TypPlnenia.SLUZBA,
            krajina_dodavatela=KrajinaDodavatela.SK,
            platitel_dph_kupujuci=True,
            platitel_dph_dodavatel=True,
            zaklad_dane=Decimal("1000"),
            sadzba_dane=Decimal("23"),
        )
        zapis = zauctuj(t)
        chyby = validuj_zapis(zapis)
        assert chyby == []

    def test_ziadna_zhoda(self):
        """Žiadne pravidlo sa nezhoduje → ValueError."""
        t = Transakcia(
            smer=SmerTransakcie.NAKUP,
            typ_plnenia=TypPlnenia.DLHODOBY_MAJETOK,
            krajina_dodavatela=KrajinaDodavatela.TRETIA_KRAJINA,
        )
        # Filter to empty set — no rules match DHM from non-EU with no other conditions
        pravidla_prazdne = [p for p in VSETKY_PRAVIDLA if p.id == "neexistujuce"]
        with pytest.raises(ValueError, match="Žiadne pravidlá"):
            zauctuj(t, pravidla_prazdne)


# ===========================================================================
# Conflict resolution
# ===========================================================================

class TestKonfliktRiesenie:
    """Test rule priority and conflict resolution."""

    def test_metoda_a_vs_b(self):
        """Metóda A a B majú rovnakú prioritu ale rôzne podmienky.
        S metóda_zasob="A" → len metóda A sa zhoduje.
        """
        t = Transakcia(
            smer=SmerTransakcie.NAKUP,
            typ_plnenia=TypPlnenia.MATERIAL,
            krajina_dodavatela=KrajinaDodavatela.SK,
            platitel_dph_kupujuci=True,
            platitel_dph_dodavatel=True,
            metoda_zasob="A",
            zaklad_dane=Decimal("1000"),
            sadzba_dane=Decimal("23"),
        )
        zhody = najdi_zhody(t)
        assert len(zhody) == 1
        assert zhody[0].id == "nakup_materialu_tuzemsko_a"

    def test_eu_vs_tuzemsko(self):
        """EU dodávateľ → EU pravidlo (vyššia priorita)."""
        t = Transakcia(
            smer=SmerTransakcie.NAKUP,
            typ_plnenia=TypPlnenia.TOVAR,
            krajina_dodavatela=KrajinaDodavatela.EU,
            platitel_dph_kupujuci=True,
            platitel_dph_dodavatel=True,
            zaklad_dane=Decimal("2500"),
            sadzba_dane=Decimal("23"),
        )
        pravidlo = vyber_pravidlo(t)
        assert pravidlo.id == "nadobudnutie_tovaru_eu"


# ===========================================================================
# 11. Nákup materiálu od neplatiteľa DPH
# ===========================================================================

class TestNakupNeplatitel:
    """Nákup materiálu od tuzemského neplatiteľa DPH."""

    def test_zakladny(self):
        """Celá suma ide do obstarávacej ceny, žiadna DPH."""
        t = Transakcia(
            smer=SmerTransakcie.NAKUP,
            typ_plnenia=TypPlnenia.MATERIAL,
            krajina_dodavatela=KrajinaDodavatela.SK,
            platitel_dph_kupujuci=True,
            platitel_dph_dodavatel=False,
            metoda_zasob="A",
            celkova_suma=Decimal("800"),
        )
        zapis = zauctuj(t)

        assert zapis.je_vyvazeny
        assert zapis.pravidlo_id == "nakup_materialu_neplatitel"
        assert zapis.dph_treatment == DphTreatment.BEZ_DPH
        assert zapis.kv_dph_sekcia == KvDphSekcia.ZIADNA
        assert len(zapis.riadky) == 2

        md_112 = [r for r in zapis.riadky if r.ucet == "112"]
        assert md_112[0].suma == Decimal("800.00")


# ===========================================================================
# 12. Dovoz z tretej krajiny
# ===========================================================================

class TestDovozTretiaKrajina:
    """Dovoz tovaru z tretej krajiny s clom."""

    def test_zakladny(self):
        """Dovoz: základ dane (colná hodnota + clo) = 5250, DPH 23 % = 1207.50.
        MD 131: 5250, MD 343: 1207.50, D 321: 5250, D 379: 1207.50.
        """
        t = Transakcia(
            smer=SmerTransakcie.NAKUP,
            typ_plnenia=TypPlnenia.TOVAR,
            krajina_dodavatela=KrajinaDodavatela.TRETIA_KRAJINA,
            platitel_dph_kupujuci=True,
            zaklad_dane=Decimal("5250"),  # colná hodnota + clo
            sadzba_dane=Decimal("23"),
        )
        zapis = zauctuj(t)

        assert zapis.je_vyvazeny
        assert zapis.pravidlo_id == "dovoz_tovar_tretia_krajina"
        assert zapis.dph_treatment == DphTreatment.VSTUPNA_DAN
        assert zapis.kv_dph_sekcia == KvDphSekcia.B2

        md_131 = [r for r in zapis.riadky if r.ucet == "131"]
        assert md_131[0].suma == Decimal("5250.00")

        md_343 = [r for r in zapis.riadky if r.ucet == "343"]
        assert md_343[0].suma == Decimal("1207.50")


# ===========================================================================
# 13. Predaj tovaru do EÚ — oslobodenie
# ===========================================================================

class TestPredajEU:
    """Predaj tovaru do iného členského štátu EÚ."""

    def test_oslobodenie(self):
        """Oslobodené dodanie do EÚ: základ 4000, COGS 3000, žiadna DPH."""
        t = Transakcia(
            smer=SmerTransakcie.PREDAJ,
            typ_plnenia=TypPlnenia.TOVAR,
            krajina_dodavatela=KrajinaDodavatela.EU,
            platitel_dph_dodavatel=True,
            zaklad_dane=Decimal("4000"),
            nadobudacia_cena=Decimal("3000"),
        )
        zapis = zauctuj(t)

        assert zapis.je_vyvazeny
        assert zapis.pravidlo_id == "predaj_tovaru_eu"
        assert zapis.dph_treatment == DphTreatment.OSLOBODENIE_S_ODPOCTOM
        assert zapis.kv_dph_sekcia == KvDphSekcia.A1

        # No DPH line
        ucty_343 = [r for r in zapis.riadky if r.ucet == "343"]
        assert len(ucty_343) == 0

        # Revenue
        d_604 = [r for r in zapis.riadky if r.ucet == "604"]
        assert d_604[0].suma == Decimal("4000.00")


# ===========================================================================
# 14. Vývoz mimo EÚ
# ===========================================================================

class TestVyvoz:
    """Vývoz tovaru mimo EÚ."""

    def test_oslobodenie(self):
        """Vývoz: základ 6000, COGS 4500, žiadna DPH, žiadna KV DPH."""
        t = Transakcia(
            smer=SmerTransakcie.PREDAJ,
            typ_plnenia=TypPlnenia.TOVAR,
            krajina_dodavatela=KrajinaDodavatela.TRETIA_KRAJINA,
            platitel_dph_dodavatel=True,
            zaklad_dane=Decimal("6000"),
            nadobudacia_cena=Decimal("4500"),
        )
        zapis = zauctuj(t)

        assert zapis.je_vyvazeny
        assert zapis.pravidlo_id == "vyvoz_tovaru"
        assert zapis.dph_treatment == DphTreatment.OSLOBODENIE_S_ODPOCTOM
        assert zapis.kv_dph_sekcia == KvDphSekcia.ZIADNA


# ===========================================================================
# 15. Tuzemský prenos — stavebné práce
# ===========================================================================

class TestPrenosStavebne:
    """Tuzemský prenos daňovej povinnosti — stavebné práce."""

    def test_samozdanenie(self):
        """Stavebné práce: základ 10000, DPH 2300 (samozdanenie)."""
        t = Transakcia(
            smer=SmerTransakcie.NAKUP,
            typ_plnenia=TypPlnenia.SLUZBA,
            krajina_dodavatela=KrajinaDodavatela.SK,
            platitel_dph_kupujuci=True,
            platitel_dph_dodavatel=True,
            tuzemsky_prenos=True,
            zaklad_dane=Decimal("10000"),
            sadzba_dane=Decimal("23"),
        )
        zapis = zauctuj(t)

        assert zapis.je_vyvazeny
        assert zapis.pravidlo_id == "prenos_stavebne_prace"
        assert zapis.dph_treatment == DphTreatment.PRENOS_DANOVEJ_POVINNOSTI
        assert zapis.kv_dph_sekcia == KvDphSekcia.A2

        # Net DPH effect = 0 (MD 343 = D 343)
        md_343 = sum(r.suma for r in zapis.riadky if r.ucet == "343" and r.strana == StranaUctu.MA_DAT)
        d_343 = sum(r.suma for r in zapis.riadky if r.ucet == "343" and r.strana == StranaUctu.DAL)
        assert md_343 == d_343 == Decimal("2300.00")


# ===========================================================================
# 17. Faktúra za energie
# ===========================================================================

class TestNakupEnergie:
    """Faktúra za energie."""

    def test_zakladny(self):
        """Elektrina: základ 400, DPH 92, celkom 492."""
        t = Transakcia(
            smer=SmerTransakcie.NAKUP,
            typ_plnenia=TypPlnenia.ENERGIA,
            krajina_dodavatela=KrajinaDodavatela.SK,
            platitel_dph_kupujuci=True,
            platitel_dph_dodavatel=True,
            zaklad_dane=Decimal("400"),
            sadzba_dane=Decimal("23"),
        )
        zapis = zauctuj(t)

        assert zapis.je_vyvazeny
        assert zapis.pravidlo_id == "nakup_energie"
        assert zapis.kv_dph_sekcia == KvDphSekcia.B2

        md_502 = [r for r in zapis.riadky if r.ucet == "502"]
        assert md_502[0].suma == Decimal("400.00")


# ===========================================================================
# 18. Bankové poplatky
# ===========================================================================

class TestBankovePoplatky:
    """Bankové poplatky — oslobodené od DPH."""

    def test_zakladny(self):
        """Bankový poplatok 15 EUR, žiadna DPH."""
        t = Transakcia(
            smer=SmerTransakcie.NAKUP,
            typ_plnenia=TypPlnenia.SLUZBA,
            krajina_dodavatela=KrajinaDodavatela.SK,
            platitel_dph_kupujuci=True,
            forma_uhrady="banka",
            celkova_suma=Decimal("15"),
        )
        zapis = zauctuj(t)

        assert zapis.je_vyvazeny
        assert zapis.pravidlo_id == "bankove_poplatky"
        assert zapis.dph_treatment == DphTreatment.OSLOBODENIE_BEZ_ODPOCTU
        assert zapis.kv_dph_sekcia == KvDphSekcia.ZIADNA

        md_568 = [r for r in zapis.riadky if r.ucet == "568"]
        assert md_568[0].suma == Decimal("15.00")

        d_221 = [r for r in zapis.riadky if r.ucet == "221"]
        assert d_221[0].suma == Decimal("15.00")


# ===========================================================================
# 19. Hotovostný predaj cez e-kasu
# ===========================================================================

class TestHotovostnyPredaj:
    """Hotovostný predaj cez e-kasu — D.1 KV DPH."""

    def test_zakladny(self):
        """Predaj za hotovosť: základ 100, DPH 23, celkom 123."""
        t = Transakcia(
            smer=SmerTransakcie.PREDAJ,
            typ_plnenia=TypPlnenia.TOVAR,
            krajina_dodavatela=KrajinaDodavatela.SK,
            platitel_dph_dodavatel=True,
            forma_uhrady="hotovost",
            zaklad_dane=Decimal("100"),
            sadzba_dane=Decimal("23"),
        )
        zapis = zauctuj(t)

        assert zapis.je_vyvazeny
        assert zapis.pravidlo_id == "hotovostny_predaj_ekasa"
        assert zapis.kv_dph_sekcia == KvDphSekcia.D1

        md_211 = [r for r in zapis.riadky if r.ucet == "211"]
        assert md_211[0].suma == Decimal("123.00")


# ===========================================================================
# 20. Cestovné náhrady
# ===========================================================================

class TestCestovneNahrady:
    """Cestovné náhrady zamestnancom."""

    def test_zakladny(self):
        """Cestovné 250 EUR, žiadna DPH."""
        t = Transakcia(
            smer=SmerTransakcie.NAKUP,
            typ_plnenia=TypPlnenia.SLUZBA,
            krajina_dodavatela=KrajinaDodavatela.SK,
            celkova_suma=Decimal("250"),
        )
        # Filter to cestovne_nahrady explicitly (low priority, would match others)
        pravidla_cestovne = [p for p in VSETKY_PRAVIDLA if p.id == "cestovne_nahrady"]
        zapis = zauctuj(t, pravidla_cestovne)

        assert zapis.je_vyvazeny
        assert zapis.pravidlo_id == "cestovne_nahrady"
        assert zapis.dph_treatment == DphTreatment.BEZ_DPH
        assert zapis.kv_dph_sekcia == KvDphSekcia.ZIADNA

        md_512 = [r for r in zapis.riadky if r.ucet == "512"]
        assert md_512[0].suma == Decimal("250.00")

        d_333 = [r for r in zapis.riadky if r.ucet == "333"]
        assert d_333[0].suma == Decimal("250.00")
