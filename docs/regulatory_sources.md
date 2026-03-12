# Slovak Accounting — Regulatory Sources & Documentation

Complete inventory of all laws, regulations, technical specs, and practical guides needed for building Slovak double-entry accounting software.

**Organized by build stage** — the order you'd implement features. Each resource appears exactly once.

---

## STAGE 1: FOUNDATION (build first)

Core laws, chart of accounts, tax administration, data protection, and business registers. These underpin everything else.

### 1.1 Core Accounting Law

| Document | URL | Coverage |
|----------|-----|----------|
| **Zákon č. 431/2002 Z.z. o účtovníctve** | [slov-lex.sk](https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/2002/431/) | Main accounting law — mandatory double-entry for all s.r.o. |
| **Opatrenie MF SR č. 23054/2002-92** (Postupy účtovania) | [mfsr.sk](https://www.mfsr.sk/sk/dane-cla-uctovnictvo/uctovnictvo-audit/uctovnictvo/legislativa-sr/opatrenia-oblasti-uctovnictva/uctovnictvo-podnikatelov/podvojne-uctovnictvo/postupy-uctovania/) | **THE critical document** — all booking rules + chart of accounts framework |
| Postupy účtovania (PDF, Feb 2025) | [financnasprava.sk](https://www.financnasprava.sk/_img/pfsedit/Dokumenty_PFS/Zverejnovanie_dok/Sprievodca/Postupy_uct/2025/2025.02.12_opatr_MFSR_23054_2002_92.pdf) | Current consolidated version |

### 1.2 Chart of Accounts (Účtová osnova)

| Resource | URL | Notes |
|----------|-----|-------|
| **Rámcová účtová osnova** (Chart of Accounts) | [slov-lex.sk (PDF)](https://static.slov-lex.sk/pdf/prilohy/SK/ZZ/2002/742/20021231_2871886-2.pdf) | 10-class account framework |
| **Účtová osnova 2023/2024 (downloadable)** | [podnikajte.sk](https://www.podnikajte.sk/uctovnictvo/uctova-osnova-2023-2024) | With descriptions |
| EUBA — full framework chart (PDF) | [fhi.euba.sk](https://fhi.euba.sk/www_write/files/katedry/kua/studijne_materialy/ramcova-uctova-osnova.pdf) | Academic reference |
| Chart of accounts with descriptions | [poradca.sk](https://www.poradca.sk/dokument/priloha-k-opatreniu-c-23-0542002-92-ramcova-uctova-osnova-pre-podnikatelov/29044) | Per-account detail |
| What is účtová osnova | [money.sk](https://www.money.sk/novinky-a-tipy/uctovnictvo/co-je-uctova-osnova-a-ako-s-nou-pracovat-v-uctovnom-programe-a-bez-neho/) | Explainer |

### 1.3 Tax Administration

| Document | URL | Coverage |
|----------|-----|----------|
| **Zákon č. 563/2009 Z.z. o správe daní** (Daňový poriadok) | [slov-lex.sk](https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/2009/563/) | Tax administration — deadlines, penalties, filing procedures, taxpayer obligations |

### 1.4 Data Protection

| Document | URL | Coverage |
|----------|-----|----------|
| **Zákon č. 18/2018 Z.z. o ochrane osobných údajov** | [slov-lex.sk](https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/2018/18/) | GDPR implementation — required for any SaaS handling company data |

### 1.5 Business Registers & Company Verification

| Resource | URL | Purpose |
|----------|-----|---------|
| **Obchodný register SR** | [orsr.sk](https://www.orsr.sk/) | Company lookup by IČO, name, address |
| **Register právnických osôb (RPO)** | [rpo.statistics.sk](https://rpo.statistics.sk/) | Statistical office — all legal entities |
| **Finstat** | [finstat.sk](https://www.finstat.sk/) | Company financials, IČO lookup, credit ratings |

### 1.6 General Booking Examples

| Resource | URL | Content |
|----------|-----|---------|
| **Účtovné príklady v praxi** | [ako-uctovat.sk](https://www.ako-uctovat.sk/uctovne-priklady-predkontacie.php) | Predkontácie (pre-entries) for all common scenarios |
| DPH on received invoices | [ako-uctovat.sk](https://www.ako-uctovat.sk/clanok.php?t=Uctovanie-DPH-prijatych-faktur-v-prikladoch&idc=309) | Worked examples |
| Banking in double-entry | [podnikajte.sk](https://www.podnikajte.sk/uctovnictvo/ucet-v-banke-uctovanie-v-podvojnom-uctovnictve) | Bank account operations |
| Dividend payments | [danovecentrum.sk](https://www.danovecentrum.sk/odborny-clanok/priklady-na-vyplatenie-podielov-na-zisku-dividendy-uctovanie-dane-z-prijmov-pri-prijmoch-vyberanych-zrazkou.htm) | Profit distribution |
| Cryptocurrency operations | [danovecentrum.sk](https://www.danovecentrum.sk/odborny-clanok/3--prakticke-priklady-uctovania-a-danoveho-posudenia-operacii-s-virtualnymi-menami.htm) | Virtual currency |

### 1.7 Electronic Filing Infrastructure

| Resource | URL |
|----------|-----|
| **eDane portal** | [financnasprava.sk/edane](https://www.financnasprava.sk/sk/elektronicke-sluzby/elektronicka-komunikacia/elektronicka-komunikacia-dane/edane) |
| **eDane user guide (PDF)** | [User_guide_eDANE_java.pdf](https://www.financnasprava.sk/_img/pfsedit/Dokumenty_PFS/Elektronicke_sluzby/Elektronicka_komunikacia/Elektronicka_komunikacia_dane/Prirucky_navody/2024/User_guide_eDANE_java.pdf) |
| **Electronic submission portal** | [financnasprava.sk/elektronicka-podatelna](https://www.financnasprava.sk/sk/elektronicke-sluzby/elektronicka-komunikacia/elektronicka-komunikacia-dane/elektronicka-podatelna-danove) |
| **SW developer technical info** | [financnasprava.sk/podklady-pre-tvorcov-sw](https://www.financnasprava.sk/sk/danovi-a-colni-specialisti/technicke-informacie/podklady-pre-tvorcov-sw) |
| **All XSD schemas** | [financnasprava.sk/xsd-schemy](https://www.financnasprava.sk/sk/danovi-a-colni-specialisti/technicke-informacie/podklady-pre-tvorcov-sw/xsd-schemy) |
| **Direct XSD access** | [ekr.financnasprava.sk/Formulare/XSD/](https://ekr.financnasprava.sk/Formulare/XSD/) |
| **All forms portal** | [pfseform.financnasprava.sk](https://pfseform.financnasprava.sk/) |

---

## STAGE 2: DAILY TRANSACTIONS (core MVP)

DPH, invoicing, bank feeds — the day-to-day accounting engine.

### 2.1 DPH Law & Rates

| Document | URL | Coverage |
|----------|-----|----------|
| **Zákon č. 222/2004 Z.z. o DPH** (VAT Act) | [slov-lex.sk](https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/2004/222/) | VAT rates, registration, deductions, reverse charge |
| DPH Law (PDF, Jan 2025) | [financnasprava.sk](https://www.financnasprava.sk/_img/pfsedit/Dokumenty_PFS/Zverejnovanie_dok/Sprievodca/Sprievodca_danami/2025/2025.01.28_zakon_DPH.pdf) | Current consolidated version |

### 2.2 DPH Methodological Guidelines

| Document | URL |
|----------|-----|
| **All methodical guidelines** | [financnasprava.sk/metodicke-pokyny](https://www.financnasprava.sk/sk/danovi-a-colni-specialisti/dane/metodicke-pokyny) |
| DPH 2025 registration guidelines | [002_DPH_2025_MP.pdf](https://www.financnasprava.sk/_img/pfsedit/Dokumenty_PFS/Zverejnovanie_dok/Dane/Metodicke_pokyny/Nepriame_dane/2025/2025.09.22_002_DPH_2025_MP.pdf) |
| KV DPH methodology | [002_DPH_2021_MP_kvdph.pdf](https://www.financnasprava.sk/_img/pfsedit/Dokumenty_PFS/Zverejnovanie_dok/Dane/Metodicke_pokyny/Nepriame_dane/2021/2021.03.29_002_DPH_2021_MP_kvdph.pdf) |

### 2.3 DPH Practical Examples

| Resource | URL | Content |
|----------|-----|---------|
| **Praktické príklady účtovania DPH** | [danovecentrum.sk](https://www.danovecentrum.sk/odborny-clanok/prakticke-priklady-uctovania-dph.htm) | Comprehensive VAT booking examples |
| DPH examples 2022 | [danovecentrum.sk](https://www.danovecentrum.sk/uctovne-suvztaznosti/1-prakticke-priklady-uctovania-dph-us-2022.htm) | Year-specific |
| DPH examples 2023 | [danovecentrum.sk](https://www.danovecentrum.sk/uctovne-suvztaznosti/1-prakticke-priklady-uctovania-dph-us-2023.htm) | Year-specific |
| KV DPH filling examples | [danovecentrum.sk](https://www.danovecentrum.sk/odborny-clanok/priklady-ku-kontrolnemu-vykazu-dph.htm) | Section A1/A2/B1-B3 examples |
| Reverse charge examples | [danovecentrum.sk](https://www.danovecentrum.sk/odborny-clanok/tuzemsky-prenos-danovej-povinnosti-dau-05-2023.htm) | Tuzemský prenos DP |
| How to fill KV DPH | [podnikajte.sk](https://www.podnikajte.sk/dan-z-pridanej-hodnoty/ako-vyplnit-kontrolny-vykaz-dph) | Step by step |

### 2.4 DPH & VAT Reporting XSD Schemas

| Schema | URL | Format |
|--------|-----|--------|
| **DPH daňové priznanie 2025** (VAT return) | [dph2025.xsd](https://ekr.financnasprava.sk/Formulare/XSD/dph2025.xsd) | XML |
| **DPH daňové priznanie 2021** | [dph2021.xsd](https://ekr.financnasprava.sk/Formulare/XSD/dph2021.xsd) | XML |
| **KV DPH 2025** (Kontrolný výkaz) | [kv_dph_2025.xsd](https://ekr.financnasprava.sk/Formulare/XSD/kv_dph_2025.xsd) | XML |
| **KV DPH 2023** | [kv_dph_2023.xsd](https://ekr.financnasprava.sk/Formulare/XSD/kv_dph_2023.xsd) | XML |
| **Súhrnný výkaz DPH** | [svdph20.xsd](https://ekr.financnasprava.sk/Formulare/XSD/svdph20.xsd) | XML |
| **OSS/VAT One-Stop Shop** | [dposs_eu.xsd](https://ekr.financnasprava.sk/Formulare/XSD/dposs_eu.xsd) | XML |
| **Súhrnný výkaz form** (form 471) | [Form portal](https://pfseform.financnasprava.sk/Formulare/eFormVzor/DP/form.471.html) | XML |
| Súhrnný výkaz PDF template | [SVDPHv20.pdf](https://pfseform.financnasprava.sk/Formulare/VzoryTlaciv/SVDPHv20.pdf) | PDF |
| Súhrnný výkaz instructions | [SVDPHv20-poucenie.pdf](https://pfseform.financnasprava.sk/Formulare/Poucenia/SVDPHv20-poucenie.pdf) | PDF |
| **KV DPH form** (form 607) | [Form portal](https://pfseform.financnasprava.sk/Formulare/eFormVzor/DP/form.607.html) | XML |

### 2.5 PSD2 / Open Banking (Bank Feeds)

#### Bank Developer Portals

| Bank | URL | Notes |
|------|-----|-------|
| **Tatra banka** | [developer.tatrabanka.sk](https://developer.tatrabanka.sk/) | Redirect-based auth, SCA via mobile |
| **SLSP** (Slovenská sporiteľňa) | [slsp.sk/psd2-api-banking](https://www.slsp.sk/sk/biznis/elektronicke-bankovnictvo/psd2-api-banking) | Largest bank |
| SLSP API spec (v5.2) | [slsppsd2publicspecification.docs.apiary.io](https://slsppsd2publicspecification.docs.apiary.io/) | Technical docs |
| SLSP (Erste group) | [developers.erstegroup.com](https://developers.erstegroup.com/) | Parent company portal |
| **VÚB** | [vub.sk/ini-poskytovatelia-sluzieb](https://www.vub.sk/en/firmy-a-podnikatelia/platby/ini-poskytovatelia-sluzieb.html) | PSD2 info |
| VÚB PSD2 API docs (v1.4) | [vub.cz (PDF)](https://www.vub.cz/files/ucty-platby/platby/platebni-formulare/jini-poskytovatele-sluzeb-technicka-dokumentace-api-psd2.pdf) | Berlin Group standard |
| VÚB implementation guidelines | [vub.sk (PDF)](https://www.vub.sk/document/documents/VUB/psd2/vub_psd2_bgs_implementation_guidelines.pdf) | NextGenPSD2 |

#### NBS (National Bank of Slovakia)

| Resource | URL |
|----------|-----|
| Open Banking overview | [nbs.sk/open-banking](https://nbs.sk/en/financial-market-supervision1/supervision/payment-services-and-electronic-money/open-banking/) |
| PSD2 incident reporting | [nbs.sk](https://nbs.sk/en/dohlad-nad-financnym-trhom/legislativa/legislativa/detail-dokumentu/revised-guidelines-on-major-incident-reporting-under-psd2/) |
| AISP/PI requirements | [nbs.sk](https://nbs.sk/en/financial-market-supervision1/supervision/payment-services-and-electronic-money/payment-institutions-and-aisp/business-requirements/) |

#### Aggregators

| Service | Coverage |
|---------|----------|
| **Salt Edge** | 1,585+ institutions including all Slovak banks |
| **finAPI** | SK, CZ, AT, HU, DE coverage |

---

## STAGE 3: PAYROLL (module 2)

Social insurance, health insurance, social fund, wage accounting.

### 3.1 Payroll Laws

| Document | URL | Coverage |
|----------|-----|----------|
| **Zákon č. 461/2003 Z.z. o sociálnom poistení** | [slov-lex.sk](https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/2003/461/) | Social insurance — pension, disability, sickness, unemployment, guarantee, accident, reserve fund contributions |
| **Zákon č. 580/2004 Z.z. o zdravotnom poistení** | [slov-lex.sk](https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/2004/580/) | Health insurance — employee/employer contributions, annual settlement |
| **Zákon č. 152/1994 Z.z. o sociálnom fonde** | [slov-lex.sk](https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/1994/152/) | Social fund — mandatory 0.6–1.0% employer contribution, permitted uses |

### 3.2 Social Insurance Rates (2025)

**Employee contributions (from gross salary):**

| Insurance Type | Rate | Notes |
|---|---|---|
| Old-age (starobné) | 4.00% | Tier 1 pension |
| Disability (invalidné) | 3.00% | Invalidity |
| Sickness (nemocenské) | 1.40% | Sick leave |
| Unemployment (nezamestnanosť) | 1.00% | Unemployment |
| **Total employee** | **9.40%** | Capped at max assessment basis |

**Employer contributions:**

| Insurance Type | Rate | Notes |
|---|---|---|
| Old-age (starobné) | 14.00% | Largest employer burden |
| Disability (invalidné) | 3.00% | |
| Sickness (nemocenské) | 1.40% | |
| Solidarity reserve fund | 4.75% | |
| Unemployment (nezamestnanosť) | 0.75% | |
| Guarantee (garančné) | 0.25% | |
| Accident (úrazové) | 0.80% | **Uncapped** |
| **Total employer social** | **24.40%** | Capped (except accident) |

**Assessment basis cap (2025):** €15,730/month (€16,764 from 2026)

### 3.3 Health Insurance Rates (2025)

| Party | Rate | Notes |
|---|---|---|
| Employee | 4.00% | From gross salary |
| Employer | 11.00% | **Uncapped** |

**Health insurance providers:** VšZP (~62% market share), Dôvera (~22%), Union (~16%)

### 3.4 Social Fund

| Item | Details |
|---|---|
| Mandatory for | All employers with ≥1 employee |
| Rate | 0.6% to 1.0% of gross wages (employer choice) |
| Account | Debit 527 (Zákonné sociálne náklady) / Credit 472 (Záväzky zo sociálneho fondu) |
| Storage | Must be in separate bank account or analytical account |

### 3.5 Tax Values (2025)

| Item | Amount |
|---|---|
| Non-taxable portion (nezdaniteľná časť) | €5,753.79/year (€479.48/month) |
| Tax rate (standard) | 19% (up to €48,441.43) |
| Tax rate (higher) | 25% (above €48,441.43) |
| Tax bonus per child (under 15) | €100/month |
| Tax bonus per child (15–18) | €50/month |
| Minimum wage | €816/month |
| Minimum living standard | €273.99/month |

### 3.6 Payroll Accounts (Chart of Accounts)

| Account | Name | Usage |
|---|---|---|
| **331** | Zamestnanci | Employee salary liability |
| **333** | Ostatné záväzky voči zamestnancom | Travel advances, other payroll obligations |
| **335** | Pohľadávky voči zamestnancom | Amounts owed by employees |
| **336** | Zúčtovanie s orgánmi SP a ZP | Insurance contribution liabilities |
| **342** | Ostatné priame dane | Income tax withholding liability |
| **472** | Záväzky zo sociálneho fondu | Social fund reserves |
| **521** | Mzdy zamestnancov | Wage expense (P&L) |
| **524** | Sociálne poistenie zamestnávateľa | Employer insurance expense |
| **527** | Zákonné sociálne náklady | Social fund contributions expense |

### 3.7 Standard Payroll Journal Entry

| Transaction | Debit | Credit |
|---|---|---|
| Record gross salary | 521 | 331 |
| Health insurance (employee 4%) | 331 | 336 |
| Social insurance (employee 9.4%) | 331 | 336 |
| Income tax withholding | 331 | 342 |
| Employer social insurance (24.4%) | 524 | 336 |
| Employer health insurance (11%) | 524 | 336 |
| Social fund (0.6–1.0%) | 527 | 472 |
| Salary payment to employee | 331 | 221 (Bank) |
| Insurance payment to authorities | 336 | 221 (Bank) |
| Tax payment to authorities | 342 | 221 (Bank) |

### 3.8 Payroll Reporting Portals

| Institution | Portal | Purpose |
|---|---|---|
| **Sociálna poisťovňa** | [esluzby.socpoist.sk](https://esluzby.socpoist.sk/) | Monthly contribution reporting, employee registration/deregistration |
| **VšZP** | [vszp.sk/platitelia](https://www.vszp.sk/platitelia/) | Employer reporting, advance payments |
| **Dôvera** | [dovera.sk](https://www.dovera.sk/) | Employer e-branch |
| **Union** | [union.sk](https://www.union.sk/) | Annual settlement, employer docs |

### 3.9 Payroll Practical Guides

| Resource | URL | Content |
|----------|-----|---------|
| Wage & contribution accounting | [podnikajte.sk](https://www.podnikajte.sk/uctovnictvo/uctovanie-miezd-odvodov) | Full payroll booking walkthrough |
| Payroll in double-entry | [humanet.sk](https://humanet.sk/blog/uctovanie-miezd-podvojne-uctovnictvo) | Account-by-account examples |
| 2025 contribution rates | [podnikajte.sk](https://www.podnikajte.sk/socialne-a-zdravotne-odvody/odvody-zamestnanca-zamestnavatela-od-1-1-2025) | Current year rates |
| Net salary calculator 2025 | [danovecentrum.sk](https://www.danovecentrum.sk/kalkulacky/vypocet-cistej-mzdy-od-1-1-2025-do-31-12-2025.htm) | Interactive tool |
| SP contribution tables | [socpoist.sk](https://www.socpoist.sk/en/social-insurance/contribution-payment-tables-january-1-2026) | Official rates & caps |
| VšZP changes 2025 | [vszp.sk](https://www.vszp.sk/platitelia/platenie-poistneho/oznamenia-zmeny/zmeny-od-01-01.2025/) | Health insurance updates |
| Social fund rules | [employment.gov.sk](https://www.employment.gov.sk/sk/praca-zamestnanost/vztah-zamestnanca-zamestnavatela/socialny-fond/) | Legal framework |
| All wage values 2025 | [relia.sk](https://www.relia.sk/Article.aspx?ID=1154) | Summary of all parameters |

---

## STAGE 4: PERIOD CLOSING & REPORTING (module 3)

Financial statements, corporate tax, year-end closing, fixed assets, depreciation.

### 4.1 Income Tax & Corporate Tax

| Document | URL | Coverage |
|----------|-----|----------|
| **Zákon č. 595/2003 Z.z. o dani z príjmov** (Income Tax) | [slov-lex.sk](https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/2003/595/) | Corporate tax, depreciation rules, deductions |

### 4.2 Financial Statements Regulations

| Document | URL | Coverage |
|----------|-----|----------|
| **Opatrenie MF/13542/2023-36** | [slov-lex.sk (PDF)](https://static.slov-lex.sk/pdf/prilohy/SK/OP/2023/19/20240101_5586740-2.pdf) | Financial statement format (individual, from 2024) |
| **Opatrenie MF/23378/2014-74** | slov-lex.sk (search) | Simplified statements for small units |
| **Register účtovných závierok** | [registeruz.sk](https://www.registeruz.sk/cruz-public/home) | Published financial statements (public) |

### 4.3 Corporate Tax & Financial Statement XSD Schemas

| Schema | URL | Format |
|--------|-----|--------|
| **DPPO 2025** (Corporate income tax return) | [dppo2025.xsd](https://ekr.financnasprava.sk/Formulare/XSD/dppo2025.xsd) | XML |
| **DPPO 2024** | [dppo2024.xsd](https://ekr.financnasprava.sk/Formulare/XSD/dppo2024.xsd) | XML |
| **DPFO A 2025** (Individual income tax part A) | [dpfo_a2025.xsd](https://ekr.financnasprava.sk/Formulare/XSD/dpfo_a2025.xsd) | XML |
| **DPFO B 2025** (Individual income tax part B) | [dpfo_b2025.xsd](https://ekr.financnasprava.sk/Formulare/XSD/dpfo_b2025.xsd) | XML |
| **Registration DP** | [regdp2024.xsd](https://ekr.financnasprava.sk/Formulare/XSD/regdp2024.xsd) | XML |
| **Účtovná závierka (general)** | [vp_uct2021.xsd](https://ekr.financnasprava.sk/Formulare/XSD/vp_uct2021.xsd) | XML |
| **Účtovná závierka (registration)** | [vp_reg2024.xsd](https://ekr.financnasprava.sk/Formulare/XSD/vp_reg2024.xsd) | XML |
| **Účtovná závierka (small business)** | [vp_spd2024.xsd](https://ekr.financnasprava.sk/Formulare/XSD/vp_spd2024.xsd) | XML |
| **Form 588** (financial statement, large) | [form.588.sk.xsd](https://ekr.financnasprava.sk/Formulare/XSD/form.588.sk.xsd) | XML |
| **Form 479** | [form.479.sk.xsd](https://ekr.financnasprava.sk/Formulare/XSD/form.479.sk.xsd) | XML |
| **Form 515** | [form.515.sk.xsd](https://ekr.financnasprava.sk/Formulare/XSD/form.515.sk.xsd) | XML |

### 4.4 Year-End Closing Guides

| Resource | URL |
|----------|-----|
| Year-end closing in Money S3 | [money.sk](https://www.money.sk/navod/uzavierka-roku-v-podvojnom-uctovnictve/) |
| Financial statements step-by-step | [jaspis.sk](https://jaspis.sk/aktuality/uctovna-zavierka) |
| 10 steps before closing | [podnikajte.sk](https://www.podnikajte.sk/uctovnictvo/kroky-pred-zostavenim-uctovnej-zavierky-2019) |
| Accruals (časové rozlíšenie) | [podnikajte.sk](https://www.podnikajte.sk/uctovnictvo/casove-rozlisenie-uctovanie) |
| Accruals accounting guidance (official) | [financnasprava.sk (PDF)](https://www.financnasprava.sk/_img/pfsedit/Dokumenty_PFS/Infoservis/Aktualne_informacie/dp/2017/UCT/2017_02_06_uctovanie_casoveho_rozlisenia.pdf) |
| Reserves & provisions | [podnikajte.sk](https://www.podnikajte.sk/uctovnictvo/rezervy) |

### 4.5 Fixed Assets & Depreciation

| Resource | URL |
|----------|-----|
| Depreciation guide | [moneyerp.com](https://moneyerp.com/sk-sk/ako-spravne-odpisovat-dlhodoby-majetok) |
| Depreciation groups 2025 | [podnikajte.sk](https://www.podnikajte.sk/odpisy/odpisove-skupiny-zaradenie-majetku-2025) |
| Capitalization thresholds | €1,700 tangible / €2,400 intangible (2025) |
| Acquisition, depreciation, disposal | [money.sk](https://www.money.sk/navod/dlhodoby-majetok-obstaranie-odpisy-vyradenie/) |
| Depreciation accounting guidance (official) | [33_DZPaU_2021_MU.pdf](https://www.financnasprava.sk/_img/pfsedit/Dokumenty_PFS/Zverejnovanie_dok/Dane/Metodicke_usmernenia/Priame_dane/2021/2021.09.09_33_DZPaU_2021_MU.pdf) |

---

## STAGE 5: COMPLIANCE & FUTURE (module 4)

E-invoicing, eKasa, Commercial Code — features needed for full compliance.

### 5.1 E-Invoicing (2027 Mandate)

#### Slovak Implementation

| Resource | URL | Notes |
|----------|-----|-------|
| IS eFaktúra demo portal | [web-einvoice-demo.mypaas.vnet.sk](https://web-einvoice-demo.mypaas.vnet.sk/) | Test environment |
| Official FAQ (Guide 9/DPH/2025/IM) | Via financnasprava.sk | Key implementation document |
| Accreditation rules for e-invoicing providers | [vatupdate.com](https://www.vatupdate.com/2026/02/04/slovakia-sets-accreditation-rules-for-e-invoicing-providers-ahead-of-2027-mandate/) | Feb 2026 |

#### EN 16931 / UBL / PEPPOL Standards

| Resource | URL |
|----------|-----|
| **PEPPOL BIS Billing 3.0** | [docs.peppol.eu](https://docs.peppol.eu/poacc/billing/3.0/) |
| EN 16931 format overview | [cleartax.com](https://www.cleartax.com/be/what-is-en-16931) |
| EU e-Invoicing concepts | [josemmo.github.io](https://josemmo.github.io/einvoicing/getting-started/eu-einvoicing-concepts/) |
| EU Digital Building Blocks — Slovakia | [ec.europa.eu](https://ec.europa.eu/digital-building-blocks/sites/spaces/DIGITAL/pages/467108899/eInvoicing+in+Slovakia) |

#### Timeline

- **2026**: Voluntary e-invoicing period
- **January 1, 2027**: Mandatory B2B + B2G structured e-invoicing
- **July 1, 2030**: Mandatory EU cross-border B2B
- Format: EN 16931 UBL XML via PEPPOL network (5-corner model)
- Penalties: €10,000 per violation, up to €100,000 for repeat

### 5.2 eKasa (Cash Register)

| Resource | URL | Coverage |
|----------|-----|----------|
| **Zákon č. 289/2008 Z.z. o používaní elektronickej registračnej pokladnice** | [slov-lex.sk](https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/2008/289/) | eKasa system — cash register requirements, electronic records |
| **Zákon č. 384/2025 Z.z. o evidencii tržieb** (new, from Jan 2026) | [tax-audit.sk](https://www.tax-audit.sk/en/novinky/new-act-on-revenue-recording-from-1-1-2026-what-changes-in-ekasa-and-what-are-the-new-obligations) | Replaces 289/2008, new revenue recording obligations |
| eKasa portal | [financnasprava.sk/ekasa](https://www.financnasprava.sk/sk/podnikatelia/dane/ekasa) | Main portal |
| VRP2 portal | [vrp2.financnasprava.sk](https://vrp2.financnasprava.sk/) | Virtual cash register |
| VRP2 user manual (PDF) | [VRP2 v2.0.1](https://www.financnasprava.sk/_img/pfsedit/Dokumenty_PFS/Elektronicke_sluzby/Elektronicka_komunikacia/Elektronicka_komunikacia_dane/Prirucky_navody/2023/2023.11.15_Prir_VRP2_v2.0.1.pdf) | User guide |

### 5.3 Commercial Code

| Document | URL | Coverage |
|----------|-----|----------|
| **Zákon č. 513/1991 Zb. Obchodný zákonník** (Commercial Code) | [slov-lex.sk](https://www.slov-lex.sk/ezbierky/pravne-predpisy/SK/ZZ/1991/513/) | s.r.o. requirements, financial statement deadlines |

---

## STAGE 6: REFERENCE

Professional organizations, open source, and known gaps.

### 6.1 Professional Organizations

| Organization | URL | Purpose |
|-------------|-----|---------|
| **Slovenská komora audítorov** (Auditors) | [skau.sk](https://www.skau.sk/) | Audit standards |
| **Slovenská komora daňových poradcov** (Tax Advisors) | [skdp.sk](https://www.skdp.sk/) | Tax guidance |
| **Slovenská komora certifikovaných účtovníkov** | [skcu.sk](https://skcu.sk/) | Accountant certification |
| **JASPIS** (Training) | [jaspis.sk](https://jaspis.sk/) | Accounting courses (80h double-entry course) |

### 6.2 Open Source References

| Resource | URL | Notes |
|----------|-----|-------|
| Daňové priznanie Digital (DPFO) | [github.com/slovensko-digital](https://github.com/slovensko-digital/priznanie-digital) | Open source tax return project |
| Tatra banka PHP API wrapper | github.com/pavolbiely/tatrabanka-api | Community PSD2 integration |

### 6.3 Top Resources (ranked by usefulness for knowledge graph)

1. **Opatrenie 23054/2002-92 (Postupy účtovania)** — THE source of all booking rules
2. **danovecentrum.sk** — Best worked examples for DPH and all transaction types
3. **ako-uctovat.sk** — Predkontácie (standard booking patterns) for every common scenario
4. **podnikajte.sk** — Comprehensive topic articles with current-year specifics
5. **money.sk/navod/** — Step-by-step guides matching real software workflows
6. **financnasprava.sk XSD schemas** — Technical specs for all filing formats
7. **PEPPOL BIS Billing 3.0** — E-invoicing technical standard
8. **socpoist.sk + vszp.sk** — Official payroll/insurance rates and reporting specs

### 6.4 Known Gaps (require direct contact or login)

These resources exist but are not publicly documented or require registration:

| Resource | Status | How to obtain |
|----------|--------|---------------|
| Finančná správa submission API (SOAP/REST) | Not publicly documented | Contact FS technical support |
| registeruz.sk submission API | Requires registration | Apply for access at registeruz.sk |
| eKasa integration API specs | Behind login | Register as eKasa integrator at financnasprava.sk |
| Obchodný register API | No public API | Use web scraping or finstat.sk as proxy |
| Sociálna poisťovňa electronic reporting format | Requires employer registration | Register at esluzby.socpoist.sk |
