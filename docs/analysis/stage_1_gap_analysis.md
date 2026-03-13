# Stage 1 Gap Analysis — Source Coverage

**Date:** 2026-03-13
**Purpose:** Verify that our regulatory sources inventory covers everything Stage 1 needs before starting extraction.

---

## Graph 1: Posting Rules

| Requirement | Source | Status | Notes |
|-------------|--------|--------|-------|
| All s.r.o. transaction types | Postupy účtovania (Opatrenie MF SR 23054/2002-92) | COVERED | Primary source — defines all booking rules |
| Account mappings (debit/credit per type) | Postupy účtovania §30-§78 | COVERED | Each section specifies accounts |
| Conditions that trigger rules | Postupy účtovania | COVERED | Conditions embedded in rule text |
| Chart of accounts (full, with descriptions) | Rámcová účtová osnova (slov-lex.sk PDF) | COVERED | Multiple sources: slov-lex, podnikajte.sk, poradca.sk, EUBA |
| Account classes 0-9 structure | Rámcová účtová osnova | COVERED | |
| Account types (asset/liability/equity/revenue/expense) | Rámcová účtová osnova + Postupy účtovania §1-§4 | COVERED | Class determines type |
| Practical booking examples (predkontácie) | ako-uctovat.sk, danovecentrum.sk | COVERED | Extensive worked examples |
| Legal source references per rule | Postupy účtovania paragraph numbers | COVERED | Each rule maps to § |

**Graph 1 verdict: FULLY COVERED** — no gaps.

---

## Graph 2: DPH (VAT)

| Requirement | Source | Status | Notes |
|-------------|--------|--------|-------|
| All DPH rates (23%, 19%, 5%, 0%) | DPH law §27 | COVERED | |
| Rate conditions (which goods/services get which rate) | DPH law §27 + Prílohy (Annexes) | PARTIALLY COVERED | Annexes with reduced-rate item lists not explicitly in our source inventory |
| Registration rules & thresholds | DPH law §4-§6 | COVERED | |
| Place of supply (goods) | DPH law §13-§14 | COVERED | |
| Place of supply (services) | DPH law §15-§18 | COVERED | |
| Tax point (deň vzniku daňovej povinnosti) | DPH law §19-§20 | COVERED | |
| Exempt transactions | DPH law §28-§42 | COVERED | |
| Reverse charge — domestic | DPH law §69 ods. 12 | COVERED | danovecentrum.sk has examples |
| Reverse charge — IC acquisition | DPH law §69 ods. 1-6 | COVERED | |
| Input VAT deduction | DPH law §49-§51 | COVERED | |
| Partial deduction coefficient | DPH law §50 | COVERED | |
| Adjustment of deducted DPH | DPH law §53-§54 | COVERED | |
| IC supplies (§ 11, § 13) | DPH law | COVERED | |
| Triangulation (trojstranný obchod) | DPH law §45 | PARTIALLY COVERED | Not explicitly listed in practical examples |
| DPH practical examples | danovecentrum.sk (multiple articles) | COVERED | 2022, 2023 examples + general |
| KV DPH section mapping | Finančná správa KV DPH methodology (2021 PDF) | COVERED | |
| KV DPH practical examples | danovecentrum.sk + podnikajte.sk | COVERED | Section A1/A2/B1-B3 examples |
| Súhrnný výkaz mapping | svdph20.xsd + instructions PDF | COVERED | |
| DPH return XSD schema | dph2025.xsd | COVERED | |
| KV DPH XSD schema | kv_dph_2025.xsd | COVERED | |

**Graph 2 verdict: MOSTLY COVERED** — two partial gaps:

### Gap 1: DPH Rate Annexes (Prílohy)
The DPH law §27 references Annexes (Prílohy) that list specific goods/services qualifying for reduced rates (19%, 5%). These annexes are part of the law but not explicitly listed as separate downloadable sources.

**Resolution:** The annexes are part of the consolidated DPH law text on slov-lex.sk. When we extract dph_law.md, we must include the Prílohy, not just the main paragraphs.

### Gap 2: Triangulation Examples
Three-party trade (trojstranný obchod, §45) is covered in the law text but we lack practical booking examples.

**Resolution:** Search danovecentrum.sk or podnikajte.sk for triangulation examples during extraction. This is an edge case — not blocking for initial extraction.

---

## Ledger Core

| Requirement | Source | Status | Notes |
|-------------|--------|--------|-------|
| Immutability requirements | Zákon o účtovníctve (431/2002) §8 | COVERED | |
| Period control rules | Zákon o účtovníctve §16-§17 | COVERED | |
| Double-entry requirements | Zákon o účtovníctve §4 + Postupy účtovania | COVERED | |
| Rounding rules | Zákon o účtovníctve + DPH law | COVERED | NUMERIC(19,2), ROUND_HALF_EVEN |

**Ledger Core verdict: FULLY COVERED**

---

## Execution Rule Schema

| Requirement | Source | Status | Notes |
|-------------|--------|--------|-------|
| Formula patterns (tax_base, vat_amount, gross) | DPH law §22 + practical examples | COVERED | Standard formulas |
| Conflict resolution logic | Not in any law — engineering decision | N/A | We design this |
| Priority ordering | Not in any law — engineering decision | N/A | We design this |
| Validity dates pattern | All laws have effective dates | COVERED | |

**Execution Rule Schema verdict: COVERED** — conflict resolution and priority are our engineering decisions, not regulatory content.

---

## Summary

| Domain | Status | Gaps |
|--------|--------|------|
| Graph 1: Posting Rules | FULLY COVERED | None |
| Graph 2: DPH | MOSTLY COVERED | DPH rate annexes (include in extraction), triangulation examples (search during extraction) |
| Ledger Core | FULLY COVERED | None |
| Execution Rule Schema | COVERED | N/A (engineering decisions) |
| Chart of Accounts | FULLY COVERED | None |
| KV DPH Section Logic | FULLY COVERED | None |

**Overall: Ready to proceed with extraction.** The two minor gaps (DPH annexes, triangulation examples) are resolvable during the extraction phase — they don't require new source discovery.

---

## Action Items
1. When extracting DPH law, ensure Prílohy (Annexes) are included
2. Search for trojstranný obchod practical examples during practical_examples extraction
3. Verify KV DPH 2021 methodology PDF is still current (check for 2024/2025 updates)
