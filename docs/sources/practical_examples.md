---
source: "ako-uctovat.sk, danovecentrum.sk, podnikajte.sk, humanet.sk, financnasprava.sk, uctuj.sk, zrozumitelne-uctovnictvo.com, fintoro.sk"
title: "Practical Booking Examples (Predkontacie) for s.r.o."
effective_date: "2025-01-01"
purpose: "Validation data for accounting engine rules"
dph_rates: "23% standard, 19% reduced I, 5% reduced II (effective 2025-01-01)"
---

# Practical Booking Examples (Predkontacie) for s.r.o.

All examples use 2025 DPH rates: 23% (standard), 19% (reduced I), 5% (reduced II).
Account numbering follows Opatrenie MF SR 23054/2002-92 (chart of accounts for entrepreneurs).

Legend:
- MD = Ma dat (Debit)
- D = Dal (Credit)
- DPH = Dan z pridanej hodnoty (VAT)
- KV DPH = Kontrolny vykaz DPH (VAT Control Statement)

---

## 1. Nakup materialu (Purchase of Material)

### Example 1.1: Purchase of material from domestic supplier with DPH

**Scenario:** Company ABC s.r.o. (VAT payer) receives invoice from supplier XYZ s.r.o. for raw material.
- Invoice total: 1,230.00 EUR
- Tax base: 1,000.00 EUR
- DPH 23%: 230.00 EUR
- Supplier VAT ID: SK2020123456

**Booking (predkontacia):**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Material on stock (prijatie materialu na sklad) | 112 | 321 | 1,000.00 |
| 2 | Input DPH (DPH na vstupe) | 343 | 321 | 230.00 |

**Alternatively, if material goes directly to consumption (method B):**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Material consumption (spotreba materialu) | 501 | 321 | 1,000.00 |
| 2 | Input DPH | 343 | 321 | 230.00 |

**DPH treatment:** Standard input VAT, fully deductible
**KV DPH section:** B.2 (received invoice from domestic supplier, standard VAT deduction)
**Legal source:** Postupy uctovania SS 30-32 (ucty 112, 501), DPH law SS 49-51

### Example 1.2: Purchase of material from EU supplier (intra-community acquisition)

**Scenario:** ABC s.r.o. purchases raw material from German supplier DE GmbH.
- Invoice total: 2,500.00 EUR (without DPH, as intra-EU B2B)
- Supplier VAT ID: DE123456789
- Slovak DPH 23% self-assessed: 575.00 EUR

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Material on stock | 112 | 321 | 2,500.00 |
| 2 | Self-assessed DPH - output (danova povinnost) | 349 | 343 | 575.00 |
| 3 | Self-assessed DPH - input (narok na odpocet) | 343 | 349 | 575.00 |

**DPH treatment:** Intra-community acquisition (nadobudnutie tovaru z EU). Buyer self-assesses both output and input DPH. Net DPH effect = 0 (if fully deductible).
**KV DPH section:** B.1 (received invoice, buyer is person liable to pay tax)
**DPH return:** Reported on both line 07 (acquisition) and line 20 (deduction)
**Legal source:** DPH law SS 11 (nadobudnutie tovaru), SS 69 ods. 6

### Example 1.3: Purchase of material from non-EU country (import)

**Scenario:** ABC s.r.o. imports raw material from China.
- Customs value: 5,000.00 EUR
- Customs duty (clo) 4%: 200.00 EUR
- DPH base: 5,200.00 EUR (customs value + duty)
- DPH 23%: 1,196.00 EUR

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Material on stock (customs value) | 112 | 321 | 5,000.00 |
| 2 | Customs duty (clo) | 112 | 379 | 200.00 |
| 3 | Input DPH on import | 343 | 379 | 1,196.00 |

**DPH treatment:** Import VAT, deductible per SS 49. DPH base includes customs value + duties.
**KV DPH section:** Not reported in KV DPH (imports are on customs declaration, not invoices)
**Legal source:** DPH law SS 20-21 (dovoz tovaru), SS 49 (odpocitanie dane)

### Example 1.4: Purchase of material - non-VAT payer

**Scenario:** Company DEF s.r.o. (NOT a VAT payer) purchases material domestically.
- Invoice total: 615.00 EUR (includes 23% DPH)
- The company cannot deduct DPH.

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Material on stock (full amount incl. DPH) | 112 | 321 | 615.00 |

**DPH treatment:** Non-deductible. Full invoice amount is cost of material.
**KV DPH section:** N/A (non-VAT payer does not file KV DPH)

---

## 2. Nakup sluzieb (Purchase of Services)

### Example 2.1: Purchase of domestic service with DPH

**Scenario:** ABC s.r.o. receives invoice for IT services from domestic supplier.
- Invoice total: 738.00 EUR
- Tax base: 600.00 EUR
- DPH 23%: 138.00 EUR

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Service cost (ostatne sluzby) | 518 | 321 | 600.00 |
| 2 | Input DPH | 343 | 321 | 138.00 |

**DPH treatment:** Standard input VAT, deductible
**KV DPH section:** B.2
**Legal source:** Postupy uctovania (ucet 518), DPH law SS 49

### Example 2.2: Purchase of service from EU (reverse charge on services)

**Scenario:** ABC s.r.o. purchases consulting services from Austrian company AT GmbH.
- Invoice total: 3,000.00 EUR (without DPH, B2B reverse charge)
- Place of supply: Slovakia (SS 15 ods. 1 DPH law - B2B rule)
- Slovak DPH 23% self-assessed: 690.00 EUR

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Service cost | 518 | 321 | 3,000.00 |
| 2 | Self-assessed DPH - output (danova povinnost) | 349 | 343 | 690.00 |
| 3 | Self-assessed DPH - input (narok na odpocet) | 343 | 349 | 690.00 |

**DPH treatment:** Reverse charge on cross-border B2B services (SS 69 ods. 3). Recipient self-assesses.
**KV DPH section:** B.1 (received invoice, buyer liable for tax per SS 69)
**DPH return:** Line 12 (services received from EU) and line 20 (deduction)
**Suhrnny vykaz:** Not reported (buyer does not report in EC Sales List)
**Legal source:** DPH law SS 15 ods. 1 (place of supply), SS 69 ods. 3

### Example 2.3: Purchase of service from non-EU country

**Scenario:** ABC s.r.o. purchases software license from US company.
- Invoice total: 1,500.00 USD = 1,380.00 EUR (at ECB rate)
- DPH 23% self-assessed: 317.40 EUR

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Service cost | 518 | 321 | 1,380.00 |
| 2 | Self-assessed DPH - output | 349 | 343 | 317.40 |
| 3 | Self-assessed DPH - input | 343 | 349 | 317.40 |

**DPH treatment:** Same as EU service (reverse charge per SS 69 ods. 3). Place of supply is Slovakia for B2B.
**KV DPH section:** B.1
**Legal source:** DPH law SS 15 ods. 1, SS 69 ods. 3

---

## 3. Nakup tovaru na predaj (Purchase of Inventory for Resale)

### Example 3.1: Purchase of goods for resale, domestic

**Scenario:** ABC s.r.o. purchases goods for resale from domestic wholesaler.
- Invoice total: 6,150.00 EUR
- Tax base: 5,000.00 EUR
- DPH 23%: 1,150.00 EUR

**Booking (method A - using stock accounts):**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Goods received to stock (tovar na sklade) | 132 | 321 | 5,000.00 |
| 2 | Input DPH | 343 | 321 | 1,150.00 |

**Booking (method B - direct to expense on purchase):**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Goods purchased (nakup tovaru) | 504 | 321 | 5,000.00 |
| 2 | Input DPH | 343 | 321 | 1,150.00 |

**DPH treatment:** Standard input VAT, deductible
**KV DPH section:** B.2
**Legal source:** Postupy uctovania SS 35-37 (ucet 132, 504)

### Example 3.2: Purchase of goods from EU supplier (intra-community acquisition)

**Scenario:** ABC s.r.o. purchases electronics for resale from Polish supplier.
- Invoice total: 8,000.00 EUR (without DPH)
- DPH 23% self-assessed: 1,840.00 EUR

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Goods to stock | 132 | 321 | 8,000.00 |
| 2 | Self-assessed DPH - output | 349 | 343 | 1,840.00 |
| 3 | Self-assessed DPH - input | 343 | 349 | 1,840.00 |

**DPH treatment:** Intra-community acquisition
**KV DPH section:** B.1
**Legal source:** DPH law SS 11, SS 69 ods. 6

---

## 4. Nakup dlhodobeho majetku (Purchase of Fixed Assets)

### Example 4.1: Purchase of machinery (independently movable asset)

**Scenario:** ABC s.r.o. purchases CNC machine from domestic supplier.
- Invoice total: 24,600.00 EUR
- Tax base: 20,000.00 EUR
- DPH 23%: 4,600.00 EUR
- Useful life: 6 years (depreciation group 2)

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Asset acquisition (obstaranie DHM) | 042 | 321 | 20,000.00 |
| 2 | Input DPH | 343 | 321 | 4,600.00 |
| 3 | Asset placed in service (zaradenie do pouzitia) | 022 | 042 | 20,000.00 |

**Note:** Step 3 occurs when the asset is ready for use, not necessarily when the invoice is received.

**DPH treatment:** Standard input VAT, deductible
**KV DPH section:** B.2
**Legal source:** Postupy uctovania SS 22-26 (DHM), DPH law SS 49
**Depreciation:** Account 551/082, annual amount depends on method (straight-line or accelerated)

### Example 4.2: Purchase of passenger vehicle (partial DPH deduction)

**Scenario:** ABC s.r.o. purchases a company car. Car is used 70% for business, 30% personal.
- Invoice total: 36,900.00 EUR
- Tax base: 30,000.00 EUR
- DPH 23%: 6,900.00 EUR
- Deductible DPH (70%): 4,830.00 EUR
- Non-deductible DPH (30%): 2,070.00 EUR

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Asset acquisition | 042 | 321 | 30,000.00 |
| 2 | Deductible DPH (70%) | 343 | 321 | 4,830.00 |
| 3 | Non-deductible DPH added to asset cost | 042 | 321 | 2,070.00 |
| 4 | Asset placed in service | 022 | 042 | 32,070.00 |

**DPH treatment:** Proportional deduction per SS 49 ods. 5. Non-deductible DPH increases asset cost.
**KV DPH section:** B.2 (only deductible portion)
**Legal source:** DPH law SS 49 ods. 5 (pomerny odpocet)

---

## 5. Zalohy dodavatelom (Advance Payments to Suppliers)

### Example 5.1: Advance payment to domestic supplier (VAT payer)

**Scenario:** ABC s.r.o. pays advance of 2,460.00 EUR for future material delivery.
- Advance: 2,460.00 EUR (incl. DPH)
- Tax base: 2,000.00 EUR
- DPH 23%: 460.00 EUR
- Supplier issues tax document for received payment.

**Step 1 - Payment of advance:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Advance payment to supplier | 314 | 221 | 2,460.00 |

**Step 2 - Received tax document for advance (danovy doklad k prijatej platbe):**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 2 | DPH from advance (input) | 343 | 314 | 460.00 |

**Step 3 - Final invoice received (6,150 EUR total, 5,000 base, 1,150 DPH):**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 3 | Material (full base) | 112 | 321 | 5,000.00 |
| 4 | DPH on final invoice (full) | 343 | 321 | 1,150.00 |
| 5 | Settlement of advance (base portion) | 321 | 314 | 2,000.00 |
| 6 | DPH correction from advance | 321 | 343 | 460.00 |
| 7 | Payment of remaining amount | 321 | 221 | 3,690.00 |

**DPH treatment:** DPH arises on advance when payment is received by supplier. Final invoice settles the difference.
**KV DPH section:** B.2 (both advance tax document and final invoice)
**Legal source:** DPH law SS 19 ods. 4 (danova povinnost pri platbe pred dodanim)

---

## 6. Predaj tovaru (Sale of Goods)

### Example 6.1: Sale of goods to domestic customer

**Scenario:** ABC s.r.o. sells goods to domestic customer.
- Invoice total: 3,690.00 EUR
- Tax base: 3,000.00 EUR
- DPH 23%: 690.00 EUR
- Cost of goods sold: 2,200.00 EUR

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Revenue from sale (trzby za tovar) | 311 | 604 | 3,000.00 |
| 2 | Output DPH (DPH na vystupe) | 311 | 343 | 690.00 |
| 3 | Cost of goods sold (naklady na predany tovar) | 504 | 132 | 2,200.00 |

**DPH treatment:** Standard output VAT, liability to state
**KV DPH section:** A.1 (issued invoice to VAT payer) or D.2 (non-VAT payer, not via ERP)
**Legal source:** Postupy uctovania (ucet 604, 504)

### Example 6.2: Sale of goods to EU customer (intra-community supply)

**Scenario:** ABC s.r.o. sells goods to Czech customer CZ s.r.o.
- Invoice total: 5,000.00 EUR (without DPH - exempt intra-community supply)
- Customer VAT ID: CZ12345678
- Cost of goods sold: 3,500.00 EUR

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Revenue from sale | 311 | 604 | 5,000.00 |
| 2 | Cost of goods sold | 504 | 132 | 3,500.00 |

**Note:** No DPH line - supply is exempt with right to deduction (oslobodene s narokom na odpocet).

**DPH treatment:** Exempt intra-community supply per SS 43 DPH law. No Slovak DPH charged.
**KV DPH section:** Not in KV DPH
**Suhrnny vykaz (EC Sales List):** Must be reported (customer VAT ID + value of supply)
**DPH return:** Line 15 (dodanie tovaru do EU) and line 16 (goods)
**Legal source:** DPH law SS 43 (oslobodenie pri dodani tovaru do EU)

### Example 6.3: Retail cash sale (e-kasa / ERP)

**Scenario:** ABC s.r.o. makes retail sale via electronic cash register.
- Cash received: 49.20 EUR
- Tax base: 40.00 EUR
- DPH 23%: 9.20 EUR

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Cash received | 211 | 604 | 40.00 |
| 2 | Output DPH | 211 | 343 | 9.20 |

**DPH treatment:** Standard output VAT
**KV DPH section:** D.1 (sale via ERP / e-kasa)
**Legal source:** DPH law SS 71-75 (zjednodusena faktura)

---

## 7. Predaj sluzieb (Sale of Services)

### Example 7.1: Sale of service to domestic customer

**Scenario:** ABC s.r.o. invoices consulting services to Slovak client.
- Invoice total: 2,460.00 EUR
- Tax base: 2,000.00 EUR
- DPH 23%: 460.00 EUR

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Revenue from services (trzby za sluzby) | 311 | 602 | 2,000.00 |
| 2 | Output DPH | 311 | 343 | 460.00 |

**DPH treatment:** Standard output VAT
**KV DPH section:** A.1 (issued invoice to VAT payer) or D.2 (to non-VAT payer)
**Legal source:** Postupy uctovania (ucet 602)

### Example 7.2: Sale of service to EU customer (B2B)

**Scenario:** ABC s.r.o. provides IT development services to German client DE GmbH.
- Invoice total: 8,500.00 EUR (without DPH)
- Customer VAT ID: DE987654321
- Place of supply: Germany (SS 15 ods. 1 - B2B recipient country)

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Revenue from services | 311 | 602 | 8,500.00 |

**Note:** No DPH line. Place of supply is customer's country. Reverse charge applies - German customer self-assesses German VAT.

**DPH treatment:** Not subject to Slovak DPH. Place of supply outside SK.
**KV DPH section:** Not in KV DPH
**Suhrnny vykaz:** Must be reported (customer VAT ID + value, code 0 for services)
**DPH return:** Line 15 (sluzby s miestom dodania v EU)
**Legal source:** DPH law SS 15 ods. 1, invoice must state "prenesenie danovej povinnosti"

### Example 7.3: Sale of service to non-EU customer

**Scenario:** ABC s.r.o. provides consulting to US client.
- Invoice total: 4,000.00 EUR (without DPH)
- Place of supply: USA (SS 15 ods. 1 - B2B recipient country)

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Revenue from services | 311 | 602 | 4,000.00 |

**DPH treatment:** Not subject to Slovak DPH. Place of supply outside SK/EU.
**KV DPH section:** Not in KV DPH
**Suhrnny vykaz:** Not reported (only EU customers)
**DPH return:** Line 15 (sluzby s miestom dodania mimo SR)
**Legal source:** DPH law SS 15 ods. 1

---

## 8. Predaj dlhodobeho majetku (Sale of Fixed Assets)

### Example 8.1: Sale of fully depreciated machine

**Scenario:** ABC s.r.o. sells a machine that is fully depreciated.
- Original cost: 12,000.00 EUR
- Accumulated depreciation: 12,000.00 EUR (net book value = 0)
- Sale price: 2,460.00 EUR (incl. DPH)
- Tax base: 2,000.00 EUR
- DPH 23%: 460.00 EUR

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Revenue from asset sale | 311 | 641 | 2,000.00 |
| 2 | Output DPH | 311 | 343 | 460.00 |
| 3 | Derecognition - accumulated depreciation | 082 | 022 | 12,000.00 |

**DPH treatment:** Standard output VAT on sale price
**KV DPH section:** A.1
**Legal source:** Postupy uctovania SS 25 ods. 6 (vyradenie predajom)

### Example 8.2: Sale of partially depreciated vehicle

**Scenario:** ABC s.r.o. sells a company car after 3 years.
- Original cost: 30,000.00 EUR
- Accumulated depreciation: 18,000.00 EUR
- Net book value (zostatova cena): 12,000.00 EUR
- Sale price: 18,450.00 EUR (incl. DPH)
- Tax base: 15,000.00 EUR
- DPH 23%: 3,450.00 EUR

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Revenue from asset sale | 311 | 641 | 15,000.00 |
| 2 | Output DPH | 311 | 343 | 3,450.00 |
| 3 | Residual value to expense (zostatova cena) | 541 | 082 | 12,000.00 |
| 4 | Derecognition of asset | 082 | 022 | 30,000.00 |

**Note:** Steps 3-4 write off the asset: remaining book value goes to expense 541, then accumulated depreciation clears against asset account.

**DPH treatment:** Standard output VAT
**KV DPH section:** A.1
**Legal source:** Postupy uctovania SS 25 ods. 6

---

## 9. Prijate zalohy od odberatelov (Advance Payments from Customers)

### Example 9.1: Received advance from domestic customer (VAT payer)

**Scenario:** ABC s.r.o. receives advance payment from customer for future service delivery.
- Advance received: 4,920.00 EUR
- Tax base: 4,000.00 EUR
- DPH 23%: 920.00 EUR
- ABC must issue tax document within 15 days of receiving payment.

**Step 1 - Advance received to bank:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Advance received | 221 | 324 | 4,920.00 |

**Step 2 - Issue tax document for received advance:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 2 | Output DPH from advance | 324 | 343 | 920.00 |

**Step 3 - Final invoice issued (total service 12,300 EUR = 10,000 base + 2,300 DPH):**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 3 | Revenue (full base) | 311 | 602 | 10,000.00 |
| 4 | Output DPH (full invoice) | 311 | 343 | 2,300.00 |
| 5 | Settlement of advance | 324 | 311 | 4,000.00 |
| 6 | DPH correction from advance | 343 | 311 | 920.00 |
| 7 | Receipt of remaining payment | 221 | 311 | 7,380.00 |

**DPH treatment:** DPH obligation arises when advance is received (SS 19 ods. 4). Final invoice adjusts.
**KV DPH section:** A.1 (both advance tax document and final invoice)
**Legal source:** DPH law SS 19 ods. 4, SS 72-74

---

## 10. Standardna DPH (23%) - Summary Patterns

### Example 10.1: Supplier invoice with standard DPH

**Standard pattern for any received invoice with 23% DPH:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Expense/Asset account | 5xx/0xx | 321 | tax_base |
| 2 | Input DPH 23% | 343 | 321 | tax_base * 0.23 |

**Total on account 321:** tax_base * 1.23

### Example 10.2: Customer invoice with standard DPH

**Standard pattern for any issued invoice with 23% DPH:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Revenue account | 311 | 6xx | tax_base |
| 2 | Output DPH 23% | 311 | 343 | tax_base * 0.23 |

**Total on account 311:** tax_base * 1.23

---

## 11. Znizena DPH (19%, 5%)

### Example 11.1: Purchase of food products at 19% DPH

**Scenario:** Restaurant ABC s.r.o. purchases food supplies.
- Invoice total: 1,190.00 EUR
- Tax base: 1,000.00 EUR
- DPH 19%: 190.00 EUR

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Material (potraviny) | 112 | 321 | 1,000.00 |
| 2 | Input DPH 19% | 343 | 321 | 190.00 |

**DPH treatment:** Reduced rate I (19%) applicable to selected food products per Annex 7 DPH law
**KV DPH section:** B.2

### Example 11.2: Sale of newspapers/periodicals at 5% DPH

**Scenario:** Publisher ABC s.r.o. sells periodical subscriptions.
- Invoice total: 1,050.00 EUR
- Tax base: 1,000.00 EUR
- DPH 5%: 50.00 EUR

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Revenue from goods/services | 311 | 604 | 1,000.00 |
| 2 | Output DPH 5% | 311 | 343 | 50.00 |

**DPH treatment:** Reduced rate II (5%) applicable to newspapers, periodicals, books per Annex 7a DPH law
**KV DPH section:** A.1

---

## 12. Tuzemske samozdanenie (Domestic Reverse Charge)

### Example 12.1: Construction services - domestic reverse charge (SS 69 ods. 12 pism. j)

**Scenario:** ABC s.r.o. (VAT payer) receives invoice for construction work from SK contractor.
- Invoice total: 15,000.00 EUR (without DPH - domestic reverse charge)
- Invoice states: "Prenesenie danovej povinnosti podla SS 69 ods. 12 pism. j) zakona o DPH"
- DPH 23% self-assessed: 3,450.00 EUR

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Construction services cost | 518 | 321 | 15,000.00 |
| 2 | Self-assessed DPH - output (danova povinnost) | 343 | 343 | 3,450.00 |
| 3 | Self-assessed DPH - input (narok na odpocet) | 343 | 343 | 3,450.00 |

**Note:** Analytically, output DPH goes to 343.AE (output analytic) and input DPH to 343.AE (input analytic). In practice, two separate analytical accounts of 343 are used.

**Alternative booking with account 395 as clearing:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Construction services cost | 518 | 321 | 15,000.00 |
| 2 | Self-assessed DPH - output | 395 | 343 | 3,450.00 |
| 3 | Self-assessed DPH - input | 343 | 395 | 3,450.00 |

**DPH treatment:** Domestic reverse charge. Supplier invoices without DPH. Buyer self-assesses both output and input DPH. Net effect = 0 for full deduction.
**KV DPH section:** B.1 (received invoice with reverse charge)
**Supplier's KV DPH section:** A.2 (issued invoice with transferred liability)
**Legal source:** DPH law SS 69 ods. 12 pism. j) (stavebne prace)

### Example 12.2: Delivery of mobile phones > 5,000 EUR base

**Scenario:** ABC s.r.o. purchases mobile phones from domestic wholesaler, base > 5,000 EUR.
- Invoice total: 8,000.00 EUR (without DPH)
- DPH 23% self-assessed: 1,840.00 EUR

**Booking:** Same pattern as 12.1 (service cost replaced by goods account 504 or 132).
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Goods purchased | 132 | 321 | 8,000.00 |
| 2 | Self-assessed DPH - output | 395 | 343 | 1,840.00 |
| 3 | Self-assessed DPH - input | 343 | 395 | 1,840.00 |

**DPH treatment:** Domestic reverse charge per SS 69 ods. 12 pism. h) (mobile phones when base >= 5,000 EUR)
**KV DPH section:** B.1
**Legal source:** DPH law SS 69 ods. 12 pism. h)

---

## 13. Reverse Charge - Intra-Community Acquisition

### Example 13.1: Intra-community acquisition of goods

**Scenario:** ABC s.r.o. purchases machinery from Italian supplier IT S.r.l.
- Invoice: 10,000.00 EUR (without DPH)
- Supplier VAT ID: IT01234567890
- DPH 23% self-assessed: 2,300.00 EUR

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Asset acquisition | 042 | 321 | 10,000.00 |
| 2 | Self-assessed DPH - output | 349 | 343 | 2,300.00 |
| 3 | Self-assessed DPH - input | 343 | 349 | 2,300.00 |
| 4 | Asset placed in service | 022 | 042 | 10,000.00 |

**DPH treatment:** Intra-community acquisition per SS 11. Buyer self-assesses.
**KV DPH section:** B.1
**DPH return:** Lines 07-08 (nadobudnutie) and line 20 (odpocet)
**Legal source:** DPH law SS 11, SS 69 ods. 6

### Example 13.2: Triangulation (trojstranny obchod)

**Scenario:** ABC s.r.o. (SK) buys from DE GmbH and sells to CZ s.r.o. Goods shipped directly DE -> CZ.
- Purchase: 6,000.00 EUR from DE
- Sale: 8,000.00 EUR to CZ

ABC is the intermediary (prostredna osoba). Under triangulation simplification:

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Purchase of goods | 504 | 321 | 6,000.00 |
| 2 | Revenue from sale | 311 | 604 | 8,000.00 |

**DPH treatment:** ABC does not self-assess DPH on acquisition (simplification per SS 45). CZ customer self-assesses. No Slovak DPH on either side.
**KV DPH section:** Not in KV DPH
**Suhrnny vykaz:** Reported with code 1 (trojstranny obchod)
**Legal source:** DPH law SS 45 (trojstranny obchod)

---

## 14. Oslobodene plnenia (Exempt Transactions)

### Example 14.1: Exempt financial services

**Scenario:** ABC s.r.o. receives invoice for bank loan arrangement fee.
- Invoice total: 500.00 EUR (exempt from DPH)

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Financial service cost | 568 | 321 | 500.00 |

**DPH treatment:** Exempt without right to deduction per SS 39 (financne sluzby). No DPH charged or deducted.
**KV DPH section:** Not reported (exempt)
**Legal source:** DPH law SS 39

### Example 14.2: Exempt rent of residential property

**Scenario:** ABC s.r.o. rents apartment to employee (residential rent).
- Monthly rent: 800.00 EUR

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Rental revenue | 311 | 602 | 800.00 |

**DPH treatment:** Exempt per SS 38 ods. 3 (prenajom bytu). No DPH charged.
**KV DPH section:** Not reported
**Legal source:** DPH law SS 38 ods. 3

---

## 15. DPH vyuctovanie (DPH Return Settlement)

### Example 15.1: DPH return - liability to pay (vlastna danova povinnost)

**Scenario:** End of DPH period. Output DPH > Input DPH.
- Output DPH (on 343 credit side): 5,200.00 EUR
- Input DPH (on 343 debit side): 3,800.00 EUR
- DPH payable: 1,400.00 EUR

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Close output DPH analytic | 343.vystup | 343.zuctovanie | 5,200.00 |
| 2 | Close input DPH analytic | 343.zuctovanie | 343.vstup | 3,800.00 |
| 3 | DPH payment to tax office | 343.zuctovanie | 221 | 1,400.00 |

**Note:** Account 343 uses analytical accounts: 343.vstup (input), 343.vystup (output), 343.zuctovanie (settlement). After settlement, 343 balance = 0.

**Legal source:** DPH law SS 78 (danove priznanie)

### Example 15.2: DPH return - excessive deduction (nadmerny odpocet)

**Scenario:** Input DPH > Output DPH.
- Output DPH: 2,100.00 EUR
- Input DPH: 4,500.00 EUR
- DPH receivable (nadmerny odpocet): 2,400.00 EUR

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Close output DPH | 343.vystup | 343.zuctovanie | 2,100.00 |
| 2 | Close input DPH | 343.zuctovanie | 343.vstup | 4,500.00 |
| 3 | DPH refund received from tax office | 221 | 343.zuctovanie | 2,400.00 |

**Note:** Tax office returns excessive deduction within 30 days (or offsets against other tax liabilities).
**Legal source:** DPH law SS 79 (nadmerny odpocet)

---

## 16. Mzdy (Salary Accrual)

### Example 16.1: Monthly payroll for one employee

**Scenario:** Employee gross salary 2,000.00 EUR.
- Employee social insurance (9.4%): 188.00 EUR
- Employee health insurance (4%): 80.00 EUR
- Employee income tax advance: 148.52 EUR
- Net salary: 1,583.48 EUR
- Employer social insurance (25.2%): 504.00 EUR
- Employer health insurance (10%): 200.00 EUR

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Gross wages (hruba mzda) | 521 | 331 | 2,000.00 |
| 2 | Employee social insurance | 331 | 336.SP | 188.00 |
| 3 | Employee health insurance | 331 | 336.ZP | 80.00 |
| 4 | Employee income tax advance | 331 | 342 | 148.52 |
| 5 | Net salary payment | 331 | 221 | 1,583.48 |
| 6 | Employer social insurance | 524 | 336.SP | 504.00 |
| 7 | Employer health insurance | 524 | 336.ZP | 200.00 |
| 8 | Payment of social insurance (employee + employer) | 336.SP | 221 | 692.00 |
| 9 | Payment of health insurance (employee + employer) | 336.ZP | 221 | 280.00 |
| 10 | Payment of income tax advance | 342 | 221 | 148.52 |

**Note:** Account 336 uses analytical accounts per institution: 336.SP (Socialna poistovna), 336.ZP (zdravotna poistovna).

**DPH treatment:** N/A (wages are not subject to DPH)
**Legal source:** Zakon o socialnom poisteni, Zakon o zdravotnom poisteni, Zakon o dani z prijmov

### Example 16.2: Payroll with tax bonus (danovy bonus)

**Scenario:** Employee with 1 child under 18. Monthly tax bonus: 140.00 EUR.
- Same salary as 16.1
- Tax advance before bonus: 148.52 EUR
- Tax bonus: 140.00 EUR
- Net tax to withhold: 8.52 EUR

**Booking (differences from 16.1):**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 4a | Tax bonus (reduces tax liability) | 342 | 331 | 140.00 |
| 4b | Income tax advance (net) | 331 | 342 | 148.52 |

**Net salary increases by tax bonus amount.**
**Legal source:** Zakon o dani z prijmov SS 33 (danovy bonus)

---

## 17. Socialne poistenie (Social Insurance) - Employer Rates 2025

### Summary of employer social insurance rates:

| Component | Employee % | Employer % |
|-----------|-----------|-----------|
| Nemocenske poistenie (sickness) | 1.4% | 1.4% |
| Starobne poistenie (old-age pension) | 4.0% | 14.0% |
| Invalidne poistenie (disability) | 3.0% | 3.0% |
| Poistenie v nezamestnanosti (unemployment) | 1.0% | 1.0% |
| Garacny fond | 0% | 0.25% |
| Rezervny fond solidarity | 0% | 4.75% |
| Urazove poistenie (accident) | 0% | 0.8% |
| **TOTAL Social Insurance** | **9.4%** | **25.2%** |
| Health insurance | 4.0% | 10.0% |
| **TOTAL Employee + Employer** | **13.4%** | **35.2%** |

### Example 17.1: Social insurance payment

Covered in Example 16.1, lines 6 and 8. Predkontacia: 524/336.SP (accrual), 336.SP/221 (payment).

---

## 18. Zdravotne poistenie (Health Insurance)

### Example 18.1: Health insurance payment

Covered in Example 16.1, lines 7 and 9. Predkontacia: 524/336.ZP (accrual), 336.ZP/221 (payment).

**Note for annual reconciliation (rocne zuctovanie):**
Health insurance companies perform annual reconciliation. Underpayment or overpayment:
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Additional employer payment (nedoplatok) | 524 | 336.ZP | amount |
| 2 | Refund to employer (preplatok) | 336.ZP | 524 | amount |

---

## 19. Odpisy (Depreciation)

### Example 19.1: Straight-line depreciation of machinery

**Scenario:** Machine with acquisition cost 20,000.00 EUR, depreciation group 2 (6 years).
- Annual depreciation: 20,000 / 6 = 3,333.33 EUR
- First year (tax): 20,000 / 12 = 1,666.67 EUR (half in first year under tax rules)

**Monthly accounting depreciation booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Monthly depreciation (odpis DHM) | 551 | 082 | 277.78 |

**Note:** Account 082 = Opravky k samostatne hnutelnym veciam. Accumulates depreciation. After full depreciation, 082 balance = 022 balance.

**Depreciation accounts by asset type:**
- 551/081 = Buildings (stavby)
- 551/082 = Machinery and equipment (samostatne hnutelne veci)
- 551/073 = Software
- 551/071 = Capitalized development costs

**Legal source:** Postupy uctovania SS 28, Zakon o dani z prijmov SS 26-28 (danove odpisy)

### Example 19.2: Accelerated depreciation (zrychlene odpisy)

**Scenario:** Same machine, depreciation group 2 (coefficient 6).
- Year 1: 20,000 / 6 = 3,333.33 EUR
- Year 2: (2 * (20,000 - 3,333.33)) / (7 - 2) = 6,666.67 EUR
- And so on with declining balance.

**Booking:** Same predkontacia 551/082, only amounts differ.

---

## 20. Bankove poplatky (Bank Charges)

### Example 20.1: Monthly bank maintenance fee

**Scenario:** Monthly bank fee 15.00 EUR.

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Bank charges | 568 | 221 | 15.00 |

**DPH treatment:** Bank services are exempt from DPH (SS 39). No DPH to deduct.
**KV DPH section:** N/A
**Legal source:** DPH law SS 39 (financne cinnosti)

### Example 20.2: Foreign currency transaction fee

**Scenario:** Fee for international payment 25.00 EUR.

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Bank charges (foreign payment) | 568 | 221 | 25.00 |

### Example 20.3: Bank interest received

**Scenario:** Interest credited to account 8.50 EUR.

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Interest income | 221 | 662 | 8.50 |

---

## 21. Uzavierkove uctovne pripady (Year-End Closing Entries)

### Example 21.1: Closing revenue and expense accounts (uzavieranie uctov)

**Scenario:** Year-end. Close all revenue (class 6) and expense (class 5) accounts to account 710 (Ucet ziskov a strat).

**Closing expense accounts:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Close material consumption | 710 | 501 | total_501 |
| 2 | Close services | 710 | 518 | total_518 |
| 3 | Close wages | 710 | 521 | total_521 |
| 4 | Close social insurance | 710 | 524 | total_524 |
| 5 | Close depreciation | 710 | 551 | total_551 |
| ... | (all other expense accounts) | 710 | 5xx | amount |

**Closing revenue accounts:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 6 | Close service revenue | 602 | 710 | total_602 |
| 7 | Close goods revenue | 604 | 710 | total_604 |
| 8 | Close asset sale revenue | 641 | 710 | total_641 |
| ... | (all other revenue accounts) | 6xx | 710 | amount |

**The balance on 710 = profit or loss for the period.**

### Example 21.2: Transfer profit to balance sheet

**Scenario:** Company has profit of 25,000.00 EUR.

| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Close P&L to retained earnings | 710 | 431 | 25,000.00 |

**At next year's AGM decision:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 2a | Transfer to retained earnings | 431 | 428 | 25,000.00 |
| OR | | | | |
| 2b | Dividend distribution | 431 | 364 | 25,000.00 |

### Example 21.3: Closing balance sheet accounts

**Scenario:** Close all balance sheet accounts to account 702 (Konecny ucet suvahovy).

| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Close asset accounts | 702 | 0xx/1xx/2xx/3xx | balance |
| 2 | Close liability/equity accounts | 3xx/4xx | 702 | balance |

### Example 21.4: Accruals and deferrals (casove rozlisenie)

**Scenario:** Insurance paid in advance for next year: 1,200.00 EUR (prepaid in December for January-December next year).

**Booking in December (current year):**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Prepaid expense (naklady buduc. obdobi) | 381 | 221 | 1,200.00 |

**Monthly booking in next year (January through December):**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Insurance expense (dissolving prepaid) | 548 | 381 | 100.00 |

---

## 22. Dobropisy / Opravne faktury (Credit Notes / Corrections)

### Example 22.1: Credit note received from supplier (reduction of invoice)

**Scenario:** Supplier issues credit note for 369.00 EUR (300.00 base + 69.00 DPH at 23%) due to quality complaint.

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Reduction of expense/cost | 321 | 501 | 300.00 |
| 2 | Reduction of input DPH | 321 | 343 | 69.00 |

**Note:** This is effectively a reversal of the original posting (accounts are swapped vs original invoice).

**DPH treatment:** Reduces input DPH in the period when credit note is received
**KV DPH section:** C.2 (opravna faktura k prijatej fakture)
**Legal source:** DPH law SS 25 (oprava zakladu dane), SS 53

### Example 22.2: Credit note issued to customer

**Scenario:** ABC s.r.o. issues credit note to customer for 615.00 EUR (500.00 base + 115.00 DPH at 23%) due to returned goods.

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Revenue reduction | 604 | 311 | 500.00 |
| 2 | Output DPH reduction | 343 | 311 | 115.00 |
| 3 | Goods returned to stock | 132 | 504 | 380.00 |

**DPH treatment:** Reduces output DPH in period of credit note
**KV DPH section:** C.1 (opravna faktura k vydanej fakture)
**Legal source:** DPH law SS 25, SS 53

### Example 22.3: Charge note (tarchopis) - increase of original invoice

**Scenario:** Supplier issues charge note for additional 246.00 EUR (200.00 base + 46.00 DPH).

**Booking:**
| # | Description | MD (Debit) | D (Credit) | Amount EUR |
|---|------------|------------|------------|------------|
| 1 | Additional expense | 501 | 321 | 200.00 |
| 2 | Additional input DPH | 343 | 321 | 46.00 |

**DPH treatment:** Same as standard received invoice (additional DPH deductible)
**KV DPH section:** C.2 (opravna faktura)
**Legal source:** DPH law SS 25

---

## KV DPH Section Reference Summary

| Section | What goes there | Threshold/Condition |
|---------|----------------|-------------------|
| A.1 | Issued invoices to VAT payers | Standard issued invoices |
| A.2 | Issued invoices - domestic reverse charge | Supplier transfers DPH liability |
| B.1 | Received invoices - reverse charge (domestic and EU) | Buyer is person liable to pay DPH |
| B.2 | Standard received invoices | Domestic supplier, standard DPH deduction |
| B.3.1 | Simplified invoices (aggregate < 3,000 EUR) | e-kasa receipts, fuel receipts, sum < 3,000 |
| B.3.2 | Simplified invoices (aggregate >= 3,000 EUR) | Same docs, sum >= 3,000, by supplier |
| C.1 | Issued credit/charge notes | Corrections to A.1/A.2 invoices |
| C.2 | Received credit/charge notes | Corrections to B.1/B.2 invoices |
| D.1 | Sales via e-kasa / ERP | Retail sales through cash register |
| D.2 | Other output without e-kasa | Sales to non-VAT payers not via ERP |

---

## Account Number Reference

### Key accounts used in examples:

| Account | Name | Class |
|---------|------|-------|
| 022 | Samostatne hnutelne veci (Machinery) | Asset |
| 042 | Obstaranie DHM (Asset acquisition) | Asset |
| 081 | Opravky k stavbam | Contra-asset |
| 082 | Opravky k sam. hnut. veciam | Contra-asset |
| 112 | Material na sklade (Material on stock) | Asset |
| 132 | Tovar na sklade (Goods on stock) | Asset |
| 211 | Pokladnica (Cash) | Asset |
| 221 | Bankove ucty (Bank accounts) | Asset |
| 261 | Peniaze na ceste (Money in transit) | Asset |
| 311 | Odberatelia (Accounts receivable) | Asset |
| 314 | Poskytnute preddavky (Advances given) | Asset |
| 315 | Ostatne pohladavky (Other receivables) | Asset |
| 321 | Dodavatelia (Accounts payable) | Liability |
| 324 | Prijate preddavky (Advances received) | Liability |
| 325 | Ostatne zavazky (Other payables) | Liability |
| 331 | Zamestnanci (Employees) | Liability |
| 335 | Pohladavky voci zamestnancom | Asset |
| 336 | Zuct. s organmi SP a ZP (Insurance bodies) | Liability |
| 342 | Ostatne priame dane (Income tax) | Liability |
| 343 | Dan z pridanej hodnoty (DPH/VAT) | Asset/Liability |
| 349 | Vyrovnanie DPH (IC acquisition clearing) | Asset/Liability |
| 364 | Zavazky voci spolocnikom (Dividends) | Liability |
| 365 | Ostatne zavazky voci spolocnikom | Liability |
| 371 | Pohladavky z predaja podniku | Asset |
| 378 | Ine pohladavky | Asset |
| 379 | Ine zavazky (Other liabilities - customs) | Liability |
| 381 | Naklady buduc. obdobi (Prepaid expenses) | Asset |
| 395 | Vnutorne zuctovanie (Internal clearing) | Clearing |
| 428 | Nerozdeleny zisk (Retained earnings) | Equity |
| 431 | Vysledok hospodarenia v schvalovani | Equity |
| 501 | Spotreba materialu (Material consumption) | Expense |
| 504 | Predany tovar (Cost of goods sold) | Expense |
| 518 | Ostatne sluzby (Services) | Expense |
| 521 | Mzdove naklady (Wages) | Expense |
| 524 | Zakonne socialne poistenie (Social insurance) | Expense |
| 541 | Zostatova cena predaneho DHM | Expense |
| 543 | Dary (Donations) | Expense |
| 548 | Ostatne prevadzkove naklady | Expense |
| 551 | Odpisy DHM a DNM (Depreciation) | Expense |
| 568 | Ostatne financne naklady (Bank fees) | Expense |
| 602 | Trzby za sluzby (Service revenue) | Revenue |
| 604 | Trzby za tovar (Goods revenue) | Revenue |
| 641 | Trzby z predaja DHM (Asset sale revenue) | Revenue |
| 648 | Ostatne prevadzkove vynosy | Revenue |
| 662 | Uroky (Interest income) | Revenue |
| 701 | Zaciatocny ucet suvahovy (Opening balance) | Technical |
| 702 | Konecny ucet suvahovy (Closing balance) | Technical |
| 710 | Ucet ziskov a strat (P&L) | Technical |
