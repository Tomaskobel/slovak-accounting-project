# Slovak Accounting — Regulatory Sources & Documentation

Complete inventory of all laws, regulations, technical specs, and practical guides needed for building Slovak double-entry accounting software.

---

## 1. CORE LAWS (slov-lex.sk)

### Accounting Law
| Document | URL | Coverage |
|----------|-----|----------|
| **Zákon č. 431/2002 Z.z. o účtovníctve** | [slov-lex.sk](https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/2002/431/) | Main accounting law — mandatory double-entry for all s.r.o. |
| **Opatrenie MF SR č. 23054/2002-92** (Postupy účtovania) | [mfsr.sk](https://www.mfsr.sk/sk/dane-cla-uctovnictvo/uctovnictvo-audit/uctovnictvo/legislativa-sr/opatrenia-oblasti-uctovnictva/uctovnictvo-podnikatelov/podvojne-uctovnictvo/postupy-uctovania/) | **THE critical document** — all booking rules + chart of accounts framework |
| Postupy účtovania (PDF, Feb 2025) | [financnasprava.sk](https://www.financnasprava.sk/_img/pfsedit/Dokumenty_PFS/Zverejnovanie_dok/Sprievodca/Postupy_uct/2025/2025.02.12_opatr_MFSR_23054_2002_92.pdf) | Current consolidated version |
| **Rámcová účtová osnova** (Chart of Accounts) | [slov-lex.sk (PDF)](https://static.slov-lex.sk/pdf/prilohy/SK/ZZ/2002/742/20021231_2871886-2.pdf) | 10-class account framework |

### Tax Laws
| Document | URL | Coverage |
|----------|-----|----------|
| **Zákon č. 222/2004 Z.z. o DPH** (VAT Act) | [slov-lex.sk](https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/2004/222/) | VAT rates, registration, deductions, reverse charge |
| DPH Law (PDF, Jan 2025) | [financnasprava.sk](https://www.financnasprava.sk/_img/pfsedit/Dokumenty_PFS/Zverejnovanie_dok/Sprievodca/Sprievodca_danami/2025/2025.01.28_zakon_DPH.pdf) | Current consolidated version |
| **Zákon č. 595/2003 Z.z. o dani z príjmov** (Income Tax) | [slov-lex.sk](https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/2003/595/) | Corporate tax, depreciation rules, deductions |
| **Zákon č. 513/1991 Zb. Obchodný zákonník** (Commercial Code) | [slov-lex.sk](https://www.slov-lex.sk/ezbierky/pravne-predpisy/SK/ZZ/1991/513/) | s.r.o. requirements, financial statement deadlines |

### Financial Statements Regulations
| Document | URL | Coverage |
|----------|-----|----------|
| **Opatrenie MF/13542/2023-36** | [slov-lex.sk (PDF)](https://static.slov-lex.sk/pdf/prilohy/SK/OP/2023/19/20240101_5586740-2.pdf) | Financial statement format (individual, from 2024) |
| **Opatrenie MF/23378/2014-74** | slov-lex.sk (search) | Simplified statements for small units |

---

## 2. XSD SCHEMAS (for software developers)

### Central Schema Repository
| Resource | URL |
|----------|-----|
| **All XSD schemas** | [financnasprava.sk/xsd-schemy](https://www.financnasprava.sk/sk/danovi-a-colni-specialisti/technicke-informacie/podklady-pre-tvorcov-sw/xsd-schemy) |
| **Direct XSD access** | [ekr.financnasprava.sk/Formulare/XSD/](https://ekr.financnasprava.sk/Formulare/XSD/) |

### Specific Schemas
| Schema | URL | Format |
|--------|-----|--------|
| **KV DPH 2025** (Kontrolný výkaz) | [kv_dph_2025.xsd](https://ekr.financnasprava.sk/Formulare/XSD/kv_dph_2025.xsd) | XML |
| **KV DPH 2023** | [kv_dph_2023.xsd](https://ekr.financnasprava.sk/Formulare/XSD/kv_dph_2023.xsd) | XML |
| **Súhrnný výkaz DPH** (form 471) | [Form portal](https://pfseform.financnasprava.sk/Formulare/eFormVzor/DP/form.471.html) | XML |
| Súhrnný výkaz PDF template | [SVDPHv20.pdf](https://pfseform.financnasprava.sk/Formulare/VzoryTlaciv/SVDPHv20.pdf) | PDF |
| Súhrnný výkaz instructions | [SVDPHv20-poucenie.pdf](https://pfseform.financnasprava.sk/Formulare/Poucenia/SVDPHv20-poucenie.pdf) | PDF |
| **KV DPH form** (form 607) | [Form portal](https://pfseform.financnasprava.sk/Formulare/eFormVzor/DP/form.607.html) | XML |
| **All forms portal** | [pfseform.financnasprava.sk](https://pfseform.financnasprava.sk/) | Various |

---

## 3. ELECTRONIC FILING (eDane)

| Resource | URL |
|----------|-----|
| **eDane portal** | [financnasprava.sk/edane](https://www.financnasprava.sk/sk/elektronicke-sluzby/elektronicka-komunikacia/elektronicka-komunikacia-dane/edane) |
| **eDane user guide (PDF)** | [User_guide_eDANE_java.pdf](https://www.financnasprava.sk/_img/pfsedit/Dokumenty_PFS/Elektronicke_sluzby/Elektronicka_komunikacia/Elektronicka_komunikacia_dane/Prirucky_navody/2024/User_guide_eDANE_java.pdf) |
| **Electronic submission portal** | [financnasprava.sk/elektronicka-podatelna](https://www.financnasprava.sk/sk/elektronicke-sluzby/elektronicka-komunikacia/elektronicka-komunikacia-dane/elektronicka-podatelna-danove) |
| **Register účtovných závierok** | [registeruz.sk](https://www.registeruz.sk/cruz-public/home) |

---

## 4. E-INVOICING (2027 MANDATE)

### Slovak Implementation
| Resource | URL | Notes |
|----------|-----|-------|
| IS eFaktúra demo portal | [web-einvoice-demo.mypaas.vnet.sk](https://web-einvoice-demo.mypaas.vnet.sk/) | Test environment |
| Official FAQ (Guide 9/DPH/2025/IM) | Via financnasprava.sk | Key implementation document |
| Accreditation rules for e-invoicing providers | [vatupdate.com](https://www.vatupdate.com/2026/02/04/slovakia-sets-accreditation-rules-for-e-invoicing-providers-ahead-of-2027-mandate/) | Feb 2026 |

### EN 16931 / UBL / PEPPOL Standards
| Resource | URL |
|----------|-----|
| **PEPPOL BIS Billing 3.0** | [docs.peppol.eu](https://docs.peppol.eu/poacc/billing/3.0/) |
| EN 16931 format overview | [cleartax.com](https://www.cleartax.com/be/what-is-en-16931) |
| EU e-Invoicing concepts | [josemmo.github.io](https://josemmo.github.io/einvoicing/getting-started/eu-einvoicing-concepts/) |
| EU Digital Building Blocks — Slovakia | [ec.europa.eu](https://ec.europa.eu/digital-building-blocks/sites/spaces/DIGITAL/pages/467108899/eInvoicing+in+Slovakia) |

### Timeline
- **2026**: Voluntary e-invoicing period
- **January 1, 2027**: Mandatory B2B + B2G structured e-invoicing
- **July 1, 2030**: Mandatory EU cross-border B2B
- Format: EN 16931 UBL XML via PEPPOL network (5-corner model)
- Penalties: €10,000 per violation, up to €100,000 for repeat

---

## 5. eKASA (Cash Register)

| Resource | URL |
|----------|-----|
| eKasa portal | [financnasprava.sk/ekasa](https://www.financnasprava.sk/sk/podnikatelia/dane/ekasa) |
| VRP2 portal | [vrp2.financnasprava.sk](https://vrp2.financnasprava.sk/) |
| VRP2 user manual (PDF) | [VRP2 v2.0.1](https://www.financnasprava.sk/_img/pfsedit/Dokumenty_PFS/Elektronicke_sluzby/Elektronicka_komunikacia/Elektronicka_komunikacia_dane/Prirucky_navody/2023/2023.11.15_Prir_VRP2_v2.0.1.pdf) |
| New Act No. 384/2025 (from Jan 2026) | [tax-audit.sk](https://www.tax-audit.sk/en/novinky/new-act-on-revenue-recording-from-1-1-2026-what-changes-in-ekasa-and-what-are-the-new-obligations) |

---

## 6. PSD2 / OPEN BANKING (Slovak Banks)

### Bank Developer Portals
| Bank | URL | Notes |
|------|-----|-------|
| **Tatra banka** | [developer.tatrabanka.sk](https://developer.tatrabanka.sk/) | Redirect-based auth, SCA via mobile |
| **SLSP** (Slovenská sporiteľňa) | [slsp.sk/psd2-api-banking](https://www.slsp.sk/sk/biznis/elektronicke-bankovnictvo/psd2-api-banking) | Largest bank |
| SLSP API spec (v5.2) | [slsppsd2publicspecification.docs.apiary.io](https://slsppsd2publicspecification.docs.apiary.io/) | Technical docs |
| SLSP (Erste group) | [developers.erstegroup.com](https://developers.erstegroup.com/) | Parent company portal |
| **VÚB** | [vub.sk/ini-poskytovatelia-sluzieb](https://www.vub.sk/en/firmy-a-podnikatelia/platby/ini-poskytovatelia-sluzieb.html) | PSD2 info |
| VÚB PSD2 API docs (v1.4) | [vub.cz (PDF)](https://www.vub.cz/files/ucty-platby/platby/platebni-formulare/jini-poskytovatele-sluzeb-technicka-dokumentace-api-psd2.pdf) | Berlin Group standard |
| VÚB implementation guidelines | [vub.sk (PDF)](https://www.vub.sk/document/documents/VUB/psd2/vub_psd2_bgs_implementation_guidelines.pdf) | NextGenPSD2 |

### NBS (National Bank of Slovakia)
| Resource | URL |
|----------|-----|
| Open Banking overview | [nbs.sk/open-banking](https://nbs.sk/en/financial-market-supervision1/supervision/payment-services-and-electronic-money/open-banking/) |
| PSD2 incident reporting | [nbs.sk](https://nbs.sk/en/dohlad-nad-financnym-trhom/legislativa/legislativa/detail-dokumentu/revised-guidelines-on-major-incident-reporting-under-psd2/) |
| AISP/PI requirements | [nbs.sk](https://nbs.sk/en/financial-market-supervision1/supervision/payment-services-and-electronic-money/payment-institutions-and-aisp/business-requirements/) |

### Aggregators
| Service | Coverage |
|---------|----------|
| **Salt Edge** | 1,585+ institutions including all Slovak banks |
| **finAPI** | SK, CZ, AT, HU, DE coverage |

---

## 7. DPH METHODOLOGICAL GUIDELINES

| Document | URL |
|----------|-----|
| **All methodical guidelines** | [financnasprava.sk/metodicke-pokyny](https://www.financnasprava.sk/sk/danovi-a-colni-specialisti/dane/metodicke-pokyny) |
| DPH 2025 registration guidelines | [002_DPH_2025_MP.pdf](https://www.financnasprava.sk/_img/pfsedit/Dokumenty_PFS/Zverejnovanie_dok/Dane/Metodicke_pokyny/Nepriame_dane/2025/2025.09.22_002_DPH_2025_MP.pdf) |
| KV DPH methodology | [002_DPH_2021_MP_kvdph.pdf](https://www.financnasprava.sk/_img/pfsedit/Dokumenty_PFS/Zverejnovanie_dok/Dane/Metodicke_pokyny/Nepriame_dane/2021/2021.03.29_002_DPH_2021_MP_kvdph.pdf) |
| Depreciation accounting guidance | [33_DZPaU_2021_MU.pdf](https://www.financnasprava.sk/_img/pfsedit/Dokumenty_PFS/Zverejnovanie_dok/Dane/Metodicke_usmernenia/Priame_dane/2021/2021.09.09_33_DZPaU_2021_MU.pdf) |
| Accruals accounting guidance | [financnasprava.sk (PDF)](https://www.financnasprava.sk/_img/pfsedit/Dokumenty_PFS/Infoservis/Aktualne_informacie/dp/2017/UCT/2017_02_06_uctovanie_casoveho_rozlisenia.pdf) |

---

## 8. PRACTICAL GUIDES & WORKED EXAMPLES

### DPH / VAT Examples
| Resource | URL | Content |
|----------|-----|---------|
| **Praktické príklady účtovania DPH** | [danovecentrum.sk](https://www.danovecentrum.sk/odborny-clanok/prakticke-priklady-uctovania-dph.htm) | Comprehensive VAT booking examples |
| DPH examples 2022 | [danovecentrum.sk](https://www.danovecentrum.sk/uctovne-suvztaznosti/1-prakticke-priklady-uctovania-dph-us-2022.htm) | Year-specific |
| DPH examples 2023 | [danovecentrum.sk](https://www.danovecentrum.sk/uctovne-suvztaznosti/1-prakticke-priklady-uctovania-dph-us-2023.htm) | Year-specific |
| KV DPH filling examples | [danovecentrum.sk](https://www.danovecentrum.sk/odborny-clanok/priklady-ku-kontrolnemu-vykazu-dph.htm) | Section A1/A2/B1-B3 examples |
| Reverse charge examples | [danovecentrum.sk](https://www.danovecentrum.sk/odborny-clanok/tuzemsky-prenos-danovej-povinnosti-dau-05-2023.htm) | Tuzemský prenos DP |
| How to fill KV DPH | [podnikajte.sk](https://www.podnikajte.sk/dan-z-pridanej-hodnoty/ako-vyplnit-kontrolny-vykaz-dph) | Step by step |

### General Booking Examples
| Resource | URL | Content |
|----------|-----|---------|
| **Účtovné príklady v praxi** | [ako-uctovat.sk](https://www.ako-uctovat.sk/uctovne-priklady-predkontacie.php) | Predkontácie (pre-entries) for all common scenarios |
| DPH on received invoices | [ako-uctovat.sk](https://www.ako-uctovat.sk/clanok.php?t=Uctovanie-DPH-prijatych-faktur-v-prikladoch&idc=309) | Worked examples |
| Banking in double-entry | [podnikajte.sk](https://www.podnikajte.sk/uctovnictvo/ucet-v-banke-uctovanie-v-podvojnom-uctovnictve) | Bank account operations |
| Dividend payments | [danovecentrum.sk](https://www.danovecentrum.sk/odborny-clanok/priklady-na-vyplatenie-podielov-na-zisku-dividendy-uctovanie-dane-z-prijmov-pri-prijmoch-vyberanych-zrazkou.htm) | Profit distribution |
| Cryptocurrency operations | [danovecentrum.sk](https://www.danovecentrum.sk/odborny-clanok/3--prakticke-priklady-uctovania-a-danoveho-posudenia-operacii-s-virtualnymi-menami.htm) | Virtual currency |

### Year-End Closing
| Resource | URL |
|----------|-----|
| Year-end closing in Money S3 | [money.sk](https://www.money.sk/navod/uzavierka-roku-v-podvojnom-uctovnictve/) |
| Financial statements step-by-step | [jaspis.sk](https://jaspis.sk/aktuality/uctovna-zavierka) |
| 10 steps before closing | [podnikajte.sk](https://www.podnikajte.sk/uctovnictvo/kroky-pred-zostavenim-uctovnej-zavierky-2019) |
| Accruals (časové rozlíšenie) | [podnikajte.sk](https://www.podnikajte.sk/uctovnictvo/casove-rozlisenie-uctovanie) |
| Reserves & provisions | [podnikajte.sk](https://www.podnikajte.sk/uctovnictvo/rezervy) |

### Payroll
| Resource | URL |
|----------|-----|
| Wage & contribution accounting | [podnikajte.sk](https://www.podnikajte.sk/uctovnictvo/uctovanie-miezd-odvodov) |
| Payroll in double-entry | [humanet.sk](https://humanet.sk/blog/uctovanie-miezd-podvojne-uctovnictvo) |
| 2025 contribution rates | [podnikajte.sk](https://www.podnikajte.sk/socialne-a-zdravotne-odvody/odvody-zamestnanca-zamestnavatela-od-1-1-2025) |

### Fixed Assets & Depreciation
| Resource | URL |
|----------|-----|
| Depreciation guide | [moneyerp.com](https://moneyerp.com/sk-sk/ako-spravne-odpisovat-dlhodoby-majetok) |
| Depreciation groups 2025 | [podnikajte.sk](https://www.podnikajte.sk/odpisy/odpisove-skupiny-zaradenie-majetku-2025) |
| Capitalization thresholds | €1,700 tangible / €2,400 intangible (2025) |
| Acquisition, depreciation, disposal | [money.sk](https://www.money.sk/navod/dlhodoby-majetok-obstaranie-odpisy-vyradenie/) |

---

## 9. CHART OF ACCOUNTS RESOURCES

| Resource | URL | Notes |
|----------|-----|-------|
| **Účtová osnova 2023/2024 (downloadable)** | [podnikajte.sk](https://www.podnikajte.sk/uctovnictvo/uctova-osnova-2023-2024) | With descriptions |
| EUBA — full framework chart (PDF) | [fhi.euba.sk](https://fhi.euba.sk/www_write/files/katedry/kua/studijne_materialy/ramcova-uctova-osnova.pdf) | Academic reference |
| Chart of accounts with descriptions | [poradca.sk](https://www.poradca.sk/dokument/priloha-k-opatreniu-c-23-0542002-92-ramcova-uctova-osnova-pre-podnikatelov/29044) | Per-account detail |
| What is účtová osnova | [money.sk](https://www.money.sk/novinky-a-tipy/uctovnictvo/co-je-uctova-osnova-a-ako-s-nou-pracovat-v-uctovnom-programe-a-bez-neho/) | Explainer |

---

## 10. PROFESSIONAL ORGANIZATIONS

| Organization | URL | Purpose |
|-------------|-----|---------|
| **Slovenská komora audítorov** (Auditors) | [skau.sk](https://www.skau.sk/) | Audit standards |
| **Slovenská komora daňových poradcov** (Tax Advisors) | [skdp.sk](https://www.skdp.sk/) | Tax guidance |
| **Slovenská komora certifikovaných účtovníkov** | [skcu.sk](https://skcu.sk/) | Accountant certification |
| **JASPIS** (Training) | [jaspis.sk](https://jaspis.sk/) | Accounting courses (80h double-entry course) |

---

## 11. TOP PRACTICAL RESOURCES (ranked by usefulness for knowledge graph)

1. **Opatrenie 23054/2002-92 (Postupy účtovania)** — THE source of all booking rules
2. **danovecentrum.sk** — Best worked examples for DPH and all transaction types
3. **ako-uctovat.sk** — Predkontácie (standard booking patterns) for every common scenario
4. **podnikajte.sk** — Comprehensive topic articles with current-year specifics
5. **money.sk/navod/** — Step-by-step guides matching real software workflows
6. **financnasprava.sk XSD schemas** — Technical specs for all filing formats
7. **PEPPOL BIS Billing 3.0** — E-invoicing technical standard

---

## 12. OPEN SOURCE REFERENCES

| Resource | URL | Notes |
|----------|-----|-------|
| Daňové priznanie Digital (DPFO) | [github.com/slovensko-digital](https://github.com/slovensko-digital/priznanie-digital) | Open source tax return project |
| Tatra banka PHP API wrapper | github.com/pavolbiely/tatrabanka-api | Community PSD2 integration |
