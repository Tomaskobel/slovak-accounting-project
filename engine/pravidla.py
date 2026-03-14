"""
Pravidlá účtovania — the 10 core s.r.o. booking rules encoded as declarative objects.

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
]
