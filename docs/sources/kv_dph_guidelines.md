---
source: "Finančná správa SR — Metodický pokyn ku kontrolnému výkazu DPH"
title: "KV DPH Section Classification Logic"
effective_date: "2025-01-01"
form_version: "KVDPHv25"
url: "https://www.financnasprava.sk/sk/podnikatelia/dane/dan-z-pridanej-hodnoty/kontrolny-vykaz-dph"
additional_sources:
  - "https://www.podnikajte.sk/dan-z-pridanej-hodnoty/ako-vyplnit-kontrolny-vykaz-dph"
  - "https://llarik.sk/blog/kontrolny-vykaz-dph"
  - "https://www.podnikajte.sk/dan-z-pridanej-hodnoty/kontrolny-vykaz-k-dph"
  - "https://www.mfsr.sk/files/archiv/92/Poucenie_KV_DPH_2021.pdf"
  - "https://www.financnasprava.sk/_img/pfsedit/Dokumenty_PFS/Profesionalna_zona/Dane/Metodicke_pokyny/Nepriame_dane/2014/2014_03_07_mp_kv_dph.pdf"
compiled: "2026-03-13"
notes: |
  Compiled from multiple official and professional sources. The section structure
  described here reflects the KVDPHv25 form valid from 2025-01-01. Key correction
  vs original user assumptions: the 5000 EUR threshold applies specifically to
  reverse charge goods in A.2 (not to A.1/A.2 split generally), and B.3 uses a
  3000 EUR threshold (not 5000 EUR). See "Important Corrections" at bottom.
---

# KV DPH — Kontrolný výkaz k dani z pridanej hodnoty

## Overview

The KV DPH (VAT Control Statement) is a mandatory electronic filing containing detailed
transaction-level data about invoices issued and received during a tax period. It is designed
to enable cross-matching between suppliers and customers to detect VAT fraud.

**Who files:** All VAT payers registered under §4, §4a, §5, or §6 of the VAT Act (222/2004 Z.z.).
Not required for those registered under §7 (IC acquisition only) or §7a (cross-border services only).

**Deadline:** 25 days after the end of the tax period (same as the VAT return).

**Format:** XML only, submitted electronically via the Financial Administration portal.

**Empty filing:** Required even if no transactions occurred in the period ("prázdny kontrolný výkaz").

**Penalties:** Up to 10,000 EUR for non-filing or failure to correct; up to 100,000 EUR for repeated violations.

---

## Section Structure

The KV DPH has four parts (A, B, C, D) with sub-sections:

| Part | Sub-sections | Reporting style |
|------|-------------|-----------------|
| A (Supplies) | A.1, A.2 | Individual documents, one per line |
| B (Acquisitions) | B.1, B.2, B.3.1, B.3.2 | B.1/B.2 individual; B.3 aggregated |
| C (Corrections) | C.1, C.2 | Individual documents, one per line |
| D (Cash register & other) | D.1, D.2 | Aggregated summaries by VAT rate |

---

## Section A — Supplies (Dodávky — strana dodávateľa)

### A.1 — Invoices Issued: Standard Domestic Supplies

**Classification criteria:**
- Invoice issued by the VAT payer (supplier)
- Supply of goods or services with place of supply in Slovakia
- Supplier is liable for VAT (standard case)
- Customer has IČ DPH (VAT ID) or IČO
- Does NOT include supplies to private individuals (those go to D.2)
- Does NOT include reverse charge supplies (those go to A.2)
- Also includes: domestic supplies of goods listed in §69(12)(f-i) where tax base per invoice is BELOW 5,000 EUR (no reverse charge triggered)

**Required fields:**
- IČ DPH odberateľa (customer VAT ID)
- Poradové číslo faktúry (invoice sequential number)
- Dátum dodania tovaru/služby (date of supply)
- Základ dane (tax base)
- Suma dane (VAT amount)
- Sadzba dane (VAT rate)
- Kód opravy (correction code, if applicable)

**Examples:**
- Company ABC s.r.o. issues invoice #2025001 for consulting services to XY s.r.o. (SK1234567890) for 1,000 EUR + 230 EUR DPH (23%) = 1,230 EUR total. Goes to A.1.
- Supplier sells mobile phones to a retailer, tax base 3,000 EUR (below 5,000 EUR threshold for reverse charge on specified goods). Goes to A.1, not A.2.

**What does NOT go here:**
- Invoices to private individuals without IČ DPH → D.2
- Exempt supplies under §43, §47, §48 → excluded from KV entirely
- Exports reported in súhrnný výkaz → excluded from KV
- Reverse charge supplies → A.2

---

### A.2 — Invoices Issued: Reverse Charge (Domestic — Supplier Side)

**Classification criteria:**
- Invoice issued by the supplier
- Recipient (not supplier) bears VAT liability under §69 ods. 12 písm. f) to i)
- Applies to specific goods where tax base per invoice >= 5,000 EUR:
  - f) Agricultural products (poľnohospodárske plodiny) — per Annex 1
  - g) Metals and metal products (kovy a kovové výrobky) — per Annex 2
  - h) Mobile phones (mobilné telefóny) — per commodity code
  - i) Integrated circuits (integrované obvody) — per commodity code
- Also applies to construction works (stavebné práce, CPA division F) under §69(12)(j) regardless of amount

**Threshold rule — the 5,000 EUR rule:**
The 5,000 EUR threshold is applied to the TAX BASE (základ dane) per invoice, not the total including VAT. If a single invoice for specified goods (§69(12)(f-i)) has a tax base >= 5,000 EUR, reverse charge applies and it goes to A.2. Below 5,000 EUR, it stays in A.1 as a standard supply.

For construction works §69(12)(j), there is NO threshold — all construction services with reverse charge go to A.2 regardless of amount.

**Required fields (beyond A.1):**
- IČ DPH odberateľa (customer VAT ID)
- Poradové číslo faktúry (invoice sequential number)
- Dátum dodania (date of supply)
- Základ dane (tax base) — NO VAT amount (supplier does not charge VAT)
- Kód tovaru (commodity code for agriculture/metals)
- Druh tovaru (goods type for phones/circuits)
- Množstvo (quantity)
- Merná jednotka (unit of measure)
- Kód opravy (correction code)

**Examples:**
- Telefonujeme s.r.o. supplies 400 mobile phones to Volám s.r.o. (SK9865389560) for 10,000 EUR tax base. Since base >= 5,000 EUR for mobile phones, reverse charge applies. Goes to A.2 with commodity details.
- Construction company issues invoice for building renovation, 8,000 EUR tax base. CPA F construction work — always A.2 regardless of amount.
- Farmer sells grain worth 4,500 EUR tax base — below 5,000 EUR, goes to A.1 (no reverse charge).

---

## Section B — Acquisitions (Prijaté plnenia — strana odberateľa)

### B.1 — Received Invoices: Reverse Charge (Samozdanenie)

**Classification criteria:**
- Invoices received where the RECIPIENT bears VAT liability
- Applies under §69 ods. 2, 3, 6, 7, 9, 10, 11, 12 — broadly:
  - Services received from foreign suppliers (other EU member states or third countries)
  - Intra-community acquisition of goods (IC acquisition from EU)
  - Gas, electricity, heat, cooling from foreign suppliers
  - Domestic reverse charge (specified goods >= 5,000 EUR, construction works)
  - Gold transactions under §69(9)
- ALWAYS reported regardless of amount — no threshold
- Reported even if the recipient does NOT claim input VAT deduction (or defers it)
- The recipient self-assesses (samozdanenie): both output and input VAT

**Required fields:**
- IČ DPH dodávateľa (supplier VAT ID — can be foreign, e.g., CZ12345679)
- Poradové číslo faktúry (invoice number)
- Dátum dodania / dátum vzniku daňovej povinnosti (date of supply / tax liability date)
- Základ dane (tax base)
- Suma dane (VAT amount — self-assessed)
- Sadzba dane (VAT rate applied)
- Odpočítaná daň (deducted VAT amount, if claimed)
- Kód opravy (correction code)

**Examples:**
- ABC s.r.o. receives invoice PF123 from Czech advertising agency (CZ12345679) for 500 EUR in services. ABC self-assesses 23% VAT = 115 EUR. Goes to B.1.
- Company acquires goods from German supplier (DE123456789) worth 3,000 EUR. IC acquisition — B.1.
- Retailer receives invoice from domestic construction subcontractor for 8,000 EUR (reverse charge under §69(12)(j)). Goes to B.1.
- Company receives invoice for 400 mobile phones from domestic supplier, tax base 10,000 EUR (reverse charge). Goes to B.1.

**Key rule:** B.1 entries must always have complete data. Unlike B.2, missing fields cannot be filled with "0".

---

### B.2 — Received Invoices: Standard Domestic (Input VAT Deduction)

**Classification criteria:**
- Invoices received from DOMESTIC (Slovak) VAT payers
- Supplier charged standard VAT on the invoice
- Recipient claims input VAT deduction in the CURRENT period
- Invoice is NOT a simplified invoice (those go to B.3)
- Does NOT include reverse charge invoices (those go to B.1)

**Required fields:**
- IČ DPH dodávateľa (supplier VAT ID — Slovak)
- Poradové číslo faktúry (invoice number)
- Dátum dodania (date of supply)
- Základ dane (tax base)
- Suma dane (VAT amount on invoice)
- Sadzba dane (VAT rate)
- Odpočítaná daň (deducted VAT amount)
- Kód opravy (correction code)

**Timing rule:** The invoice appears in B.2 in the period when the deduction is CLAIMED, not when the invoice is received. For cash-basis VAT payers (§68d), deduction occurs when payment is made.

**100% advance payments:** If a 100% advance payment invoice is received, it replaces the final invoice in KV reporting. Do not duplicate.

**Examples:**
- Office receives rental invoice from Prenájom s.r.o. (SK8888888888) for 1,000 EUR + 230 EUR VAT (23%). Deduction claimed in current period. Goes to B.2.
- Company receives invoice for office supplies, 200 EUR + 46 EUR VAT. Claims full deduction. Goes to B.2.

**Missing data handling:** If required invoice fields are absent, enter "0" in the affected column (unlike B.1 where all data must be present).

---

### B.3 — Simplified Invoices (Zjednodušené faktúry — Aggregated)

**Classification criteria:**
- Documents that are NOT full invoices (zjednodušené faktúry / simplified invoices)
- Input VAT deduction claimed from these documents
- Types of simplified documents:
  - Doklady z pokladníc e-kasa (e-cash register receipts)
  - Doklady z tankovacích automatov (fuel pump receipts)
  - Doklady do 100 EUR: parking tickets, highway vignettes, transit tickets, toll receipts
  - Other documents under §74 ods. 3 of the VAT Act

**Reporting:** AGGREGATED (sumárne) — not individual documents like A.1/A.2/B.1/B.2.

**The 3,000 EUR threshold splits B.3 into two sub-sections:**

#### B.3.1 — Total Deducted VAT < 3,000 EUR in the Period

- If the total deducted VAT from ALL simplified invoices in the period is BELOW 3,000 EUR
- Report as a SINGLE summary line: total tax base and total VAT by rate
- NO individual supplier identification required

**Example:**
- Company has fuel receipts (83.33 EUR base + 19.17 EUR VAT at 23%) and toll sticker (50 EUR base + 11.50 EUR VAT). Total deducted VAT = 30.67 EUR, well below 3,000 EUR. One summary line in B.3.1.

#### B.3.2 — Total Deducted VAT >= 3,000 EUR in the Period

- If the total deducted VAT from ALL simplified invoices in the period is 3,000 EUR OR MORE
- Report aggregated totals GROUPED BY SUPPLIER VAT ID
- Each supplier gets its own line with aggregated base + VAT amounts

**Example:**
- Large transport company with many fuel purchases. Total deducted VAT from simplified invoices reaches 4,500 EUR in the period. Must group by each fuel station's VAT ID and report separately per supplier.

---

## Section C — Corrections (Opravy)

### C.1 — Credit Notes / Corrections Issued (Supplier Side)

**Classification criteria:**
- Credit notes (dobropisy) issued correcting previously reported invoices in A.1 or A.2
- Correction documents for uncollectible debts (opravný doklad podľa §25a)
- Subsequent collection documents (if debtor pays after debt was written off)
- Any correction to a previously reported supply

**Required fields:**
- IČ DPH odberateľa (customer VAT ID)
- Poradové číslo opravného dokladu (credit note number)
- Poradové číslo pôvodnej faktúry (original invoice number — REQUIRED reference)
- Rozdiel základu dane (difference in tax base — can be negative)
- Rozdiel sumy dane (difference in VAT amount — can be negative)
- Sadzba dane (VAT rate)
- Kód opravy (correction code)
- For A.2 corrections: commodity code, goods type, quantity difference, unit

**Timing:** Reported in the period when the correction OCCURS (e.g., when a debt becomes uncollectible under §25a), not when the document is physically issued.

**Examples:**
- ABC s.r.o. issues credit note #D2025001 to customer SK1090444444 for -600 EUR base and -138 EUR VAT, correcting original invoice #F2024050. Goes to C.1 with reference to original invoice.
- Supplier writes off uncollectible debt of 1,000 EUR + 230 EUR VAT. Issues correction document. Goes to C.1 in the period the debt became uncollectible.

**Key rule:** The original invoice number must ALWAYS be referenced. Multiple original invoices corrected by a single credit note require listing all original invoice numbers.

---

### C.2 — Credit Notes / Corrections Received (Recipient Side)

**Classification criteria:**
- Credit notes (dobropisy) received correcting previously reported invoices in B.1 or B.2
- Correction documents from suppliers for uncollectible debts
- VAT adjustments under §53b (when payment remains outstanding > 100 days past due date)
- Subsequent collection documents (if payment made after write-off)

**Required fields:**
- IČ DPH dodávateľa (supplier VAT ID)
- Poradové číslo opravného dokladu (credit note number)
- Poradové číslo pôvodnej faktúry (original invoice number — REQUIRED reference)
- Rozdiel základu dane (difference in tax base)
- Rozdiel sumy dane (difference in VAT)
- Rozdiel odpočítanej dane (difference in deducted VAT)
- Sadzba dane (VAT rate)
- Kód opravy (correction code)

**Timing:** Credit notes received must be reported within 30 days of issuance. If deduction was previously claimed, it must be adjusted in the period the credit note is received.

**§53b adjustment:** When an invoice remains unpaid for more than 100 days past due date, the recipient must adjust (reduce) their input VAT deduction. This adjustment is reported in C.2.

**Examples:**
- Company receives credit note D230703 from supplier Dobják s.r.o. (SK1066666666) for -1,500 EUR base and -345 EUR VAT, correcting original invoice F2024100. Goes to C.2.
- Invoice #F2024200 from supplier remains unpaid 100+ days past due. Company must reduce input VAT deduction by 460 EUR. Adjustment goes to C.2 with reference to original invoice.

---

## Section D — Cash Register and Other Supplies

### D.1 — E-Cash Register Sales (Tržby z pokladníc e-kasa)

**Classification criteria:**
- Aggregate sales data from electronic cash registers (e-kasa pokladnica)
- Sales to end consumers (private individuals)
- Mandatory for businesses required to use e-kasa

**Reporting:** AGGREGATED by VAT rate — NOT individual transactions.

**Required fields:**
- Celkový obrat z pokladníc (total turnover from cash registers)
- Základ dane by rate (tax base split by VAT rate: 23%, 19%, 5%)
- Suma dane by rate (VAT amount per rate)
- Kód opravy (correction code)

**Key rule:** If a sale was made through e-kasa BUT a full invoice was also issued and reported in A.1, do NOT duplicate it in D.1. The A.1 entry takes precedence.

**Example:**
- Retail shop's monthly e-kasa total: 20,000 EUR turnover. Breakdown: 16,260.16 EUR base at 23% = 3,739.84 EUR VAT. Report as single D.1 summary line.

---

### D.2 — Other Non-Invoiced Supplies

**Classification criteria:**
- Taxable supplies where no invoice is required (sales to non-entrepreneurs/private individuals)
- Supplies NOT through e-kasa
- Invoices issued to customers WITHOUT IČ DPH (private individuals)
- "Príjmové pokladničné doklady" (receipt documents) for cash sales not via e-kasa

**Reporting:** AGGREGATED by VAT rate — summary totals only.

**Required fields:**
- Základ dane by rate (tax base per VAT rate)
- Suma dane by rate (VAT amount per rate)
- Kód opravy (correction code)

**Examples:**
- Consulting firm issues invoice to a private individual (no VAT ID) for 500 EUR + 115 EUR VAT. Goes to D.2 (aggregated with other such invoices for the period).
- Transit tickets, fuel pump receipts from the SUPPLIER's perspective (not buyer's simplified invoices).

---

## Correction Mechanisms

### Opravný kontrolný výkaz (Corrective — before deadline)

- Submitted BEFORE the 25-day filing deadline expires
- Completely REPLACES the original filing
- Must contain ALL data for the period (not just corrections)

### Dodatočný kontrolný výkaz (Supplementary — after deadline)

- Submitted AFTER the deadline has passed
- Contains ONLY the changes, using correction codes:
  - **Kód 1** = cancellation of an originally reported row (storno)
  - **Kód 2** = addition of a new row (doplnenie)
- To correct a row: submit code 1 for the wrong row + code 2 for the correct row

---

## Transactions EXCLUDED from KV DPH

The following are NOT reported in the KV DPH at all:

- Exempt supplies with right of deduction: §43 (IC supply of goods), §47 (export of goods), §48 (exempt services)
- Transactions reported in Súhrnný výkaz (EC Sales List) instead
- Theft-related VAT settlements (§53 ods. 5)
- Tourist VAT refunds for goods exported to third countries
- Year-end coefficient adjustments (§50 ods. 4)
- Capital asset adjustments (§54 to §54d)
- Registration-period deductions (§55)
- Deregistration VAT settlements
- VAT on import of goods (reported separately)

---

## Important Corrections to Common Assumptions

### The 5,000 EUR threshold

The 5,000 EUR threshold does NOT split A.1 vs A.2 by invoice total amount. Instead:

- **A.1 vs A.2 distinction** is about WHO bears the VAT liability (supplier vs recipient)
- The 5,000 EUR threshold applies ONLY to specific goods under §69(12)(f-i): agricultural products, metals, mobile phones, integrated circuits
- When the TAX BASE (not total) per invoice for these specific goods is >= 5,000 EUR, reverse charge applies and the invoice goes to A.2
- Below 5,000 EUR for these goods, normal VAT applies and it stays in A.1
- Construction works (§69(12)(j)) ALWAYS trigger reverse charge regardless of amount

Similarly, B.1 vs B.2 is about reverse charge vs standard VAT, not about an amount threshold.

### The 3,000 EUR threshold in B.3

- Applies to B.3 (simplified invoices), not B.1/B.2
- The threshold is on TOTAL DEDUCTED VAT from all simplified invoices in the period
- Below 3,000 EUR → B.3.1 (single summary line)
- At or above 3,000 EUR → B.3.2 (grouped by supplier VAT ID)

### Classification decision tree

```
SUPPLIER SIDE (invoice issued):
├── Is it a standard domestic supply where supplier pays VAT?
│   ├── Customer has IČ DPH → A.1
│   └── Customer is private individual → D.2
├── Is it reverse charge under §69(12)?
│   ├── Construction works → A.2 (always)
│   └── Specified goods (agri, metals, phones, circuits):
│       ├── Tax base >= 5,000 EUR → A.2
│       └── Tax base < 5,000 EUR → A.1
├── Is it a sale through e-kasa? → D.1 (aggregated)
├── Is it a credit note / correction? → C.1
└── Is it exempt (§43, §47, §48) or export? → NOT in KV

RECIPIENT SIDE (invoice received):
├── Is it reverse charge / self-assessment?
│   ├── Foreign supplier (EU/third country services) → B.1
│   ├── IC acquisition of goods → B.1
│   ├── Domestic reverse charge (specified goods, construction) → B.1
│   └── Gold, gas/electricity from abroad → B.1
├── Is it a standard domestic invoice with VAT? → B.2
├── Is it a simplified invoice (receipt, fuel pump, etc.)?
│   ├── Total period deducted VAT < 3,000 EUR → B.3.1
│   └── Total period deducted VAT >= 3,000 EUR → B.3.2
├── Is it a credit note / correction? → C.2
└── Is it exempt or import VAT? → NOT in KV
```

---

## VAT Rates (effective 2025-01-01)

| Rate | Application |
|------|------------|
| 23% | Standard rate (zvýšená z 20% od 1.1.2025) |
| 19% | Reduced rate for selected goods/services |
| 5% | Reduced rate for basic food, press, etc. |
| 0% | Exempt with right of deduction (export, IC supply) |

---

## Filing frequency

- **Monthly:** If tax period is monthly (turnover > 100,000 EUR or first year of registration)
- **Quarterly:** If tax period is quarterly (turnover <= 100,000 EUR, after first year)
- KV DPH is filed for EVERY period where a VAT return is required
