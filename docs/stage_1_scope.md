# Stage 1: Posting Rules + Full DPH

**Status:** Defined (2026-03-13)
**Goal:** Prove the full architecture — source material → knowledge graph → execution rules → deterministic posting — on the two most critical regulatory domains.

---

## In Scope

### Graph 1: Posting Rules (full)
- All common s.r.o. transaction types (30+ types)
- Account mappings with conditions
- Debit/credit posting patterns
- Required input fields per transaction type
- Legal source references (Postupy účtovania paragraphs)

### Graph 2: DPH (full)
- All DPH rates (23% standard, 19% reduced, 5% reduced, 0% exempt)
- Standard input/output VAT
- Reverse charge (tuzemský samozdanenie)
- Intra-community supplies and acquisitions (§ 11, § 13)
- Exempt transactions (§ 28-42)
- DPH registration thresholds
- Place of supply rules
- Tax point (deň vzniku daňovej povinnosti)
- KV DPH section mapping (A1, A2, B1, B2, B3, C1, C2, D1, D2)
- Súhrnný výkaz mapping (IC supplies)
- Coefficient for partial deduction (§ 50)
- Adjustment of deducted DPH (§ 53, § 54)

### Deterministic Execution Engine
- Rule resolution (transaction type + conditions → matching rule)
- Posting generation (rule + amounts → journal entry lines)
- DPH calculation module (reads rates from Graph 2)
- Amount formula evaluation (tax_base, vat_amount, gross_amount)
- Priority ordering and conflict resolution when multiple rules match
- Invariant validation (debits = credits, balance sheet equation)

### Ledger Core
- Immutable journal entries schema
- Double-entry validation
- Period control (open/close fiscal periods)
- Chart of accounts for s.r.o. (rámcová účtová osnova pre podnikateľov)

### Execution Rule Schema
- The engineering contract between graph and engine
- Conditions, postings, tax treatment, report mapping
- Formula language for amount expressions
- Required inputs specification
- Legal source traceability
- Validity dates (valid_from / valid_to)
- Priority field for conflict resolution

### Test Fixtures
- 30+ transaction scenarios with accountant-approved expected outputs
- Full DPH treatment coverage in test cases
- Edge cases: reverse charge, IC, exempt, partial deduction
- Target: 90%+ match against certified accountant decisions

---

## Out of Scope (deferred to later stages)

| Component | Why deferred |
|-----------|-------------|
| Graph 3: Full Reporting (súvaha, VZaS, účtovná závierka, XML generation) | Not needed to prove core engine |
| Graph 4: Payroll (social/health insurance, income tax, deductions) | Entirely separate regulatory domain |
| AI Interaction Layer (intake wizard, Q&A, explanation) | Needs deterministic core first |
| Frontend UI | Engine-first, UI later |
| E-invoicing 2027 (EN 16931, PEPPOL, UBL XML) | Compliance deadline is Jan 2027 |
| eKasa integration | Cash register, not core accounting |
| Bank feeds (PSD2 / Salt Edge) | Integration layer, not core logic |
| Subscription billing / onboarding | Product layer |
| Multi-tenant RLS | Infrastructure, not domain logic |

---

## Regulatory Sources Consumed

| Source | What we extract |
|--------|----------------|
| **Postupy účtovania** (Opatrenie MF SR 23054/2002-92 + amendments) | All posting rules, account mappings, transaction type conditions |
| **DPH law** (Act 222/2004 Z.z. — consolidated) | All VAT rates, treatments, reverse charge rules, exemptions, thresholds, place of supply |
| **Finančná správa KV DPH guidelines** | KV DPH section classification logic (A1/A2/B1/B2/B3/C1/C2/D1/D2) |
| **Rámcová účtová osnova** (chart of accounts for podnikatelia) | Account codes, names, classes, types |
| **Zákon o účtovníctve** (Act 431/2002) | Core accounting principles, period rules, immutability requirements |

---

## Success Criteria

1. **Deterministic correctness** — engine produces correct journal entries for 30+ common s.r.o. transaction types
2. **Full DPH coverage** — standard, reduced, exempt, reverse charge, IC supplies all handled
3. **Accountant validation** — 90%+ match against certified accountant decisions on test fixtures
4. **Traceability** — every posting linked to legal source paragraph
5. **Rule-driven** — adding a new transaction type = adding a rule object, not writing code
6. **Versioned** — rules have validity dates, graph can be versioned per regulatory change

---

## What Stage 1 Proves

If Stage 1 succeeds, we've proven:
- The declarative regulatory model works for real Slovak accounting
- The deterministic engine can replace hard-coded if/else logic
- DPH (the densest regulatory domain) is fully captured in the graph
- New transaction types can be added by authoring rules, not code
- The architecture supports regulatory versioning

This is the foundation everything else builds on.
