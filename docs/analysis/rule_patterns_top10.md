---
title: "Rule Patterns — Top 10 s.r.o. Transaction Types"
date: "2026-03-14"
scope: "Stage 1: Posting Rules (Graph 1) + DPH (Graph 2)"
---

# Rule Patterns — Top 10 s.r.o. Transaction Types

Extracted from source material (Postupy účtovania, DPH law, practical examples).
Every rule traces to § reference. No invented terminology.

## Summary

| # | Typ transakcie | Kategória | Účet | DPH | Sadzba | KV | Právny zdroj |
|---|----------------|-----------|------|-----|--------|----|----|
| 1 | Nákup materiálu (tuzemsko) | Náklad | 112/501 | Vstupná | 23% | B.2 | §30-32, DPH §49 |
| 2 | Nákup služieb (tuzemsko) | Náklad | 518 | Vstupná | 23% | B.2 | §517-518, DPH §49 |
| 3 | Predaj tovaru (tuzemsko) | Výnos | 604 | Výstupná | 23% | A.1/D.2 | §35-37, DPH §19 |
| 4 | Predaj služieb (tuzemsko) | Výnos | 602 | Výstupná | 23% | A.1/D.2 | §602, DPH §27 |
| 5 | Nákup z EÚ (nadobudnutie) | Náklad | 112 | Samozdanenie | 23% | B.1 | DPH §11, §20, §69 |
| 6 | Prijatie služby z EÚ | Náklad | 518 | Prenos | 23% | B.1 | DPH §15, §69 |
| 7 | Nákup DHM | Majetok | 042→022 | Vstupná | 23% | B.2 | §32-36, DPH §49 |
| 8 | Dobropis prijatý | Oprava | 501/321 | Zníženie vstupu | varies | C.2 | DPH §25, §53 |
| 9 | Dobropis vydaný | Oprava | 604/311 | Zníženie výstupu | varies | C.1 | DPH §25, §53 |
| 10 | Preddavok s DPH | Záväzok | 314→321 | Preddavková | 23% | B.2 | DPH §19 ods. 2 |

## Key Findings for Schema Design

1. **Conditions that differentiate rules:**
   - `krajina_dodavatela` (SK / EÚ / tretia krajina)
   - `platitel_dph` (buyer/seller VAT payer status)
   - `typ_plnenia` (tovar / služba / majetok)
   - `smer` (nákup / predaj)
   - `forma_uhrady` (faktúra / hotovosť / preddavok)

2. **DPH treatment types (enum):**
   - `vstupna_dan` — standard input deduction
   - `vystupna_dan` — standard output liability
   - `samozdanenie` — self-assessment (net effect = 0)
   - `prenos_danovej_povinnosti` — domestic reverse charge
   - `oslobodenie_s_odpoctom` — exempt with deduction right
   - `oslobodenie_bez_odpoctu` — exempt without deduction
   - `oprava_vstupnej` — credit note reducing input
   - `oprava_vystupnej` — credit note reducing output

3. **Multi-step transactions:** Preddavok requires 3 sequential steps. Engine must support ordered posting sequences.

4. **Variant resolution:** Same transaction type (e.g., nákup materiálu) has variants by inventory method (A vs B), supplier country, VAT status. Priority: most specific match wins.

5. **KV DPH section is deterministic:** Derived from conditions (smer + typ_plnenia + DPH_treatment). No ambiguity.
