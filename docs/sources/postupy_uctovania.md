# Postupy uctovania pre podnikatelov
# (Opatrenie MF SR c. 23054/2002-92 v zneni neskorsich predpisov)

**Source:** Financna sprava SR — official full text (98 pages)
**Last amendment:** Opatrenie c. MF/014948/2024-74 (effective 1.1.2025)
**Scope:** Entrepreneurs (podnikatelia) using double-entry bookkeeping (podvojne uctovnictvo)
**Extracted:** 2026-03-13 for Slovak AI Accountant project

---

## Structure Overview

| Part | Sections | Topic |
|------|----------|-------|
| Part 1 | §1-§30f | General provisions + special operations |
| Part 2 | §31-§84 | Account classes 0-7 (detailed booking rules) |
| Part 3 | §84-§85 | Closing accounts + off-balance sheet |
| Part 4 | §85a-§86n | Transitional provisions (EUR conversion, amendments) |
| Part 5 | §87-§88 | Repealing + effectiveness |
| Appendix 1 | — | Ramcova uctova osnova (Chart of accounts framework) |
| Appendix 2 | — | EU directives list |

---

## PART 1: GENERAL PROVISIONS (§1 — §30f)

### §1 — Scope
Applies to entrepreneurs (podnikatelia) accounting in the double-entry system per Act 431/2002 Coll.

### §2 — Accounting Date (Den uctovneho pripadu)
The day when a receivable, liability, expense, revenue, asset movement, or equity change occurs that must be recorded. Also includes dates per special regulations (commercial register entries, etc.).

### §3 — Accounting Books
- **Dennik** (Journal) — chronological record of all entries
- **Hlavna kniha** (General ledger) — synoptic accounts with turnovers and balances
- **General ledger content per account:** opening balance, debit/credit turnovers, closing balance

### §4 — Chart of Accounts
- Each entity creates its own chart based on the framework chart (Appendix 1)
- Synoptic accounts = 3-digit codes from framework
- Analytical accounts = subdivisions of synoptic accounts for: types, locations, responsible persons, tax purposes
- Account 431 must have analytics for: profit distribution, loss coverage, dividends, tantiemy

### §5 — Accrual Accounting (Casove rozlisenie)
**Accounts used:**
- **381** — Naklady buducich obdobi (Prepaid expenses)
- **382** — Komplexne naklady buducich obdobi (Complex prepaid expenses)
- **383** — Vydavky buducich obdobi (Accrued expenses)
- **384** — Vynosy buducich obdobi (Deferred revenue)
- **385** — Primy buducich obdobi (Accrued revenue)

**Key rules:**
- Micro entities do not need accruals for immaterial recurring items between two periods
- Small and large entities must accrue; exception for immaterial recurring items of last/first month only

### §6 — Internal Accounting (Vnutorne zuctovanie)
Account 395 — used for internal settlements between organizational units within the entity.

### §7 — Opening Books (Otvaranie uctovnych knih)
**Booking pattern:**
- Assets: Debit asset account / Credit 701 (Zaciatocny ucet suvahovy)
- Liabilities + Equity: Debit 701 / Credit liability/equity account

### §8 — Closing Books (Uzavieranie uctovnych knih)
**Booking pattern:**
- Expense accounts close: Debit 710 (Ucet ziskov a strat) / Credit expense account
- Revenue accounts close: Debit revenue account / Credit 710
- Asset accounts close: Debit 702 (Konecny ucet suvahovy) / Credit asset account
- Liability/Equity accounts close: Debit liability/equity account / Credit 702
- Profit: Debit 710 / Credit 702
- Loss: Debit 702 / Credit 710

### §9 — Profit Determination
Profit/loss = Revenue - Expenses, adjusted for income tax. Result transfers to account 431 at opening of next period.

### §10 — Income Tax Accounting
**Accounts:**
- **341** — Dan z prijmov (Income tax)
- **591** — Splatna dan z prijmov (Current income tax)
- **592** — Odlozena dan z prijmov (Deferred income tax)
- **481** — Odlozeny danovy zavazok a odlozena danova pohladavka

**Booking patterns:**
- Current tax: Debit 591 / Credit 341
- Closing: Debit 341 / Credit 591 (via 591 on 341)
- Deferred tax liability: Debit 592 / Credit 481
- Deferred tax asset: Debit 481 / Credit 592
- **Dorovnavacia dan (top-up tax from 1.1.2025):** also on accounts 341, 591, account class 59

### §11 — Inventory Differences (Inventarizacne rozdiely)
**Surplus:**
- Long-term tangible assets: Credit to account 07x/08x (accumulated depreciation) at replacement cost
- Inventories: Credit to account class 1 (inventory) matched to relevant revenue/internal account
- Financial assets: per §14

**Shortage (manko):**
- Up to natural loss limits: Debit 501 (Spotreba materialu) or 504 (Predany tovar)
- Above natural loss: Debit 549 (Manka a skody)
- Long-term assets: Debit 549 / Credit asset (via accumulated depreciation)

### §12 — Long-term vs Short-term Classification
- Short-term = maturity <= 1 year from balance sheet date
- Long-term = maturity > 1 year
- Exception: bank loans classified by original maturity term

### §13 — Current / Non-current Reclassification
Long-term items within 1 year of maturity reclassify to short-term (e.g., long-term receivable becoming current).

### §14 — Securities Accounting
**Categories:** held-to-maturity, trading, available-for-sale, subsidiaries/associates
**Revaluation:** fair value changes to 414 (Ocenovacie rozdiely) or through P&L (564/664)

### §15 — Bills of Exchange (Zmenky)
Receivable bills: account 312 or 313. Payable bills: account 322.
Discount on escont: through 562 (Uroky).

### §16 — Derivatives
Accounted per separate rules. Fair value changes through P&L (567/667) or to 414.

### §17 — Short-term Asset Classification
Current assets include inventory, receivables, financial accounts, accruals.

### §18 — Allowances (Opravne polozky)
**Creation booking patterns:**
- To receivables: Debit 547 / Credit 391
- To inventories: Debit 505 / Credit 19x
- To long-term intangible assets: Debit 553 / Credit 09x (091-097)
- To long-term tangible assets: Debit 553 / Credit 09x
- To financial assets: Debit 565 / Credit 09x (096)

**Release/utilization:** reverse the above entries

### §19 — Reserves (Rezervy)
**Creation:** Debit 548 (Ostatne naklady) or relevant expense / Credit 323 (Kratkodobe rezervy) or 451 (Rezervy zakonne)
**Usage:** Debit 323 or 451 / Credit relevant account
**Statutory reserves (451):** legally required reserves
**Short-term reserves (323):** expected obligations within 1 year

### §20 — Depreciation (Odpisy)
**Booking pattern:** Debit 551 / Credit 07x (intangible) or 08x (tangible)
- Account 07x — Opravky k dlhodobemu nehmotnemu majetku
- Account 08x — Opravky k dlhodobemu hmotnemu majetku
- Depreciation starts month after asset is put into use
- Methods: straight-line or accelerated (per tax law)

### §21 — Long-term Asset Valuation
Acquisition cost includes: purchase price + transport + installation + customs + non-deductible VAT.
Own creation cost: direct costs + production overhead.

### §22-§23 — Inventory Valuation
- Purchased inventory: acquisition cost (purchase price + ancillary costs)
- Own production: own cost of production
- FIFO or weighted average for consumption

### §24 — Currency Differences (Kurzove rozdiely)
**Accounts:**
- **563** — Kurzove straty (FX losses) — expense
- **663** — Kurzove zisky (FX gains) — revenue

**When recognized:** at payment date, at balance sheet date, at any settlement date
- Loss: Debit 563 / Credit receivable or Debit payable / Credit 563... (various patterns)
- Gain: opposite direction through 663

### §25 — Equity Changes (Zmeny vlastneho imania)
**Account 411** — Zakladne imanie (Share capital)
**Account 419** — Zmeny zakladneho imania (Changes in share capital)
**Account 417** — Zakonny rezervny fond z kapitalovych vkladov
**Account 418** — Nedelitelny fond z kapitalovych vkladov

### §26-§29 — Special Operations
- §26: Transformations (mergers, demergers)
- §27: Business sale
- §28: Liquidation
- §29: Bankruptcy

### §30a — Financial Leasing
**Lessee booking:**
- Recognition: Debit 042 (Obstaranie DHM) / Credit 474 (Zavazky z najmu) — at present value of payments
- Activation: Debit 02x / Credit 042
- Lease payment: Debit 474 / Credit 221 (principal) + Debit 562 / Credit 221 (interest)
- Lessor: recognizes sale via 641 (Trzby z predaja) and receivable 374 (Pohladavky z najmu)

### §30b — Emission Quotas
Gratuitous quotas at fair value. Trading quotas at cost. Sold via 541/641.

### §30c — Concessions (Service Concession Arrangements)
Infrastructure accounted based on control conditions.

### §30d — Real Estate Construction for Sale
Accounted on 133 (Nehnutelnost na predaj) when built for sale purpose.

### §30e — Energy Services (ESCO)
Specific rules for energy performance contracting.

### §30f — Utility Tokens (from 1.1.2025)
Crypto-assets that are utility tokens — specific accounting treatment added by amendment MF/014948/2024-74.

---

## PART 2: ACCOUNT CLASSES (§31 — §84)

### §31 — Account Classes Overview
| Class | Name | Type |
|-------|------|------|
| 0 | Dlhodoby majetok (Long-term assets) | Balance sheet |
| 1 | Zasoby (Inventories) | Balance sheet |
| 2 | Financne ucty (Financial accounts) | Balance sheet |
| 3 | Zuctovacie vztahy (Settlement relationships) | Balance sheet |
| 4 | Kapitalove ucty a dlhodobe zavazky (Capital + LT liabilities) | Balance sheet |
| 5 | Naklady (Expenses) | P&L |
| 6 | Vynosy (Revenues) | P&L |
| 7 | Uzavierkove ucty a podsuvahove ucty (Closing + off-balance) | Technical |

---

### CLASS 0: LONG-TERM ASSETS (§32-§42)

#### §32 — Content
Long-term intangible assets, tangible assets, financial assets, accumulated depreciation, allowances.

#### §33-§35 — Acquisition of Long-term Assets

**Purchase from supplier:**
- Intangible: Debit 041 / Credit 321 (then activate: Debit 01x / Credit 041)
- Tangible: Debit 042 / Credit 321 (then activate: Debit 02x / Credit 042)
- Financial: Debit 043 / Credit 321 (then: Debit 06x / Credit 043)

**VAT on purchase (if deductible):** Debit 343 / Credit 321

**Own creation (self-built):**
- Intangible: Debit 041 / Credit 623 (Aktivacia DNM), then Debit 01x / Credit 041
- Tangible: Debit 042 / Credit 624 (Aktivacia DHM), then Debit 02x / Credit 042

**Advance payments:**
- Debit 051/052/053 / Credit 221 (advance paid)
- When invoice received: Debit 04x / Credit 321, then Debit 321 / Credit 051/052/053

#### §36 — Disposal of Long-term Assets

**Sale:**
- Net book value to expense: Debit 541 / Credit 07x or 08x (depreciation reversal) + Debit 07x or 08x / Credit 01x or 02x
- Revenue: Debit 311 or 315 / Credit 641

**Scrapping (fully depreciated):**
- Debit 551 / Credit 07x or 08x (any remaining depreciation)
- Debit 07x or 08x / Credit 01x or 02x

**Donation:**
- Debit 543 (Dary) / Credit 07x or 08x + Debit 07x or 08x / Credit 01x or 02x

**Shortage/damage:**
- Debit 549 (Manka a skody) / Credit 07x or 08x + Debit 07x or 08x / Credit 01x or 02x

**Transfer to personal use (sole trader):**
- Debit 491 / Credit 07x or 08x + Debit 07x or 08x / Credit 01x or 02x

#### §37 — Intangible Assets (DNM)
- **012** — Aktivovane naklady na vyvoj (Capitalized development costs)
- **013** — Softver
- **014** — Ocenitelne prava (Valuable rights, licenses)
- **015** — Goodwill
- **019** — Ostatny dlhodoby nehmotny majetok

Amortized over economic useful life. Goodwill max 5 years (can extend if justified).

#### §38 — Tangible Assets (DHM)
- **021** — Stavby (Buildings)
- **022** — Samostatne hnutelne veci a subory hnutelnych veci (Equipment)
- **025** — Pestovatelske celky trvalych porastov (Permanent crops)
- **026** — Zakladne stado a tazne zvierata (Livestock)
- **029** — Ostatny dlhodoby hmotny majetok
- **031** — Pozemky (Land) — NOT depreciated
- **032** — Umelecke diela a zbierky (Art) — NOT depreciated

#### §39-§42 — Long-term Financial Assets
- **061** — Podielove cenne papiere v dcerskej jednotke (Shares in subsidiaries)
- **062** — Podielove CP v spolocnosti s podielovou ucastou
- **063** — Realizovatelne CP a podiely
- **065** — Dlhove CP drzane do splatnosti
- **066** — Pozicky prepojenym jednotkam
- **067** — Ostatne pozicky
- **069** — Ostatny DFM

---

### CLASS 1: INVENTORIES (§43-§45)

#### Two Methods:

**Method A (perpetual):**
- Purchase: Debit 111 (Obstaranie materialu) / Credit 321
- Receipt to warehouse: Debit 112 (Material na sklade) / Credit 111
- Consumption: Debit 501 (Spotreba materialu) / Credit 112

**Method B (periodic):**
- Purchase: Debit 501 / Credit 321 (directly to expense)
- At year-end: opening stock reversal Debit 501 / Credit 112; closing stock: Debit 112 / Credit 501

**Goods (tovar):**
- Method A: 131 → 132 → 504
- Method B: direct to 504

**Own production:**
- 121 — Nedokoncena vyroba (WIP)
- 122 — Polotovary vlastnej vyroby
- 123 — Vyrobky (Finished goods)
- 124 — Zvierata

**Changes in own production inventory:** through accounts 611-614

**Allowances to inventories:**
- Creation: Debit 505 / Credit 19x (191-196)
- Release: reverse

---

### CLASS 2: FINANCIAL ACCOUNTS (§46-§47)

- **211** — Pokladnica (Cash register)
- **213** — Ceniny (Stamps, vouchers)
- **221** — Bankove ucty (Bank accounts)
- **231** — Kratkodobe bankove uvery (Short-term bank loans)
- **232** — Eskontne uvery
- **241** — Vydane kratkodobe dlhopisy
- **249** — Ostatne kratkodobe financne vypomoci
- **251** — Majetkove CP na obchodovanie (Trading securities)
- **253** — Dlhove CP na obchodovanie
- **255** — Vlastne dlhopisy
- **256** — Dlhove CP so splatnostou do 1 roka
- **261** — Peniaze na ceste (Money in transit)

**Key booking patterns:**
- Cash receipt: Debit 211 / Credit 261 or revenue account
- Cash payment: Debit expense or 321 / Credit 211
- Bank receipt: Debit 221 / Credit 261 or revenue account
- Bank payment: Debit expense or 321 / Credit 221
- Transfer cash→bank: Debit 261 / Credit 211, then Debit 221 / Credit 261

---

### CLASS 3: SETTLEMENT RELATIONSHIPS (§48-§57)

#### §49 — Receivables (Pohladavky)
- **311** — Odberatelia (Trade receivables — customer invoices)
- **312** — Zmenky na inkaso (Bills receivable)
- **313** — Pohladavky za eskontovane CP
- **314** — Poskytnutne preddavky (Advances given)
- **315** — Ostatne pohladavky
- **316** — Cista hodnota zakazky

**Customer invoice:** Debit 311 / Credit 601/602/604 + Debit 311 / Credit 343 (DPH)

#### §50 — Payables (Zavazky)
- **321** — Dodavatelia (Trade payables — supplier invoices)
- **322** — Zmenky na uhradu
- **323** — Kratkodobe rezervy
- **324** — Prijate preddavky (Advances received)
- **325** — Ostatne zavazky
- **326** — Nevyfakturovane dodavky (Uninvoiced deliveries)

**Supplier invoice:** Debit 5xx (expense) / Credit 321 + Debit 343 / Credit 321 (input VAT)

#### §51 — Employees and Social Insurance
- **331** — Zamestnanci (Employees — net wages payable)
- **333** — Ostatne zavazky voci zamestnancom
- **335** — Pohladavky voci zamestnancom
- **336** — Zuctovanie s organmi SP a ZP (Social/health insurance)

**Payroll booking pattern:**
- Gross wages: Debit 521 (Mzdove naklady) / Credit 331
- Employee's insurance deductions: Debit 331 / Credit 336
- Employee's income tax: Debit 331 / Credit 342
- Employer's insurance: Debit 524 (Zakonne socialne poistenie) / Credit 336
- Net wage payment: Debit 331 / Credit 221

#### §52 — Taxes and Subsidies

**Income tax (341):**
- Advance payment: Debit 341 / Credit 221
- Year-end liability: Debit 591 / Credit 341
- Overpayment: Debit 341 / Credit receivable

**Other direct taxes (342):**
- Withholding tax on wages: Debit 331 / Credit 342
- Payment to tax office: Debit 342 / Credit 221

**VAT — DPH (343):**
- Output VAT (sale): Debit 311 / Credit 343
- Input VAT (purchase — deductible): Debit 343 / Credit 321
- VAT liability to pay: balance of 343 credit side > debit side
- VAT claim for refund: balance of 343 debit side > credit side
- VAT where no deduction right: included in cost of asset/expense (not on 343)
- VAT on acquisition of goods from EU: Debit 343 analytical / Credit 343 analytical (self-assessment)
- Prorated VAT deduction: non-deductible portion to expense (548) or revenue (648)
- Theft with VAT adjustment: Debit 549 / Credit 343

**Other taxes and fees (345):**
- Motor vehicle tax (531), real estate tax (532), other taxes
- Fees: Debit 538 / Credit 345, payment: Debit 345 / Credit 221

**Dorovnavacia dan (top-up tax, from 1.1.2025):**
- Accounted on 341 and 591 per amended §52 ods. 1 and §67 ods. 1

#### §52a — Subsidies and Grants (Dotacie)
- **346** — Dotacie zo statneho rozpoctu (State budget grants)
- **347** — Ostatne dotacie (Other grants)
- **384** — Vynosy buducich obdobi (for deferred grant recognition)

**Grant for asset purchase:**
- Receipt: Debit 221 / Credit 346 or 347
- If conditions met simultaneously: directly to revenue (648)
- If conditions over time: Debit 346/347 / Credit 384, then release to 648 over depreciation period

**Grant for expense reimbursement:**
- Directly to revenue (648) in the period of compensated expense

#### §52b — Sponsorship (Sponzorske)
- Received: Debit 347 / Credit 648 or 384
- Asset-related: released over useful life from 384 to 648

#### §53 — Receivables/Payables to Partners (Spolocnici, Clenovia)
- **351** — Pohladavky voci prepojenym uctovnym jednotkam
- **353** — Pohladavky za upisane vlastne imanie
- **354** — Pohladavky voci spolocnikovi pri uhrade straty
- **355** — Ostatne pohladavky voci spolocnikovi a clenom
- **358** — Pohladavky voci ucastnikom zdruzenia

#### §54 — Payables to Partners
- **361** — Zavazky voci prepojenym uctovnym jednotkam
- **364** — Zavazky voci spolocnikovi pri rozdelovani zisku
- **365** — Ostatne zavazky voci spolocnikovi a clenom
- **366** — Zavazky voci spolocnikovi zo zavislej cinnosti
- **367** — Zavazky z upisanych nespatenych CP a vkladov
- **368** — Zavazky voci ucastnikom zdruzenia

**Profit distribution:** Debit 431 / Credit 364 (dividends) + Debit 431 / Credit 421 (reserve fund)

#### §55 — Other Receivables and Payables
- **371** — Pohladavky z predaja podniku
- **372** — Zavazky z kupy podniku
- **373** — Pohladavky/zavazky z terminovych operacii (§16)
- **374** — Pohladavky z najmu (lessor leasing receivable)
- **375** — Pohladavky z vydanych dlhopisov
- **376** — Nakupene opcie
- **377** — Predane opcie
- **378** — Ine pohladavky
- **379** — Ine zavazky

#### §56 — Accruals (Casove rozlisenie)
- **381** — Naklady buducich obdobi (prepaid expenses, e.g. rent paid in advance)
- **382** — Komplexne naklady buducich obdobi
- **383** — Vydavky buducich obdobi (accrued expenses)
- **384** — Vynosy buducich obdobi (deferred revenue)
- **385** — Primy buducich obdobi (accrued revenue)

**Rules for micro/small entities:** can skip accruals for immaterial, recurring items.

#### §57 — Allowances to Receivables
- **391** — Opravne polozky k pohladavkam
- Creation: Debit 547 / Credit 391
- Release: Debit 391 / Credit 547
- Write-off of receivable: Debit 546 (Odpis pohladavok) + Debit 391 / Credit 311 (or other receivable)

---

### CLASS 4: CAPITAL AND LONG-TERM LIABILITIES (§58-§62)

#### §58 — Content
Equity, funds, reserves, long-term bank loans, long-term payables, deferred tax, sole trader equity.

#### §59 — Equity (Vlastne imanie)
- **411** — Zakladne imanie (Share capital)
- **412** — Emisne azio (Share premium)
- **413** — Ostatne kapitalove fondy
- **414** — Ocenovacie rozdiely z precenenia majetku a zavazkov
- **415** — Ocenovacie rozdiely z kapitalovych ucastin
- **416** — Ocenovacie rozdiely pri zluceni, splyunti a rozdeleni
- **417** — Zakonny rezervny fond z kapitalovych vkladov
- **418** — Nedelitelny fond z kapitalovych vkladov
- **419** — Zmeny zakladneho imania (Changes in share capital — temporary)

#### Funds from Profit
- **421** — Zakonny rezervny fond
- **422** — Nedelitelny fond
- **423** — Statutarne fondy
- **427** — Ostatne fondy
- **428** — Nerozdeleny zisk minulych rokov (Retained earnings)
- **429** — Neuhradena strata minulych rokov (Accumulated losses)

#### §59 ods. 15 — Profit Distribution (account 431)
- **431** — Vysledok hospodarenia v schvalovani
- Dividends: Debit 431 / Credit 364
- Reserve fund: Debit 431 / Credit 421
- Retained earnings: Debit 431 / Credit 428
- Loss carry forward: Debit 429 / Credit 431

#### §60 — Reserves
- **451** — Rezervy zakonne (Statutory reserves)
- **459** — Ostatne rezervy (Other reserves)

#### §61 — Long-term Bank Loans
- **461** — Bankove uvery (Long-term bank loans)

#### Long-term Payables
- **471** — Dlhodobe zavazky voci prepojenym uctovnym jednotkam
- **472** — Zavazky zo socialneho fondu
- **473** — Vydane dlhopisy
- **474** — Zavazky z najmu (Lease liabilities)
- **475** — Dlhodobe prijate preddavky
- **476** — Dlhodobe nevyfakturovane dodavky
- **478** — Dlhodobe zmenky na uhradu
- **479** — Ostatne dlhodobe zavazky

#### §61 ods. 13 — Deferred Tax
- **481** — Odlozeny danovy zavazok a odlozena danova pohladavka

#### §62 — Sole Trader Equity
- **491** — Vlastne imanie fyzickej osoby — podnikatela
- Can have debit (asset) or credit (liability) balance
- All personal deposits, withdrawals, profit/loss flow through this account

---

### CLASS 5: EXPENSES (§63-§73)

#### §63 — General Rules
Expenses in class 5 are primary and secondary costs. Recorded on accrual basis from start of period.

#### §64 — Account Group 50: Consumed Purchases
- **501** — Spotreba materialu (Material consumption)
  - Method A: Debit 501 / Credit 112
  - Method B: Debit 501 / Credit 321 (direct)
- **502** — Spotreba energie (Energy consumption)
- **503** — Spotreba ostatnych neskladovatelnych dodavok
- **504** — Predany tovar (Cost of goods sold)
- **505** — Tvorba a zuctovanie opravnych poloziek k zasobam (Allowances to inventories)
- **507** — Predana nehnutelnost (Sold real estate — construction for sale)

#### §65 — Account Group 51: Services
- **511** — Opravy a udrzivanie (Repairs and maintenance)
- **512** — Cestovne (Travel expenses)
- **513** — Naklady na reprezentaciu (Representation/entertainment)
- **518** — Ostatne sluzby (Other services — rent, postal, consulting, etc.)

#### §66 — Account Group 52: Personnel Costs
- **521** — Mzdove naklady (Wages and salaries)
- **522** — Prijmy spolocnikov a clenov zo zavislej cinnosti
- **523** — Odmeny clenom organov spolocnosti a druzstva
- **524** — Zakonne socialne poistenie (Statutory social insurance — employer's portion)
- **525** — Ostatne socialne poistenie
- **526** — Socialne naklady FO — podnikatela
- **527** — Zakonne socialne naklady (Statutory social costs — meal vouchers, social fund)
- **528** — Ostatne socialne naklady

**Payroll wages always in gross amounts.** Gross wage = net + employee deductions.

#### §67 — Account Group 53: Taxes and Fees
- **531** — Dan z motorovych vozidiel (Motor vehicle tax)
- **532** — Dan z nehnutelnosti (Real estate tax)
- **538** — Ostatne dane a poplatky (Other taxes and fees)
  - From 1.1.2025: also includes **dan z financnych transakcii** (financial transaction tax)

#### §68 — Account Group 54: Other Operating Expenses
- **541** — Zostatkova cena predaneho DHM a DNM (NBV of sold long-term assets)
- **542** — Predany material (Sold material at cost)
- **543** — Dary (Donations given)
- **544** — Zmluvne pokuty, penale a uroky z omeskania (Contractual penalties)
- **545** — Ostatne pokuty, penale a uroky z omeskania
- **546** — Odpis pohladavok (Receivable write-offs)
- **547** — Tvorba a zuctovanie opravnych poloziek k pohladavkam
- **548** — Ostatne naklady na hospodarsku cinnost (Other operating expenses)
- **549** — Manka a skody (Shortages and damages)

#### §69 — Account Group 55: Depreciation and Allowances to LT Assets
- **551** — Odpisy DNM a DHM (Depreciation of intangible and tangible assets)
- **553** — Tvorba a zuctovanie opravnych poloziek k DM (Allowances to LT assets)
- **555** — Zuctovanie komplexnych nakladov buducich obdobi
- **557** — Zuctovanie opravky k opravnej polozke k nadobudnutemu majetku

#### §70 — Account Group 56: Financial Expenses
- **561** — Predane CP a podiely (Sold securities — cost)
- **562** — Uroky (Interest expense)
- **563** — Kurzove straty (Foreign exchange losses)
- **564** — Naklady na precenenie CP (Revaluation losses on securities)
- **565** — Tvorba a zuctovanie opravnych poloziek k financnemu majetku
- **566** — Naklady na kratkodoby financny majetok
- **567** — Naklady na derivatove operacie
- **568** — Ostatne financne naklady (Other financial expenses — bank fees, etc.)
- **569** — Manka a skody na financnom majetku

#### §73 — Account Group 59: Income Tax and Transfers
- **591** — Splatna dan z prijmov (Current income tax expense)
- **592** — Odlozena dan z prijmov (Deferred income tax expense)
- **595** — Dodatocne odvody dane z prijmov
- **596** — Prevod podielov na vysledku hospodarenia spolocnikom

**Closing:** All class 5 accounts close to 710 (Ucet ziskov a strat).

---

### CLASS 6: REVENUES (§74-§80)

#### §74 — General Rules
Revenues in class 6 recorded on accrual basis. VAT (DPH) from sales recognized as credit to 343.
Revenue discounts reduce revenue.

#### §75 — Account Group 60: Sales Revenue
- **601** — Trzby za vlastne vyrobky (Revenue from own products)
- **602** — Trzby z predaja sluzieb (Revenue from services)
- **604** — Trzby za tovar (Revenue from goods sold)
- **606** — Vynosy zo zakazky (Contract revenue)
- **607** — Vynosy z nehnutelnosti na predaj

**Sale booking:** Debit 311 / Credit 601/602/604 (net) + Debit 311 / Credit 343 (DPH)
**Cash sale:** Debit 211 / Credit 601/602/604 + DPH

#### §76 — Account Group 61: Changes in Internal Inventories
- **611** — Zmena stavu nedokoncenej vyroby (Change in WIP)
- **612** — Zmena stavu polotovarov
- **613** — Zmena stavu vyrobkov
- **614** — Zmena stavu zvierat

#### §77 — Account Group 62: Activation
- **621** — Aktivacia materialu a tovaru (Activation of material/goods)
- **622** — Aktivacia vnutroorganizacnych sluzieb (Activation of internal services)
- **623** — Aktivacia dlhodobeho nehmotneho majetku (Activation of intangible assets)
- **624** — Aktivacia dlhodobeho hmotneho majetku (Activation of tangible assets)

**Self-built tangible asset:** Debit 042 / Credit 624, then Debit 02x / Credit 042

#### §78 — Account Group 64: Other Operating Revenue
- **641** — Trzby z predaja DNM a DHM (Revenue from sale of LT assets)
- **642** — Trzby z predaja materialu
- **644** — Zmluvne pokuty, penale a uroky z omeskania (Contractual penalties received)
- **645** — Ostatne pokuty, penale a uroky z omeskania
- **646** — Vynosy z odpisanych pohladavok (Revenue from written-off receivables recovered)
- **648** — Ostatne vynosy z hospodarskej cinnosti (Other operating revenue)

#### §79 — Account Group 65: Allowance Releases
- **655** — Zuctovanie komplexnych nakladov buducich obdobi
- **657** — Zuctovanie opravky k opravnej polozke k nadobudnutemu majetku

#### §80 — Account Group 66: Financial Revenue
- **661** — Trzby z predaja CP a podielov (Revenue from sale of securities)
- **662** — Uroky (Interest revenue)
- **663** — Kurzove zisky (Foreign exchange gains)
- **664** — Vynosy z precenenia CP (Revaluation gains on securities)
- **665** — Vynosy z dlhodobeho financneho majetku (Revenue from LT financial assets — dividends)
- **666** — Vynosy z kratkodobeho financneho majetku
- **667** — Vynosy z derivatovych operacii
- **668** — Ostatne financne vynosy (Other financial revenue)
  - From 1.1.2025: includes **kryptoaktivum** acquired through validation in crypto-asset network

**Closing:** All class 6 accounts close to 710 (Ucet ziskov a strat).

---

### CLASS 7: CLOSING AND OFF-BALANCE SHEET ACCOUNTS (§84-§85)

#### §84 — Closing Accounts (Uzavierkove ucty)
- **701** — Zaciatocny ucet suvahovy (Opening balance sheet account)
- **702** — Konecny ucet suvahovy (Closing balance sheet account)
- **710** — Ucet ziskov a strat (Profit and loss account)
- **711** — Zaciatocny ucet nakladov a vynosov (used for interim financial statements with EUR conversion)

#### §85 — Off-Balance Sheet Accounts (Podsuvahove ucty)
Track items not in balance sheet but important for financial position assessment:
a) received deposits and mortgages
b) leased-out assets
c) assets in custody
d) inventory received for processing
e) bills used for payment until maturity
f) strict accountability forms
g) civil defense material
h) program 222
i) leasing liabilities
j) leasing receivables
k) purchased options receivables
l) options liabilities
m) written-off receivables
n) **crypto-assets acquired through validation** (from 1.1.2025)

---

## APPENDIX 1: RAMCOVA UCTOVA OSNOVA PRE PODNIKATELOV
## (Framework Chart of Accounts for Entrepreneurs)

### Class 0 — Long-term Assets
| Code | Name (SK) | Name (EN) |
|------|-----------|-----------|
| 01 | Dlhodoby nehmotny majetok | Long-term intangible assets |
| 012 | Aktivovane naklady na vyvoj | Capitalized development costs |
| 013 | Softver | Software |
| 014 | Ocenitelne prava | Valuable rights |
| 015 | Goodwill | Goodwill |
| 019 | Ostatny DNM | Other intangible assets |
| 02 | Dlhodoby hmotny majetok — odpisovany | Tangible assets — depreciable |
| 021 | Stavby | Buildings |
| 022 | Samostatne hnutelne veci a subory hnutelnych veci | Equipment and sets |
| 025 | Pestovatelske celky trvalych porastov | Permanent crops |
| 026 | Zakladne stado a tazne zvierata | Livestock |
| 029 | Ostatny DHM | Other tangible assets |
| 03 | DHM — neodpisovany | Tangible — non-depreciable |
| 031 | Pozemky | Land |
| 032 | Umelecke diela a zbierky | Art and collections |
| 04 | Obstaranie dlhodobeho majetku | Acquisition of LT assets |
| 041 | Obstaranie DNM | Acquisition of intangible |
| 042 | Obstaranie DHM | Acquisition of tangible |
| 043 | Obstaranie DFM | Acquisition of financial |
| 05 | Poskytnutne preddavky na DM | Advances for LT assets |
| 051 | Preddavky na DNM | Advances for intangible |
| 052 | Preddavky na DHM | Advances for tangible |
| 053 | Preddavky na DFM | Advances for financial |
| 06 | Dlhodoby financny majetok | Long-term financial assets |
| 061 | Podielove CP v dcerskej jednotke | Shares in subsidiaries |
| 062 | Podielove CP v spolocnosti s podielovou ucastou | Shares in associates |
| 063 | Realizovatelne CP a podiely | Available-for-sale securities |
| 065 | Dlhove CP drzane do splatnosti | Held-to-maturity debt securities |
| 066 | Pozicky prepojenym jednotkam | Loans to related entities |
| 067 | Ostatne pozicky | Other loans |
| 069 | Ostatny DFM | Other LT financial assets |
| 07 | Opravky k DNM | Accumulated amortization — intangible |
| 071 | Opravky k DNM | (generic) |
| 072 | Opravky k aktivovanym nakladom na vyvoj | Amort. — development costs |
| 073 | Opravky k softveru | Amort. — software |
| 074 | Opravky k ocenitelnym pravam | Amort. — valuable rights |
| 075 | Opravky ku goodwillu | Amort. — goodwill |
| 079 | Opravky k ostatnemu DNM | Amort. — other intangible |
| 08 | Opravky k DHM | Accumulated depreciation — tangible |
| 081 | Opravky k stavbam | Depr. — buildings |
| 082 | Opravky k samostatnym hnutelnym veciam | Depr. — equipment |
| 085 | Opravky k pestovatelskym celkom | Depr. — permanent crops |
| 086 | Opravky k zakladnemu stadu | Depr. — livestock |
| 089 | Opravky k ostatnemu DHM | Depr. — other tangible |
| 09 | Opravne polozky k DM | Allowances to LT assets |
| 091 | OP k dlhodobemu nehmotnemu majetku | Allowance — intangible |
| 092 | OP k dlhodobemu hmotnemu majetku | Allowance — tangible |
| 093 | OP k nedokoncenemu DNM | Allowance — WIP intangible |
| 094 | OP k nedokoncenemu DHM | Allowance — WIP tangible |
| 095 | OP k poskytnutym preddavkom na DM | Allowance — advances |
| 096 | OP k dlhodobemu financnemu majetku | Allowance — financial |
| 097 | OP k nadobudnutemu majetku | Allowance — acquired assets |
| 098 | Opravky k opravnej polozke k nadobudnutemu majetku | Amort. of allowance — acquired |

### Class 1 — Inventories
| Code | Name (SK) | Name (EN) |
|------|-----------|-----------|
| 11 | Material | Material |
| 111 | Obstaranie materialu | Procurement of material |
| 112 | Material na sklade | Material in warehouse |
| 119 | Material na ceste | Material in transit |
| 12 | Zasoby vlastnej vyroby | Own production inventory |
| 121 | Nedokoncena vyroba | Work in progress |
| 122 | Polotovary vlastnej vyroby | Semi-finished products |
| 123 | Vyrobky | Finished products |
| 124 | Zvierata | Animals |
| 13 | Tovar | Goods |
| 131 | Obstaranie tovaru | Procurement of goods |
| 132 | Tovar na sklade a v predajniach | Goods in warehouse/shops |
| 133 | Nehnutelnost na predaj | Real estate for sale |
| 139 | Tovar na ceste | Goods in transit |
| 19 | Opravne polozky k zasobam | Allowances to inventories |
| 191 | OP k materialu | Allowance — material |
| 192 | OP k nedokoncenej vyrobe | Allowance — WIP |
| 193 | OP k polotovarom | Allowance — semi-finished |
| 194 | OP k vyrobkom | Allowance — finished |
| 195 | OP k zvieratam | Allowance — animals |
| 196 | OP k tovaru | Allowance — goods |

### Class 2 — Financial Accounts
| Code | Name (SK) | Name (EN) |
|------|-----------|-----------|
| 21 | Peniaze | Cash |
| 211 | Pokladnica | Cash register |
| 213 | Ceniny | Stamps/vouchers |
| 22 | Ucty v bankach | Bank accounts |
| 221 | Bankove ucty | Bank accounts |
| 23 | Bezne bankove uvery | Current bank loans |
| 231 | Kratkodobe bankove uvery | Short-term bank loans |
| 232 | Eskontne uvery | Discount loans |
| 24 | Ine kratkodobe financne vypomoci | Other ST financial aid |
| 241 | Vydane kratkodobe dlhopisy | Issued ST bonds |
| 249 | Ostatne kratkodobe financne vypomoci | Other ST financial aid |
| 25 | Kratkodoby financny majetok | Short-term financial assets |
| 251 | Majetkove CP na obchodovanie | Trading equity securities |
| 252 | Vlastne akcie a vlastne obchodne podiely | Treasury shares |
| 253 | Dlhove CP na obchodovanie | Trading debt securities |
| 255 | Vlastne dlhopisy | Own bonds |
| 256 | Dlhove CP so splatnostou do 1 roka | Debt securities due < 1yr |
| 257 | Ostatne realizovatelne CP | Other AFS securities |
| 259 | Obstaranie kratkodobeho financneho majetku | Acquisition ST financial |
| 26 | Prevody medzi financnymi uctami | Transfers between accounts |
| 261 | Peniaze na ceste | Money in transit |
| 29 | Opravne polozky ku KFM | Allowances to ST financial |
| 291 | OP ku kratkodobemu financnemu majetku | Allowance — ST financial |

### Class 3 — Settlement Relationships
| Code | Name (SK) | Name (EN) |
|------|-----------|-----------|
| 31 | Pohladavky | Receivables |
| 311 | Odberatelia | Trade receivables |
| 312 | Zmenky na inkaso | Bills receivable |
| 313 | Pohladavky za eskontovane CP | Discounted securities receivable |
| 314 | Poskytnutne preddavky | Advances given |
| 315 | Ostatne pohladavky | Other receivables |
| 316 | Cista hodnota zakazky | Net contract value |
| 32 | Zavazky | Payables |
| 321 | Dodavatelia | Trade payables |
| 322 | Zmenky na uhradu | Bills payable |
| 323 | Kratkodobe rezervy | Short-term reserves |
| 324 | Prijate preddavky | Advances received |
| 325 | Ostatne zavazky | Other payables |
| 326 | Nevyfakturovane dodavky | Uninvoiced deliveries |
| 33 | Zuctovanie so zamestnancami a organmi SP/ZP | Employee settlements |
| 331 | Zamestnanci | Employees |
| 333 | Ostatne zavazky voci zamestnancom | Other employee payables |
| 335 | Pohladavky voci zamestnancom | Employee receivables |
| 336 | Zuctovanie s organmi SP a ZP | Social/health insurance |
| 34 | Zuctovanie dani a dotacii | Tax and subsidy settlements |
| 341 | Dan z prijmov | Income tax |
| 342 | Ostatne priame dane | Other direct taxes |
| 343 | Dan z pridanej hodnoty | VAT (DPH) |
| 345 | Ostatne dane a poplatky | Other taxes and fees |
| 346 | Dotacie zo statneho rozpoctu | State budget grants |
| 347 | Ostatne dotacie | Other grants |
| 35 | Pohladavky voci spolocnikom a zdruzeniu | Partner receivables |
| 351 | Pohladavky voci prepojenym jednotkam | Receivables — related entities |
| 353 | Pohladavky za upisane vlastne imanie | Subscribed capital receivable |
| 354 | Pohladavky voci spolocnikovi pri uhrade straty | Partner — loss coverage |
| 355 | Ostatne pohladavky voci spolocnikovi | Other partner receivables |
| 358 | Pohladavky voci ucastnikom zdruzenia | Association receivables |
| 36 | Zavazky voci spolocnikom a zdruzeniu | Partner payables |
| 361 | Zavazky voci prepojenym jednotkam | Payables — related entities |
| 364 | Zavazky voci spolocnikovi pri rozdelovani zisku | Profit distribution payable |
| 365 | Ostatne zavazky voci spolocnikovi | Other partner payables |
| 366 | Zavazky voci spolocnikovi zo zavislej cinnosti | Employment partner payable |
| 367 | Zavazky z upisanych nespatenych CP | Unpaid subscribed securities |
| 368 | Zavazky voci ucastnikom zdruzenia | Association payables |
| 37 | Ine pohladavky a zavazky | Other receivables/payables |
| 371 | Pohladavky z predaja podniku | Business sale receivables |
| 372 | Zavazky z kupy podniku | Business purchase payables |
| 373 | Pohladavky/zavazky z terminovych operacii | Derivatives |
| 374 | Pohladavky z najmu | Lease receivables |
| 375 | Pohladavky z vydanych dlhopisov | Bond receivables |
| 376 | Nakupene opcie | Purchased options |
| 377 | Predane opcie | Written options |
| 378 | Ine pohladavky | Miscellaneous receivables |
| 379 | Ine zavazky | Miscellaneous payables |
| 38 | Casove rozlisenie nakladov a vynosov | Accruals |
| 381 | Naklady buducich obdobi | Prepaid expenses |
| 382 | Komplexne naklady buducich obdobi | Complex prepaid expenses |
| 383 | Vydavky buducich obdobi | Accrued expenses |
| 384 | Vynosy buducich obdobi | Deferred revenue |
| 385 | Primy buducich obdobi | Accrued revenue |
| 39 | OP k zuctovacim vztahom a vnutorne zuctovanie | Allowances + internal |
| 391 | Opravne polozky k pohladavkam | Allowance — receivables |
| 395 | Vnutorne zuctovanie | Internal settlements |
| 398 | Spojovaci ucet pri zdruzeni | Association clearing |

### Class 4 — Capital and Long-term Liabilities
| Code | Name (SK) | Name (EN) |
|------|-----------|-----------|
| 41 | Zakladne imanie a kapitalove fondy | Share capital and capital funds |
| 411 | Zakladne imanie | Share capital |
| 412 | Emisne azio | Share premium |
| 413 | Ostatne kapitalove fondy | Other capital funds |
| 414 | Ocenovacie rozdiely z precenenia majetku a zavazkov | Revaluation differences |
| 415 | Ocenovacie rozdiely z kapitalovych ucastin | Equity method revaluation |
| 416 | Ocenovacie rozdiely pri zluceni/splyunti/rozdeleni | Merger revaluation |
| 417 | Zakonny rezervny fond z kapitalovych vkladov | Legal reserve — capital |
| 418 | Nedelitelny fond z kapitalovych vkladov | Indivisible fund — capital |
| 419 | Zmeny zakladneho imania | Changes in share capital |
| 42 | Fondy tvorene zo zisku a prevedene vysledky | Profit funds and carry-forwards |
| 421 | Zakonny rezervny fond | Legal reserve fund |
| 422 | Nedelitelny fond | Indivisible fund |
| 423 | Statutarne fondy | Statutory funds |
| 427 | Ostatne fondy | Other funds |
| 428 | Nerozdeleny zisk minulych rokov | Retained earnings |
| 429 | Neuhradena strata minulych rokov | Accumulated losses |
| 43 | Vysledok hospodarenia | Operating result |
| 431 | Vysledok hospodarenia v schvalovani | P&L awaiting approval |
| 45 | Rezervy | Reserves |
| 451 | Rezervy zakonne | Statutory reserves |
| 459 | Ostatne rezervy | Other reserves |
| 46 | Bankove uvery | Bank loans (LT) |
| 461 | Bankove uvery | Long-term bank loans |
| 47 | Dlhodobe zavazky | Long-term payables |
| 471 | Dlhodobe zavazky voci prepojenym jednotkam | LT payables — related |
| 472 | Zavazky zo socialneho fondu | Social fund payables |
| 473 | Vydane dlhopisy | Issued bonds |
| 474 | Zavazky z najmu | Lease liabilities |
| 475 | Dlhodobe prijate preddavky | LT advances received |
| 476 | Dlhodobe nevyfakturovane dodavky | LT uninvoiced deliveries |
| 478 | Dlhodobe zmenky na uhradu | LT bills payable |
| 479 | Ostatne dlhodobe zavazky | Other LT payables |
| 48 | Odlozeny danovy zavazok a odlozena danova pohladavka | Deferred tax |
| 481 | Odlozeny danovy zavazok a odlozena danova pohladavka | Deferred tax asset/liability |
| 49 | Fyzicka osoba — podnikatel | Sole trader |
| 491 | Vlastne imanie FO — podnikatela | Sole trader equity |

### Class 5 — Expenses
| Code | Name (SK) | Name (EN) |
|------|-----------|-----------|
| 50 | Spotrebovane nakupy | Consumed purchases |
| 501 | Spotreba materialu | Material consumption |
| 502 | Spotreba energie | Energy consumption |
| 503 | Spotreba ostatnych neskladovatelnych dodavok | Other non-storable supplies |
| 504 | Predany tovar | Cost of goods sold |
| 505 | Tvorba a zuctovanie OP k zasobam | Allowances — inventories |
| 507 | Predana nehnutelnost | Sold real estate |
| 51 | Sluzby | Services |
| 511 | Opravy a udrzivanie | Repairs and maintenance |
| 512 | Cestovne | Travel |
| 513 | Naklady na reprezentaciu | Representation |
| 518 | Ostatne sluzby | Other services |
| 52 | Osobne naklady | Personnel costs |
| 521 | Mzdove naklady | Wages |
| 522 | Prijmy spolocnikov zo zavislej cinnosti | Partner employment income |
| 523 | Odmeny clenom organov | Board member remuneration |
| 524 | Zakonne socialne poistenie | Statutory social insurance |
| 525 | Ostatne socialne poistenie | Other social insurance |
| 526 | Socialne naklady FO — podnikatela | Sole trader social costs |
| 527 | Zakonne socialne naklady | Statutory social costs |
| 528 | Ostatne socialne naklady | Other social costs |
| 53 | Dane a poplatky | Taxes and fees |
| 531 | Dan z motorovych vozidiel | Motor vehicle tax |
| 532 | Dan z nehnutelnosti | Real estate tax |
| 538 | Ostatne dane a poplatky | Other taxes and fees |
| 54 | Ine naklady na hospodarsku cinnost | Other operating expenses |
| 541 | Zostatkova cena predaneho DM | NBV of sold LT assets |
| 542 | Predany material | Sold material (cost) |
| 543 | Dary | Donations |
| 544 | Zmluvne pokuty, penale a uroky z omeskania | Contractual penalties |
| 545 | Ostatne pokuty, penale a uroky z omeskania | Other penalties |
| 546 | Odpis pohladavok | Receivable write-offs |
| 547 | Tvorba a zuctovanie OP k pohladavkam | Allowances — receivables |
| 548 | Ostatne naklady na hospodarsku cinnost | Other operating expenses |
| 549 | Manka a skody | Shortages and damages |
| 55 | Odpisy a OP k DM | Depreciation and allowances |
| 551 | Odpisy DNM a DHM | Depreciation |
| 553 | Tvorba a zuctovanie OP k DM | Allowances — LT assets |
| 555 | Zuctovanie komplexnych nakladov buducich obdobi | Complex prepaid exp release |
| 557 | Zuctovanie opravky k OP k nadobudnutemu majetku | Amort of acquired asset allowance |
| 56 | Financne naklady | Financial expenses |
| 561 | Predane CP a podiely | Sold securities (cost) |
| 562 | Uroky | Interest expense |
| 563 | Kurzove straty | FX losses |
| 564 | Naklady na precenenie CP | Securities revaluation losses |
| 565 | Tvorba a zuctovanie OP k financnemu majetku | Allowances — financial assets |
| 566 | Naklady na kratkodoby financny majetok | ST financial asset expenses |
| 567 | Naklady na derivatove operacie | Derivative expenses |
| 568 | Ostatne financne naklady | Other financial expenses |
| 569 | Manka a skody na financnom majetku | Financial asset shortages |
| 59 | Dane z prijmov a prevodove ucty | Income tax + transfers |
| 591 | Splatna dan z prijmov | Current income tax |
| 592 | Odlozena dan z prijmov | Deferred income tax |
| 595 | Dodatocne odvody dane z prijmov | Additional income tax |
| 596 | Prevod podielov na vysledku hospodarenia spolocnikom | Profit share transfers |

### Class 6 — Revenues
| Code | Name (SK) | Name (EN) |
|------|-----------|-----------|
| 60 | Trzby za vlastne vykony a tovar | Sales revenue |
| 601 | Trzby za vlastne vyrobky | Revenue — own products |
| 602 | Trzby z predaja sluzieb | Revenue — services |
| 604 | Trzby za tovar | Revenue — goods |
| 606 | Vynosy zo zakazky | Contract revenue |
| 607 | Vynosy z nehnutelnosti na predaj | Real estate sale revenue |
| 61 | Zmeny stavu vnutroorganizacnych zasob | Internal inventory changes |
| 611 | Zmena stavu nedokoncenej vyroby | Change in WIP |
| 612 | Zmena stavu polotovarov | Change in semi-finished |
| 613 | Zmena stavu vyrobkov | Change in finished goods |
| 614 | Zmena stavu zvierat | Change in animals |
| 62 | Aktivacia | Activation |
| 621 | Aktivacia materialu a tovaru | Activation — material/goods |
| 622 | Aktivacia vnutroorganizacnych sluzieb | Activation — internal services |
| 623 | Aktivacia DNM | Activation — intangible assets |
| 624 | Aktivacia DHM | Activation — tangible assets |
| 64 | Ine vynosy z hospodarskej cinnosti | Other operating revenue |
| 641 | Trzby z predaja DNM a DHM | Revenue — sale of LT assets |
| 642 | Trzby z predaja materialu | Revenue — sale of material |
| 644 | Zmluvne pokuty, penale a uroky z omeskania | Contractual penalties received |
| 645 | Ostatne pokuty, penale a uroky z omeskania | Other penalties received |
| 646 | Vynosy z odpisanych pohladavok | Recovered written-off receivables |
| 648 | Ostatne vynosy z hospodarskej cinnosti | Other operating revenue |
| 65 | Zuctovanie niektorych poloziek z hospodarskej cinnosti | Certain operating releases |
| 655 | Zuctovanie komplexnych nakladov buducich obdobi | Complex prepaid release |
| 657 | Zuctovanie opravky k OP k nadobudnutemu majetku | Acquired asset allowance amort |
| 66 | Financne vynosy | Financial revenue |
| 661 | Trzby z predaja CP a podielov | Revenue — sale of securities |
| 662 | Uroky | Interest revenue |
| 663 | Kurzove zisky | FX gains |
| 664 | Vynosy z precenenia CP | Securities revaluation gains |
| 665 | Vynosy z dlhodobeho financneho majetku | LT financial asset revenue |
| 666 | Vynosy z kratkodobeho financneho majetku | ST financial asset revenue |
| 667 | Vynosy z derivatovych operacii | Derivative revenue |
| 668 | Ostatne financne vynosy | Other financial revenue |

### Class 7 — Closing and Off-Balance Sheet
| Code | Name (SK) | Name (EN) |
|------|-----------|-----------|
| 70 | Suvahove uzavierkove ucty | Balance sheet closing |
| 701 | Zaciatocny ucet suvahovy | Opening balance sheet |
| 702 | Konecny ucet suvahovy | Closing balance sheet |
| 71 | Vysledkovy uzavierkovy ucet | P&L closing |
| 710 | Ucet ziskov a strat | Profit and loss |
| 711 | Zaciatocny ucet nakladov a vynosov | Opening expense/revenue (interim) |
| 75-79 | Podsuvahove ucty | Off-balance sheet accounts |

### Classes 8 and 9 — Internal Accounting
Used for management/cost accounting. Structure defined by each entity internally.

---

## KEY BOOKING PATTERNS SUMMARY (Predkontacie)

### Supplier Invoice (Received)
| Step | Debit | Credit | Description |
|------|-------|--------|-------------|
| 1 | 5xx (expense) or 04x (asset) | 321 | Net amount (tax base) |
| 2 | 343 | 321 | Input VAT (if deductible) |
| 3 | 321 | 221 | Payment |

### Customer Invoice (Issued)
| Step | Debit | Credit | Description |
|------|-------|--------|-------------|
| 1 | 311 | 6xx (revenue) | Net amount (tax base) |
| 2 | 311 | 343 | Output VAT |
| 3 | 221 | 311 | Collection |

### Purchase of Tangible Asset
| Step | Debit | Credit | Description |
|------|-------|--------|-------------|
| 1 | 042 | 321 | Purchase (excl. VAT) |
| 2 | 343 | 321 | Input VAT |
| 3 | 02x | 042 | Activation into use |
| 4 | 551 | 08x | Monthly depreciation |

### Purchase of Intangible Asset
| Step | Debit | Credit | Description |
|------|-------|--------|-------------|
| 1 | 041 | 321 | Purchase (excl. VAT) |
| 2 | 343 | 321 | Input VAT |
| 3 | 01x | 041 | Activation into use |
| 4 | 551 | 07x | Monthly amortization |

### Sale of Long-term Asset
| Step | Debit | Credit | Description |
|------|-------|--------|-------------|
| 1 | 541 | 07x/08x | Remaining book value to expense |
| 2 | 07x/08x | 01x/02x | Derecognition |
| 3 | 311/315 | 641 | Sale revenue |
| 4 | 311/315 | 343 | Output VAT on sale |

### Material Purchase (Method A)
| Step | Debit | Credit | Description |
|------|-------|--------|-------------|
| 1 | 111 | 321 | Purchase order |
| 2 | 343 | 321 | Input VAT |
| 3 | 112 | 111 | Receipt to warehouse |
| 4 | 501 | 112 | Consumption |

### Material Purchase (Method B)
| Step | Debit | Credit | Description |
|------|-------|--------|-------------|
| 1 | 501 | 321 | Purchase directly to expense |
| 2 | 343 | 321 | Input VAT |
| Year-end | 501 | 112 | Reverse opening stock |
| Year-end | 112 | 501 | Record closing stock |

### Payroll
| Step | Debit | Credit | Description |
|------|-------|--------|-------------|
| 1 | 521 | 331 | Gross wages |
| 2 | 331 | 336 | Employee SP/ZP deductions |
| 3 | 331 | 342 | Employee income tax withholding |
| 4 | 524 | 336 | Employer SP/ZP contributions |
| 5 | 331 | 221 | Net wage payment |
| 6 | 336 | 221 | Insurance payment to authorities |
| 7 | 342 | 221 | Tax payment to tax office |

### Depreciation (Monthly)
| Debit | Credit | Description |
|-------|--------|-------------|
| 551 | 07x | Amortization of intangible assets |
| 551 | 08x | Depreciation of tangible assets |

### Financial Leasing (Lessee)
| Step | Debit | Credit | Description |
|------|-------|--------|-------------|
| 1 | 042 | 474 | Recognition at PV of payments |
| 2 | 02x | 042 | Activation |
| 3 | 474 | 221 | Lease principal payment |
| 4 | 562 | 221 | Lease interest payment |
| 5 | 551 | 08x | Depreciation |

### Opening Books
| Debit | Credit | Description |
|-------|--------|-------------|
| Asset accounts | 701 | Open asset balances |
| 701 | Liability/Equity accounts | Open liability/equity balances |

### Closing Books
| Debit | Credit | Description |
|-------|--------|-------------|
| 710 | 5xx | Close expense accounts to P&L |
| 6xx | 710 | Close revenue accounts to P&L |
| 702 | Asset accounts | Close assets to balance sheet |
| Liability/Equity accounts | 702 | Close liabilities to balance sheet |
| 710 | 702 | Transfer profit (or Debit 702 / Credit 710 for loss) |

### Profit Distribution
| Debit | Credit | Description |
|-------|--------|-------------|
| 431 | 421 | To legal reserve fund |
| 431 | 364 | Dividends to partners |
| 431 | 428 | Retained earnings |
| 429 | 431 | Loss carry forward |

### Currency Differences
| Debit | Credit | Description |
|-------|--------|-------------|
| 563 | 3xx | FX loss on settlement |
| 3xx | 663 | FX gain on settlement |

### Allowances
| Type | Creation (Debit/Credit) | Release (Debit/Credit) |
|------|------------------------|----------------------|
| Receivables | 547 / 391 | 391 / 547 |
| Inventories | 505 / 19x | 19x / 505 |
| LT intangible | 553 / 09x | 09x / 553 |
| LT tangible | 553 / 09x | 09x / 553 |
| Financial | 565 / 09x | 09x / 565 |

---

## AMENDMENT EFFECTIVE 1.1.2025 (Opatrenie c. MF/014948/2024-74)

Key changes:
1. **Dorovnavacia dan (top-up tax)** — global minimum tax for large multinational/domestic groups. Accounted on 341/591. Per Act 507/2023 Z.z.
2. **Dan z financnych transakcii** — financial transaction tax added to account 538 (Ostatne dane a poplatky). Per Act 279/2024 Z.z.
3. **Kryptoaktiva** — crypto-assets acquired through network validation accounted as revenue on 668 (Ostatne financne vynosy). Off-balance tracking on podsuvahovy ucet.
4. **Utility tokens** (§30f) — new section for accounting of utility tokens.
5. Various footnote reference updates.

---

## TRANSITIONAL PROVISIONS (§85a — §86n)

Historical provisions for:
- EUR conversion (2009) — §85a through §85e
- Various amendment effective dates from 2003 through 2024
- §86n (from 31.12.2024) — transitional rule for financial statements prepared as of 31.12.2024

These are historical and generally not relevant for new transactions.

---

## SOURCE REFERENCE

- **Legal citation:** Opatrenie MF SR c. 23054/2002-92 v zneni neskorsich predpisov (vrátane opatrenia c. MF/014948/2024-74)
- **Full text source:** Financna sprava SR (financnasprava.sk)
- **Effective from:** 1.1.2003, last amendment effective 1.1.2025
- **Appendix 1:** Ramcova uctova osnova pre podnikatelov (Framework chart of accounts)
- **Appendix 2:** EU directives transposed (2013/34/EU, 2006/111/ES)
