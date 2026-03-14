"""
Pravidlá účtovania — 24 s.r.o. booking rules encoded as declarative objects.

Each rule maps conditions → posting lines + DPH treatment + KV DPH section.
Extracted from Postupy účtovania, DPH law, and practical examples.
"""

from engine.schema import (
    Pravidlo, Podmienky, RiadokZapisu,
    SmerTransakcie, TypPlnenia, KrajinaDodavatela,
    DphTreatment, KvDphSekcia, StranaUctu, VzorecSumy,
)


# ---------------------------------------------------------------------------
# 1. Nákup materiálu — tuzemsko, platiteľ DPH, metóda A
# ---------------------------------------------------------------------------
NAKUP_MATERIALU_TUZEMSKO = Pravidlo(
    id="nakup_materialu_tuzemsko_a",
    nazov="Nákup materiálu od tuzemského dodávateľa (metóda A)",
    name_en="Purchase of material from domestic supplier (perpetual inventory)",
    podmienky=Podmienky(
        smer=SmerTransakcie.NAKUP,
        typ_plnenia=TypPlnenia.MATERIAL,
        krajina_dodavatela=KrajinaDodavatela.SK,
        platitel_dph_kupujuci=True,
        platitel_dph_dodavatel=True,
        metoda_zasob="A",
    ),
    riadky=(
        RiadokZapisu("112", StranaUctu.MA_DAT, VzorecSumy.ZAKLAD_DANE, "Materiál na sklade"),
        RiadokZapisu("343", StranaUctu.MA_DAT, VzorecSumy.DAN, "DPH — vstupná daň"),
        RiadokZapisu("321", StranaUctu.DAL, VzorecSumy.CELKOVA_VYSKA, "Dodávatelia"),
    ),
    dph_treatment=DphTreatment.VSTUPNA_DAN,
    sadzba_dane_id="sadzba_dane_23",
    kv_dph_sekcia=KvDphSekcia.B2,
    povinne_vstupy=("datum_faktury", "dodavatel_ico_dph", "zaklad_dane", "sadzba_dane"),
    pravny_zdroj="Postupy účtovania § 30-32, DPH § 49",
    priorita=110,
    dovera="high",
)

# ---------------------------------------------------------------------------
# 1b. Nákup materiálu — tuzemsko, platiteľ DPH, metóda B
# ---------------------------------------------------------------------------
NAKUP_MATERIALU_TUZEMSKO_B = Pravidlo(
    id="nakup_materialu_tuzemsko_b",
    nazov="Nákup materiálu od tuzemského dodávateľa (metóda B — priama spotreba)",
    name_en="Purchase of material from domestic supplier (periodic inventory)",
    podmienky=Podmienky(
        smer=SmerTransakcie.NAKUP,
        typ_plnenia=TypPlnenia.MATERIAL,
        krajina_dodavatela=KrajinaDodavatela.SK,
        platitel_dph_kupujuci=True,
        platitel_dph_dodavatel=True,
        metoda_zasob="B",
    ),
    riadky=(
        RiadokZapisu("501", StranaUctu.MA_DAT, VzorecSumy.ZAKLAD_DANE, "Spotreba materiálu"),
        RiadokZapisu("343", StranaUctu.MA_DAT, VzorecSumy.DAN, "DPH — vstupná daň"),
        RiadokZapisu("321", StranaUctu.DAL, VzorecSumy.CELKOVA_VYSKA, "Dodávatelia"),
    ),
    dph_treatment=DphTreatment.VSTUPNA_DAN,
    sadzba_dane_id="sadzba_dane_23",
    kv_dph_sekcia=KvDphSekcia.B2,
    povinne_vstupy=("datum_faktury", "dodavatel_ico_dph", "zaklad_dane", "sadzba_dane"),
    pravny_zdroj="Postupy účtovania § 30-32, DPH § 49",
    priorita=110,
    dovera="high",
)

# ---------------------------------------------------------------------------
# 2. Nákup služieb — tuzemsko
# ---------------------------------------------------------------------------
NAKUP_SLUZIEB_TUZEMSKO = Pravidlo(
    id="nakup_sluzieb_tuzemsko",
    nazov="Nákup služieb od tuzemského dodávateľa",
    name_en="Purchase of services from domestic supplier",
    podmienky=Podmienky(
        smer=SmerTransakcie.NAKUP,
        typ_plnenia=TypPlnenia.SLUZBA,
        krajina_dodavatela=KrajinaDodavatela.SK,
        platitel_dph_kupujuci=True,
        platitel_dph_dodavatel=True,
    ),
    riadky=(
        RiadokZapisu("518", StranaUctu.MA_DAT, VzorecSumy.ZAKLAD_DANE, "Ostatné služby"),
        RiadokZapisu("343", StranaUctu.MA_DAT, VzorecSumy.DAN, "DPH — vstupná daň"),
        RiadokZapisu("321", StranaUctu.DAL, VzorecSumy.CELKOVA_VYSKA, "Dodávatelia"),
    ),
    dph_treatment=DphTreatment.VSTUPNA_DAN,
    sadzba_dane_id="sadzba_dane_23",
    kv_dph_sekcia=KvDphSekcia.B2,
    povinne_vstupy=("datum_faktury", "dodavatel_ico_dph", "zaklad_dane", "sadzba_dane", "popis_sluzby"),
    pravny_zdroj="Postupy účtovania § 47, DPH § 49",
    priorita=100,
    dovera="high",
)

# ---------------------------------------------------------------------------
# 3. Predaj tovaru — tuzemsko
# ---------------------------------------------------------------------------
PREDAJ_TOVARU_TUZEMSKO = Pravidlo(
    id="predaj_tovaru_tuzemsko",
    nazov="Predaj tovaru tuzemskému odberateľovi",
    name_en="Sale of goods to domestic customer",
    podmienky=Podmienky(
        smer=SmerTransakcie.PREDAJ,
        typ_plnenia=TypPlnenia.TOVAR,
        krajina_dodavatela=KrajinaDodavatela.SK,
        platitel_dph_kupujuci=None,  # Any — both VAT and non-VAT customers
        platitel_dph_dodavatel=True,
    ),
    riadky=(
        RiadokZapisu("311", StranaUctu.MA_DAT, VzorecSumy.CELKOVA_VYSKA, "Odberatelia"),
        RiadokZapisu("604", StranaUctu.DAL, VzorecSumy.ZAKLAD_DANE, "Tržby za tovar"),
        RiadokZapisu("343", StranaUctu.DAL, VzorecSumy.DAN, "DPH — výstupná daň"),
        RiadokZapisu("504", StranaUctu.MA_DAT, VzorecSumy.NADOBUDACIA_CENA, "Predaný tovar (COGS)"),
        RiadokZapisu("132", StranaUctu.DAL, VzorecSumy.NADOBUDACIA_CENA, "Tovar na sklade"),
    ),
    dph_treatment=DphTreatment.VYSTUPNA_DAN,
    sadzba_dane_id="sadzba_dane_23",
    kv_dph_sekcia=KvDphSekcia.A1,
    povinne_vstupy=("datum_dodania", "odberatel_nazov", "zaklad_dane", "sadzba_dane", "nadobudacia_cena"),
    pravny_zdroj="Postupy účtovania § 35-37, DPH § 8, § 19",
    priorita=100,
    dovera="high",
)

# ---------------------------------------------------------------------------
# 4. Predaj služieb — tuzemsko
# ---------------------------------------------------------------------------
PREDAJ_SLUZIEB_TUZEMSKO = Pravidlo(
    id="predaj_sluzieb_tuzemsko",
    nazov="Predaj služieb tuzemskému odberateľovi",
    name_en="Sale of services to domestic customer",
    podmienky=Podmienky(
        smer=SmerTransakcie.PREDAJ,
        typ_plnenia=TypPlnenia.SLUZBA,
        krajina_dodavatela=KrajinaDodavatela.SK,
        platitel_dph_dodavatel=True,
    ),
    riadky=(
        RiadokZapisu("311", StranaUctu.MA_DAT, VzorecSumy.CELKOVA_VYSKA, "Odberatelia"),
        RiadokZapisu("602", StranaUctu.DAL, VzorecSumy.ZAKLAD_DANE, "Tržby za služby"),
        RiadokZapisu("343", StranaUctu.DAL, VzorecSumy.DAN, "DPH — výstupná daň"),
    ),
    dph_treatment=DphTreatment.VYSTUPNA_DAN,
    sadzba_dane_id="sadzba_dane_23",
    kv_dph_sekcia=KvDphSekcia.A1,
    povinne_vstupy=("datum_dodania", "odberatel_nazov", "zaklad_dane", "sadzba_dane", "popis_sluzby"),
    pravny_zdroj="Postupy účtovania § 602, DPH § 9, § 15, § 27",
    priorita=100,
    dovera="high",
)

# ---------------------------------------------------------------------------
# 5. Nákup tovaru z EÚ — nadobudnutie, samozdanenie
# ---------------------------------------------------------------------------
NAKUP_TOVARU_EU = Pravidlo(
    id="nadobudnutie_tovaru_eu",
    nazov="Nadobudnutie tovaru z iného členského štátu EÚ",
    name_en="Intra-community acquisition of goods from EU",
    podmienky=Podmienky(
        smer=SmerTransakcie.NAKUP,
        typ_plnenia=TypPlnenia.TOVAR,
        krajina_dodavatela=KrajinaDodavatela.EU,
        platitel_dph_kupujuci=True,
        platitel_dph_dodavatel=True,
    ),
    riadky=(
        RiadokZapisu("112", StranaUctu.MA_DAT, VzorecSumy.ZAKLAD_DANE, "Materiál/tovar na sklade"),
        RiadokZapisu("321", StranaUctu.DAL, VzorecSumy.ZAKLAD_DANE, "Dodávatelia (bez DPH)"),
        RiadokZapisu("349", StranaUctu.MA_DAT, VzorecSumy.DAN, "Samozdanenie — výstupná daň"),
        RiadokZapisu("343", StranaUctu.DAL, VzorecSumy.DAN, "Samozdanenie — vstupná daň (odpočet)"),
    ),
    dph_treatment=DphTreatment.SAMOZDANENIE,
    sadzba_dane_id="sadzba_dane_23",
    kv_dph_sekcia=KvDphSekcia.B1,
    povinne_vstupy=("datum_faktury", "dodavatel_ico_dph_eu", "krajina_dodavatela", "zaklad_dane"),
    pravny_zdroj="DPH § 11, § 20, § 69 ods. 3",
    priorita=120,
    dovera="high",
)

# ---------------------------------------------------------------------------
# 6. Prijatie služby z EÚ — prenos daňovej povinnosti
# ---------------------------------------------------------------------------
PRIJATIE_SLUZBY_EU = Pravidlo(
    id="prijatie_sluzby_eu",
    nazov="Prijatie služby z EÚ s prenosom daňovej povinnosti",
    name_en="Receipt of service from EU with reverse charge",
    podmienky=Podmienky(
        smer=SmerTransakcie.NAKUP,
        typ_plnenia=TypPlnenia.SLUZBA,
        krajina_dodavatela=KrajinaDodavatela.EU,
        platitel_dph_kupujuci=True,
    ),
    riadky=(
        RiadokZapisu("518", StranaUctu.MA_DAT, VzorecSumy.ZAKLAD_DANE, "Ostatné služby"),
        RiadokZapisu("321", StranaUctu.DAL, VzorecSumy.ZAKLAD_DANE, "Dodávatelia (bez DPH)"),
        RiadokZapisu("349", StranaUctu.MA_DAT, VzorecSumy.DAN, "Samozdanenie — výstupná daň"),
        RiadokZapisu("343", StranaUctu.DAL, VzorecSumy.DAN, "Samozdanenie — vstupná daň (odpočet)"),
    ),
    dph_treatment=DphTreatment.SAMOZDANENIE,
    sadzba_dane_id="sadzba_dane_23",
    kv_dph_sekcia=KvDphSekcia.B1,
    povinne_vstupy=("datum_faktury", "dodavatel_ico_dph_eu", "krajina_dodavatela", "zaklad_dane", "popis_sluzby"),
    pravny_zdroj="DPH § 15, § 69 ods. 3",
    priorita=120,
    dovera="high",
)

# ---------------------------------------------------------------------------
# 7. Nákup DHM — tuzemsko (step 1: receipt of invoice)
# ---------------------------------------------------------------------------
NAKUP_DHM_TUZEMSKO_KROK1 = Pravidlo(
    id="nakup_dhm_tuzemsko_krok1",
    nazov="Nákup dlhodobého hmotného majetku — prijatie faktúry",
    name_en="Purchase of fixed asset — invoice receipt (step 1)",
    podmienky=Podmienky(
        smer=SmerTransakcie.NAKUP,
        typ_plnenia=TypPlnenia.DLHODOBY_MAJETOK,
        krajina_dodavatela=KrajinaDodavatela.SK,
        platitel_dph_kupujuci=True,
        platitel_dph_dodavatel=True,
    ),
    riadky=(
        RiadokZapisu("042", StranaUctu.MA_DAT, VzorecSumy.ZAKLAD_DANE, "Obstaranie DHM"),
        RiadokZapisu("343", StranaUctu.MA_DAT, VzorecSumy.DAN, "DPH — vstupná daň"),
        RiadokZapisu("321", StranaUctu.DAL, VzorecSumy.CELKOVA_VYSKA, "Dodávatelia"),
    ),
    dph_treatment=DphTreatment.VSTUPNA_DAN,
    sadzba_dane_id="sadzba_dane_23",
    kv_dph_sekcia=KvDphSekcia.B2,
    povinne_vstupy=("datum_faktury", "dodavatel_ico_dph", "zaklad_dane", "sadzba_dane", "popis_majetku"),
    pravny_zdroj="Postupy účtovania § 32-36, DPH § 49",
    priorita=110,
    krok=1,
    celkovo_krokov=2,
    dovera="high",
)

# ---------------------------------------------------------------------------
# 7b. Nákup DHM — aktivácia (step 2: put into use)
# ---------------------------------------------------------------------------
NAKUP_DHM_TUZEMSKO_KROK2 = Pravidlo(
    id="nakup_dhm_tuzemsko_krok2",
    nazov="Nákup dlhodobého hmotného majetku — zaradenie do používania",
    name_en="Purchase of fixed asset — activation (step 2)",
    podmienky=Podmienky(
        smer=SmerTransakcie.NAKUP,
        typ_plnenia=TypPlnenia.DLHODOBY_MAJETOK,
        krajina_dodavatela=KrajinaDodavatela.SK,
    ),
    riadky=(
        RiadokZapisu("022", StranaUctu.MA_DAT, VzorecSumy.ZAKLAD_DANE, "Samostatné hnuteľné veci"),
        RiadokZapisu("042", StranaUctu.DAL, VzorecSumy.ZAKLAD_DANE, "Obstaranie DHM (vyúčtovanie)"),
    ),
    dph_treatment=DphTreatment.BEZ_DPH,
    kv_dph_sekcia=KvDphSekcia.ZIADNA,
    povinne_vstupy=("datum_zaradenia", "obstarávacia_cena"),
    pravny_zdroj="Postupy účtovania § 32-36",
    priorita=110,
    krok=2,
    celkovo_krokov=2,
    dovera="high",
)

# ---------------------------------------------------------------------------
# 8. Dobropis prijatý
# ---------------------------------------------------------------------------
DOBROPIS_PRIJATY = Pravidlo(
    id="dobropis_prijaty",
    nazov="Dobropis od dodávateľa (zníženie nákupu)",
    name_en="Credit note received from supplier",
    podmienky=Podmienky(
        smer=SmerTransakcie.OPRAVA,
        typ_plnenia=None,  # Can be any type — material, services, etc.
        krajina_dodavatela=KrajinaDodavatela.SK,
        platitel_dph_kupujuci=True,
    ),
    riadky=(
        RiadokZapisu("321", StranaUctu.MA_DAT, VzorecSumy.ZAKLAD_DANE, "Dodávatelia (zníženie záväzku)"),
        RiadokZapisu("501", StranaUctu.DAL, VzorecSumy.ZAKLAD_DANE, "Spotreba materiálu (zníženie nákladu)"),
        RiadokZapisu("321", StranaUctu.MA_DAT, VzorecSumy.DAN, "Dodávatelia (DPH časť)"),
        RiadokZapisu("343", StranaUctu.DAL, VzorecSumy.DAN, "DPH — zníženie odpočtu"),
    ),
    dph_treatment=DphTreatment.OPRAVA_VSTUPNEJ,
    sadzba_dane_id=None,  # Rate from original invoice
    kv_dph_sekcia=KvDphSekcia.C2,
    povinne_vstupy=("datum_dobropisu", "cislo_povodnej_faktury", "dodavatel_ico_dph", "zaklad_dane", "sadzba_dane"),
    pravny_zdroj="DPH § 25, § 53",
    priorita=100,
    dovera="high",
)

# ---------------------------------------------------------------------------
# 9. Dobropis vydaný
# ---------------------------------------------------------------------------
DOBROPIS_VYDANY = Pravidlo(
    id="dobropis_vydany",
    nazov="Dobropis vydaný odberateľovi (zníženie predaja)",
    name_en="Credit note issued to customer",
    podmienky=Podmienky(
        smer=SmerTransakcie.OPRAVA,
        typ_plnenia=TypPlnenia.TOVAR,
        krajina_dodavatela=KrajinaDodavatela.SK,
        platitel_dph_dodavatel=True,
    ),
    riadky=(
        RiadokZapisu("604", StranaUctu.MA_DAT, VzorecSumy.ZAKLAD_DANE, "Tržby za tovar (zníženie výnosu)"),
        RiadokZapisu("311", StranaUctu.DAL, VzorecSumy.ZAKLAD_DANE, "Odberatelia (zníženie pohľadávky)"),
        RiadokZapisu("343", StranaUctu.MA_DAT, VzorecSumy.DAN, "DPH — zníženie výstupnej dane"),
        RiadokZapisu("311", StranaUctu.DAL, VzorecSumy.DAN, "Odberatelia (DPH časť)"),
    ),
    dph_treatment=DphTreatment.OPRAVA_VYSTUPNEJ,
    sadzba_dane_id=None,  # Rate from original invoice
    kv_dph_sekcia=KvDphSekcia.C1,
    povinne_vstupy=("datum_dobropisu", "cislo_povodnej_faktury", "odberatel_ico_dph", "zaklad_dane", "sadzba_dane"),
    pravny_zdroj="DPH § 25, § 53",
    priorita=100,
    dovera="high",
)

# ---------------------------------------------------------------------------
# 10. Preddavok s DPH — krok 1: platba preddavku
# ---------------------------------------------------------------------------
PREDDAVOK_KROK1 = Pravidlo(
    id="preddavok_platba_krok1",
    nazov="Preddavok — platba dodávateľovi",
    name_en="Advance payment to supplier (step 1)",
    podmienky=Podmienky(
        smer=SmerTransakcie.PREDDAVOK,
        krajina_dodavatela=KrajinaDodavatela.SK,
        platitel_dph_kupujuci=True,
        forma_uhrady="preddavok",
    ),
    riadky=(
        RiadokZapisu("314", StranaUctu.MA_DAT, VzorecSumy.PREDDAVKOVA_SUMA, "Poskytnuté preddavky"),
        RiadokZapisu("221", StranaUctu.DAL, VzorecSumy.PREDDAVKOVA_SUMA, "Bankové účty"),
    ),
    dph_treatment=DphTreatment.BEZ_DPH,
    kv_dph_sekcia=KvDphSekcia.ZIADNA,
    povinne_vstupy=("datum_platby", "suma_preddavku", "dodavatel_nazov"),
    pravny_zdroj="Postupy účtovania § 314",
    priorita=100,
    krok=1,
    celkovo_krokov=3,
    dovera="high",
)

# ---------------------------------------------------------------------------
# 10b. Preddavok s DPH — krok 2: prijatie daňového dokladu
# ---------------------------------------------------------------------------
PREDDAVOK_KROK2 = Pravidlo(
    id="preddavok_danovy_doklad_krok2",
    nazov="Preddavok — prijatie daňového dokladu (odpočet DPH)",
    name_en="Advance payment — tax document receipt (step 2)",
    podmienky=Podmienky(
        smer=SmerTransakcie.PREDDAVOK,
        krajina_dodavatela=KrajinaDodavatela.SK,
        platitel_dph_kupujuci=True,
    ),
    riadky=(
        RiadokZapisu("343", StranaUctu.MA_DAT, VzorecSumy.DAN, "DPH — odpočet z preddavku"),
        RiadokZapisu("314", StranaUctu.DAL, VzorecSumy.DAN, "Poskytnuté preddavky (DPH časť)"),
    ),
    dph_treatment=DphTreatment.PREDDAVKOVA,
    sadzba_dane_id="sadzba_dane_23",
    kv_dph_sekcia=KvDphSekcia.B2,
    povinne_vstupy=("datum_danoveho_dokladu", "dodavatel_ico_dph", "zaklad_dane_preddavku", "sadzba_dane"),
    pravny_zdroj="DPH § 19 ods. 2, § 49",
    priorita=100,
    krok=2,
    celkovo_krokov=3,
    dovera="high",
)

# ---------------------------------------------------------------------------
# 10c. Preddavok s DPH — krok 3: vyúčtovacia faktúra
# ---------------------------------------------------------------------------
PREDDAVOK_KROK3 = Pravidlo(
    id="preddavok_vyuctovanie_krok3",
    nazov="Preddavok — vyúčtovacia faktúra (vysporiadanie)",
    name_en="Advance payment — final invoice settlement (step 3)",
    podmienky=Podmienky(
        smer=SmerTransakcie.PREDDAVOK,
        krajina_dodavatela=KrajinaDodavatela.SK,
        platitel_dph_kupujuci=True,
    ),
    riadky=(
        RiadokZapisu("112", StranaUctu.MA_DAT, VzorecSumy.ZAKLAD_DANE, "Materiál/tovar (plná suma)"),
        RiadokZapisu("343", StranaUctu.MA_DAT, VzorecSumy.DAN, "DPH — plná faktúra"),
        RiadokZapisu("321", StranaUctu.DAL, VzorecSumy.CELKOVA_VYSKA, "Dodávatelia (plná faktúra)"),
    ),
    dph_treatment=DphTreatment.VSTUPNA_DAN,
    sadzba_dane_id="sadzba_dane_23",
    kv_dph_sekcia=KvDphSekcia.B2,
    povinne_vstupy=("datum_faktury", "dodavatel_ico_dph", "zaklad_dane", "sadzba_dane"),
    pravny_zdroj="DPH § 19, § 49",
    priorita=100,
    krok=3,
    celkovo_krokov=3,
    dovera="high",
    poznamky="Po tomto kroku sa vysporiadajú preddavky: MD 321 / D 314 + MD 321 / D 343 (vrátenie DPH z preddavku)",
)


# ---------------------------------------------------------------------------
# 11. Nákup materiálu od neplatiteľa DPH
# ---------------------------------------------------------------------------
NAKUP_MATERIALU_NEPLATITEL = Pravidlo(
    id="nakup_materialu_neplatitel",
    nazov="Nákup materiálu od tuzemského neplatiteľa DPH",
    name_en="Purchase of material from domestic non-VAT-payer",
    podmienky=Podmienky(
        smer=SmerTransakcie.NAKUP,
        typ_plnenia=TypPlnenia.MATERIAL,
        krajina_dodavatela=KrajinaDodavatela.SK,
        platitel_dph_kupujuci=True,
        platitel_dph_dodavatel=False,
        metoda_zasob="A",
    ),
    riadky=(
        RiadokZapisu("112", StranaUctu.MA_DAT, VzorecSumy.CELKOVA_VYSKA, "Materiál na sklade"),
        RiadokZapisu("321", StranaUctu.DAL, VzorecSumy.CELKOVA_VYSKA, "Dodávatelia"),
    ),
    dph_treatment=DphTreatment.BEZ_DPH,
    kv_dph_sekcia=KvDphSekcia.ZIADNA,
    povinne_vstupy=("datum_faktury", "dodavatel_nazov", "celkova_suma"),
    pravny_zdroj="Postupy účtovania § 30-32",
    priorita=115,
    dovera="high",
    poznamky="Dodávateľ nie je platiteľ DPH — faktúra bez DPH, celá suma do obstarávacej ceny",
)

# ---------------------------------------------------------------------------
# 12. Dovoz tovaru z tretej krajiny (s clom)
# ---------------------------------------------------------------------------
DOVOZ_TOVAR_TRETIA_KRAJINA = Pravidlo(
    id="dovoz_tovar_tretia_krajina",
    nazov="Dovoz tovaru z tretej krajiny (s clom a DPH na vstupe)",
    name_en="Import of goods from non-EU country (with customs duty)",
    podmienky=Podmienky(
        smer=SmerTransakcie.NAKUP,
        typ_plnenia=TypPlnenia.TOVAR,
        krajina_dodavatela=KrajinaDodavatela.TRETIA_KRAJINA,
        platitel_dph_kupujuci=True,
    ),
    riadky=(
        RiadokZapisu("131", StranaUctu.MA_DAT, VzorecSumy.ZAKLAD_DANE, "Tovar na sklade (colná hodnota + clo)"),
        RiadokZapisu("343", StranaUctu.MA_DAT, VzorecSumy.DAN, "DPH — vstupná daň pri dovoze"),
        RiadokZapisu("321", StranaUctu.DAL, VzorecSumy.ZAKLAD_DANE, "Dodávatelia (zahraničný)"),
        RiadokZapisu("379", StranaUctu.DAL, VzorecSumy.DAN, "Iné záväzky (DPH colnému úradu)"),
    ),
    dph_treatment=DphTreatment.VSTUPNA_DAN,
    sadzba_dane_id="sadzba_dane_23",
    kv_dph_sekcia=KvDphSekcia.B2,
    povinne_vstupy=("datum_faktury", "colne_vyhlasenie", "zaklad_dane", "sadzba_dane"),
    pravny_zdroj="DPH § 12, § 20 ods. 1, § 49; Postupy účtovania § 35",
    priorita=120,
    dovera="high",
    poznamky="Základ dane = colná hodnota + clo + vedľajšie náklady (zadáva sa ako zaklad_dane). DPH platí dovozca cez colný úrad.",
)

# ---------------------------------------------------------------------------
# 13. Predaj tovaru do EÚ — oslobodenie od DPH
# ---------------------------------------------------------------------------
PREDAJ_TOVARU_EU = Pravidlo(
    id="predaj_tovaru_eu",
    nazov="Predaj tovaru do iného členského štátu EÚ (oslobodené)",
    name_en="Intra-community supply of goods to EU (exempt with deduction)",
    podmienky=Podmienky(
        smer=SmerTransakcie.PREDAJ,
        typ_plnenia=TypPlnenia.TOVAR,
        krajina_dodavatela=KrajinaDodavatela.EU,
        platitel_dph_dodavatel=True,
    ),
    riadky=(
        RiadokZapisu("311", StranaUctu.MA_DAT, VzorecSumy.ZAKLAD_DANE, "Odberatelia (EÚ)"),
        RiadokZapisu("604", StranaUctu.DAL, VzorecSumy.ZAKLAD_DANE, "Tržby za tovar"),
        RiadokZapisu("504", StranaUctu.MA_DAT, VzorecSumy.NADOBUDACIA_CENA, "Predaný tovar (COGS)"),
        RiadokZapisu("132", StranaUctu.DAL, VzorecSumy.NADOBUDACIA_CENA, "Tovar na sklade"),
    ),
    dph_treatment=DphTreatment.OSLOBODENIE_S_ODPOCTOM,
    kv_dph_sekcia=KvDphSekcia.A1,
    povinne_vstupy=("datum_dodania", "odberatel_ico_dph_eu", "krajina_odberatela", "zaklad_dane", "nadobudacia_cena"),
    pravny_zdroj="DPH § 43 ods. 1 — oslobodenie pri dodaní tovaru do IČŠ",
    priorita=120,
    dovera="high",
    poznamky="Bez DPH — oslobodené s právom na odpočet. Povinné uviesť v súhrnnom výkaze.",
)

# ---------------------------------------------------------------------------
# 14. Vývoz tovaru mimo EÚ
# ---------------------------------------------------------------------------
VYVOZ_TOVARU = Pravidlo(
    id="vyvoz_tovaru",
    nazov="Vývoz tovaru mimo EÚ (oslobodené)",
    name_en="Export of goods outside EU (exempt with deduction)",
    podmienky=Podmienky(
        smer=SmerTransakcie.PREDAJ,
        typ_plnenia=TypPlnenia.TOVAR,
        krajina_dodavatela=KrajinaDodavatela.TRETIA_KRAJINA,
        platitel_dph_dodavatel=True,
    ),
    riadky=(
        RiadokZapisu("311", StranaUctu.MA_DAT, VzorecSumy.ZAKLAD_DANE, "Odberatelia (zahraničný)"),
        RiadokZapisu("604", StranaUctu.DAL, VzorecSumy.ZAKLAD_DANE, "Tržby za tovar"),
        RiadokZapisu("504", StranaUctu.MA_DAT, VzorecSumy.NADOBUDACIA_CENA, "Predaný tovar (COGS)"),
        RiadokZapisu("132", StranaUctu.DAL, VzorecSumy.NADOBUDACIA_CENA, "Tovar na sklade"),
    ),
    dph_treatment=DphTreatment.OSLOBODENIE_S_ODPOCTOM,
    kv_dph_sekcia=KvDphSekcia.ZIADNA,
    povinne_vstupy=("datum_dodania", "odberatel_nazov", "krajina_odberatela", "zaklad_dane", "nadobudacia_cena", "colne_vyhlasenie"),
    pravny_zdroj="DPH § 47 — oslobodenie pri vývoze tovaru",
    priorita=120,
    dovera="high",
    poznamky="Vývoz potvrdený colným vyhlásením. Neuvádza sa v KV DPH.",
)

# ---------------------------------------------------------------------------
# 15. Tuzemský prenos daňovej povinnosti — stavebné práce (§ 69 ods. 12 písm. j)
# ---------------------------------------------------------------------------
PRENOS_STAVEBNE_PRACE = Pravidlo(
    id="prenos_stavebne_prace",
    nazov="Tuzemský prenos daňovej povinnosti — stavebné práce",
    name_en="Domestic reverse charge — construction services (§ 69/12/j)",
    podmienky=Podmienky(
        smer=SmerTransakcie.NAKUP,
        typ_plnenia=TypPlnenia.SLUZBA,
        krajina_dodavatela=KrajinaDodavatela.SK,
        platitel_dph_kupujuci=True,
        platitel_dph_dodavatel=True,
        tuzemsky_prenos=True,
    ),
    riadky=(
        RiadokZapisu("518", StranaUctu.MA_DAT, VzorecSumy.ZAKLAD_DANE, "Ostatné služby (stavebné práce)"),
        RiadokZapisu("343", StranaUctu.MA_DAT, VzorecSumy.DAN, "DPH — prenos, výstupná povinnosť"),
        RiadokZapisu("343", StranaUctu.DAL, VzorecSumy.DAN, "DPH — prenos, vstupný odpočet"),
        RiadokZapisu("321", StranaUctu.DAL, VzorecSumy.ZAKLAD_DANE, "Dodávatelia (bez DPH)"),
    ),
    dph_treatment=DphTreatment.PRENOS_DANOVEJ_POVINNOSTI,
    sadzba_dane_id="sadzba_dane_23",
    kv_dph_sekcia=KvDphSekcia.A2,
    povinne_vstupy=("datum_faktury", "dodavatel_ico_dph", "zaklad_dane", "sadzba_dane", "popis_stavebnych_prac"),
    pravny_zdroj="DPH § 69 ods. 12 písm. j) — stavebné práce sekcie F CPA",
    priorita=130,
    dovera="high",
    poznamky="Odberateľ platí daň. Dodávateľ fakturuje bez DPH. Odberateľ vykazuje v A.2 aj B.1 KV DPH.",
)

# ---------------------------------------------------------------------------
# 16. Tuzemský prenos daňovej povinnosti — tovar (§ 69 ods. 12) — elektronika >5000 EUR
# ---------------------------------------------------------------------------
PRENOS_ELEKTRONIKA = Pravidlo(
    id="prenos_elektronika",
    nazov="Tuzemský prenos daňovej povinnosti — tovar nad 5 000 EUR (elektronika a pod.)",
    name_en="Domestic reverse charge — goods above 5000 EUR (electronics etc.)",
    podmienky=Podmienky(
        smer=SmerTransakcie.NAKUP,
        typ_plnenia=TypPlnenia.TOVAR,
        krajina_dodavatela=KrajinaDodavatela.SK,
        platitel_dph_kupujuci=True,
        platitel_dph_dodavatel=True,
        tuzemsky_prenos=True,
    ),
    riadky=(
        RiadokZapisu("132", StranaUctu.MA_DAT, VzorecSumy.ZAKLAD_DANE, "Tovar na sklade"),
        RiadokZapisu("343", StranaUctu.MA_DAT, VzorecSumy.DAN, "DPH — prenos, výstupná povinnosť"),
        RiadokZapisu("343", StranaUctu.DAL, VzorecSumy.DAN, "DPH — prenos, vstupný odpočet"),
        RiadokZapisu("321", StranaUctu.DAL, VzorecSumy.ZAKLAD_DANE, "Dodávatelia (bez DPH)"),
    ),
    dph_treatment=DphTreatment.PRENOS_DANOVEJ_POVINNOSTI,
    sadzba_dane_id="sadzba_dane_23",
    kv_dph_sekcia=KvDphSekcia.A2,
    povinne_vstupy=("datum_faktury", "dodavatel_ico_dph", "zaklad_dane", "sadzba_dane"),
    pravny_zdroj="DPH § 69 ods. 12 písm. f), g), h), i) — integrované obvody, mobily, tablety, laptopy >5000 EUR",
    priorita=130,
    dovera="high",
    poznamky="Platí len ak základ dane na faktúre ≥ 5 000 EUR. Odberateľ platí daň.",
)

# ---------------------------------------------------------------------------
# 17. Faktúra za energie (elektrina, plyn, teplo, voda)
# ---------------------------------------------------------------------------
NAKUP_ENERGIE = Pravidlo(
    id="nakup_energie",
    nazov="Faktúra za energie (elektrina, plyn, teplo, voda)",
    name_en="Energy invoice (electricity, gas, heat, water)",
    podmienky=Podmienky(
        smer=SmerTransakcie.NAKUP,
        typ_plnenia=TypPlnenia.ENERGIA,
        krajina_dodavatela=KrajinaDodavatela.SK,
        platitel_dph_kupujuci=True,
        platitel_dph_dodavatel=True,
    ),
    riadky=(
        RiadokZapisu("502", StranaUctu.MA_DAT, VzorecSumy.ZAKLAD_DANE, "Spotreba energie"),
        RiadokZapisu("343", StranaUctu.MA_DAT, VzorecSumy.DAN, "DPH — vstupná daň"),
        RiadokZapisu("321", StranaUctu.DAL, VzorecSumy.CELKOVA_VYSKA, "Dodávatelia"),
    ),
    dph_treatment=DphTreatment.VSTUPNA_DAN,
    sadzba_dane_id="sadzba_dane_23",
    kv_dph_sekcia=KvDphSekcia.B2,
    povinne_vstupy=("datum_faktury", "dodavatel_ico_dph", "zaklad_dane", "sadzba_dane"),
    pravny_zdroj="Postupy účtovania § 47, DPH § 49; účet 502",
    priorita=100,
    dovera="high",
)

# ---------------------------------------------------------------------------
# 18. Bankové poplatky
# ---------------------------------------------------------------------------
BANKOVE_POPLATKY = Pravidlo(
    id="bankove_poplatky",
    nazov="Bankové poplatky (bez DPH)",
    name_en="Bank fees (no VAT)",
    podmienky=Podmienky(
        smer=SmerTransakcie.NAKUP,
        typ_plnenia=TypPlnenia.SLUZBA,
        krajina_dodavatela=KrajinaDodavatela.SK,
        platitel_dph_kupujuci=True,
        platitel_dph_dodavatel=None,
        forma_uhrady="banka",
    ),
    riadky=(
        RiadokZapisu("568", StranaUctu.MA_DAT, VzorecSumy.CELKOVA_VYSKA, "Ostatné finančné náklady"),
        RiadokZapisu("221", StranaUctu.DAL, VzorecSumy.CELKOVA_VYSKA, "Bankové účty"),
    ),
    dph_treatment=DphTreatment.OSLOBODENIE_BEZ_ODPOCTU,
    kv_dph_sekcia=KvDphSekcia.ZIADNA,
    povinne_vstupy=("datum_pohybu", "suma"),
    pravny_zdroj="DPH § 39 — oslobodené finančné služby; účet 568",
    priorita=110,
    dovera="high",
    poznamky="Bankové služby sú oslobodené od DPH podľa § 39. Nie je odpočet, nie je KV DPH.",
)

# ---------------------------------------------------------------------------
# 19. Hotovostný predaj cez e-kasu (D.1 KV DPH)
# ---------------------------------------------------------------------------
HOTOVOSTNY_PREDAJ_EKASA = Pravidlo(
    id="hotovostny_predaj_ekasa",
    nazov="Hotovostný predaj cez e-kasu",
    name_en="Cash sale via e-kasa (point of sale)",
    podmienky=Podmienky(
        smer=SmerTransakcie.PREDAJ,
        typ_plnenia=TypPlnenia.TOVAR,
        krajina_dodavatela=KrajinaDodavatela.SK,
        platitel_dph_dodavatel=True,
        forma_uhrady="hotovost",
    ),
    riadky=(
        RiadokZapisu("211", StranaUctu.MA_DAT, VzorecSumy.CELKOVA_VYSKA, "Pokladnica"),
        RiadokZapisu("604", StranaUctu.DAL, VzorecSumy.ZAKLAD_DANE, "Tržby za tovar"),
        RiadokZapisu("343", StranaUctu.DAL, VzorecSumy.DAN, "DPH — výstupná daň"),
    ),
    dph_treatment=DphTreatment.VYSTUPNA_DAN,
    sadzba_dane_id="sadzba_dane_23",
    kv_dph_sekcia=KvDphSekcia.D1,
    povinne_vstupy=("datum_predaja", "celkova_suma", "sadzba_dane"),
    pravny_zdroj="DPH § 8, § 71 ods. 1; Zákon 289/2008 Z.z. o e-kase",
    priorita=110,
    dovera="high",
    poznamky="Pokladničný doklad z e-kasy. Uvádza sa v D.1 KV DPH (súhrnne za obdobie).",
)

# ---------------------------------------------------------------------------
# 20. Cestovné náhrady (bez DPH)
# ---------------------------------------------------------------------------
CESTOVNE_NAHRADY = Pravidlo(
    id="cestovne_nahrady",
    nazov="Cestovné náhrady zamestnancom",
    name_en="Travel expense reimbursement to employees",
    podmienky=Podmienky(
        smer=SmerTransakcie.NAKUP,
        typ_plnenia=TypPlnenia.SLUZBA,
        krajina_dodavatela=KrajinaDodavatela.SK,
    ),
    riadky=(
        RiadokZapisu("512", StranaUctu.MA_DAT, VzorecSumy.CELKOVA_VYSKA, "Cestovné"),
        RiadokZapisu("333", StranaUctu.DAL, VzorecSumy.CELKOVA_VYSKA, "Ostatné záväzky voči zamestnancom"),
    ),
    dph_treatment=DphTreatment.BEZ_DPH,
    kv_dph_sekcia=KvDphSekcia.ZIADNA,
    povinne_vstupy=("datum_cesty", "zamestnanec", "suma", "ucel_cesty"),
    pravny_zdroj="Zákon 283/2002 Z.z. o cestovných náhradách; účet 512",
    priorita=90,
    dovera="high",
    poznamky="Cestovné náhrady nie sú predmetom DPH. Zahŕňa: diety, cestovné, ubytovanie.",
)


# ---------------------------------------------------------------------------
# Registry — all rules in one place
# ---------------------------------------------------------------------------
VSETKY_PRAVIDLA: list[Pravidlo] = [
    NAKUP_MATERIALU_TUZEMSKO,
    NAKUP_MATERIALU_TUZEMSKO_B,
    NAKUP_SLUZIEB_TUZEMSKO,
    PREDAJ_TOVARU_TUZEMSKO,
    PREDAJ_SLUZIEB_TUZEMSKO,
    NAKUP_TOVARU_EU,
    PRIJATIE_SLUZBY_EU,
    NAKUP_DHM_TUZEMSKO_KROK1,
    NAKUP_DHM_TUZEMSKO_KROK2,
    DOBROPIS_PRIJATY,
    DOBROPIS_VYDANY,
    PREDDAVOK_KROK1,
    PREDDAVOK_KROK2,
    PREDDAVOK_KROK3,
    NAKUP_MATERIALU_NEPLATITEL,
    DOVOZ_TOVAR_TRETIA_KRAJINA,
    PREDAJ_TOVARU_EU,
    VYVOZ_TOVARU,
    PRENOS_STAVEBNE_PRACE,
    PRENOS_ELEKTRONIKA,
    NAKUP_ENERGIE,
    BANKOVE_POPLATKY,
    HOTOVOSTNY_PREDAJ_EKASA,
    CESTOVNE_NAHRADY,
]
