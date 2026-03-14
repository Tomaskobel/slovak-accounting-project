# Slovak AI Accountant — Deterministic Platform with Declarative Regulatory Model

## Vision

Build a deterministic accounting platform driven by a versioned declarative regulatory model. The knowledge graph is the authoritative policy layer, the ledger engine is the deterministic execution layer, and the AI agent is a wizard, explainer, and controller for ambiguity, exceptions, and change management.

**Core insight:** Accounting has two layers:
- **Invariant math** (double-entry, debits=credits, balance sheet equation) — hasn't changed since 1494
- **Regulatory rules** (DPH rates, booking rules, reporting requirements) — changes every year

Separate them. Hard-code the math. Put the rules in a declarative model. Let a deterministic engine execute them. Let AI assist where ambiguity exists.

**Critical design principle:** AI is NOT the booking engine.
- Deterministic engine decides
- Knowledge graph defines policy
- AI agent assists, explains, and controls exceptions

---

## Architecture

```
┌─────────────────────────────────────────────┐
│  Layer 3: AI Interaction Layer              │
│  Intake wizard, Q&A, explanation            │
│  Exception handling, anomaly commentary     │
│  Regulation-diff assistance                 │
│  Software-spec suggestions                  │
├─────────────────────────────────────────────┤
│  Layer 2: Deterministic Execution Engine    │
│  Posting, tax calculation, validation       │
│  Filing section mapping, XML generation     │
│  Period control, reversals                  │
│  No LLM here.                              │
├─────────────────────────────────────────────┤
│  Layer 1: Declarative Regulatory Model      │
│  Transaction types, conditions              │
│  Account mappings, VAT treatments           │
│  Report mappings, legal references          │
│  Validity dates, exception paths            │
│  Required input fields                      │
└─────────────────────────────────────────────┘
```

**Normal operating path:**
```
document/event → deterministic classifier or configured mapping → graph rule resolution → deterministic posting
```

**LLM enters ONLY when:**
- Classification is uncertain
- Data is incomplete
- User asks a question
- Regulation must be interpreted before graph update
- Anomaly needs explanation

---

## Layer 1: Declarative Regulatory Model

### What the model contains
The graph is the **authoritative policy model**, not just RAG material for an LLM. It is the source that drives:
- Rule resolution
- Required fields
- VAT logic selection
- Report mapping
- Validation requirements
- Software change requirements

### Legal sources ingested
- **Act 431/2002 Coll.** (Zákon o účtovníctve) — full text, structured
- **Opatrenie MF SR 23054/2002-92** — chart of accounts framework
- **DPH law (222/2004 Z.z.)** — all VAT rules
- **Postupy účtovania** — detailed booking procedures for entrepreneurs
- **Finančná správa methodical guidelines** — KV DPH, Súhrnný výkaz instructions
- **E-invoicing regulation** — EN 16931, 2027 mandate rules

### Two distinct schemas

**1. Knowledge graph schema** — models the law. Entities, relationships, legal sources, validity dates. This is the regulatory content layer.

**2. Execution rule schema** — the contract the deterministic engine reads. Derived from the graph, but adds the engineering layer: formula evaluation, condition matching, priority ordering, conflict resolution, rounding policy.

These are separate design artifacts. The graph is the source of truth. Execution rules are derived from it.

### Knowledge graph schema

Stores regulatory knowledge as structured data:
- What the law says about each transaction type
- Which accounts are involved and why
- How concepts relate (account → rule → rate → report section → legal source)
- Validity dates and version history

The graph schema should emerge from the actual source material (Postupy účtovania, DPH law), not be designed in a vacuum.

### Execution rule schema (the critical engineering artifact)

The contract between the graph and the engine. Example:

```json
{
  "rule_id": "purchase_telecom_services_domestic",
  "transaction_type": "received_supplier_invoice",
  "conditions": {
    "category": "telecom_service",
    "supplier_country": "SK",
    "customer_is_vat_payer": true
  },
  "postings": [
    {"account": "518", "side": "debit", "amount": "tax_base"},
    {"account": "343", "side": "debit", "amount": "vat_amount"},
    {"account": "321", "side": "credit", "amount": "gross_amount"}
  ],
  "tax_treatment": "standard_input_vat",
  "report_mapping": ["kv_b3"],
  "required_inputs": [
    "invoice_date",
    "taxable_supply_date",
    "gross_amount",
    "vat_rate"
  ],
  "legal_source": ["source_ref_001"],
  "valid_from": "2025-01-01",
  "valid_to": null,
  "priority": 100
}
```

This schema must also handle (not yet designed):
- Formula language for amount expressions (how engine computes `tax_base` from `gross_amount` and `vat_rate`)
- Conditional branching (if amount > threshold → different account)
- Multi-line computed splits (salary = 10+ posting lines)
- Priority and conflict resolution when multiple rules match

**Key principle:** The graph stores regulatory knowledge. Execution rules are derived from it and add the engineering contract. The engine interprets execution rules. The UI reads required inputs from them. AI explains them using the graph. The graph does NOT directly generate arbitrary business logic code.

### Graph structure
**Entities (nodes):**
- `Account` — code, name, class, type (asset/liability/equity/revenue/expense)
- `Rule` — declarative booking rule with conditions, postings, and metadata
- `Rate` — DPH rate with effective dates and applicable categories
- `Report` — required report with structure and filing rules
- `FormSection` — KV DPH sections (A1, A2, B1...), Súhrnný výkaz fields
- `LegalSource` — reference to specific law paragraph

**Relationships (edges):**
- `Rule --POSTS_TO--> Account` (with side: debit/credit, amount expression)
- `Rule --APPLIES_WHEN--> Condition` (purchase of material, sale of service, etc.)
- `Rule --REQUIRES_RATE--> Rate` (which DPH rate applies)
- `Rule --MAPS_TO_REPORT--> FormSection` (which report section gets this data)
- `Rate --EFFECTIVE_FROM--> Date` (rate validity)
- `Rule --SOURCE--> LegalSource` (traceability to law)

### Where the graph adds real value

1. **Traceability** — connect rule → legal source → report section → effective date → exception → software requirement
2. **Versioned change management** — regulation changes update relationships and rule objects, not procedural code
3. **Dependency mapping** — ask: which rules depend on this VAT treatment? Which reports are affected by this law change? Which UI inputs become newly required? Which transaction types are impacted?

### Where the graph is NOT enough

A graph alone does not solve:
- Precise posting execution
- Ordering of calculations
- Deterministic evaluation priority
- Conflict resolution between rules
- Rounding policy
- Period locks
- Reversal semantics
- Tenant-specific chart-of-accounts variants

Those need the execution engine (Layer 2) and governance model.

### Technology
- **Supabase PostgreSQL + pgvector + JSONB** for graph storage
- Graph as tables with vector embeddings for semantic search
- Start with PostgreSQL (consistent with rest of stack), migrate to Neo4j if graph traversal becomes bottleneck
- Storage format matters less than the rule schema being well-defined

### Ingestion pipeline
1. Collect all legal texts (available on slov-lex.sk, financnasprava.sk)
2. Use Claude to extract structured rule objects
3. Human accountant validates every rule before production
4. Version the graph (each regulatory change = new graph version with effective date)

### Domain-decomposed knowledge graphs

The regulatory knowledge decomposes into four atomic domain graphs, each independently versioned:

| Graph | Domain | Scope | Update frequency | Primary legal source |
|-------|--------|-------|-----------------|---------------------|
| **Graph 1: Posting Rules** | Account mappings, transaction types, conditions, posting patterns | Which accounts, what side, what conditions | Rarely (~every few years) | Opatrenie MF SR 23054/2002-92, Postupy účtovania |
| **Graph 2: DPH (VAT)** | Rates, treatments, reverse charge, KV sections, exemptions, thresholds | Dense edge cases, many conditional paths | Often (rates changed 2025, thresholds shift) | Act 222/2004 Z.z. |
| **Graph 3: Reporting** | Súvaha structure, VZaS mapping, KV DPH XML schema, filing rules, deadlines | Report structure and compliance outputs | Medium (XML schemas update, new filing requirements) | Finančná správa methodical guidelines |
| **Graph 4: Payroll** | Social/health insurance rates, income tax brackets, deductions, caps, minimums | Very dense, very specific | Annually (rates, caps, minimums change every Jan 1) | Multiple acts + annual parameter decrees |

**Why four graphs, not one:**
- **Independent versioning** — DPH rate change (Graph 2) doesn't touch posting rules (Graph 1)
- **Focused validation** — accountant validates one domain at a time
- **Cleaner dependencies** — posting rules reference DPH treatments but don't contain them
- **Phased build** — Graph 1+2 first (covers ~80% of s.r.o. transactions), Graph 3 for compliance exports, Graph 4 deferred

**Cross-graph references:**
- Posting rule (Graph 1) → references DPH treatment (Graph 2) for tax calculation
- Posting rule (Graph 1) → maps to report section (Graph 3) for filing
- DPH treatment (Graph 2) → maps to KV DPH section (Graph 3) for XML generation

**Execution engine resolution path:**
```
transaction event → match posting rule (Graph 1)
                  → look up DPH rate/treatment (Graph 2)
                  → determine report section (Graph 3)
                  → generate complete journal entry
```

---

## Layer 2: Deterministic Execution Engine

This layer interprets the declarative model and performs all accounting operations. **No LLM here.**

### What it does
- **Posting** — reads rule, resolves accounts, creates journal entry lines
- **Tax calculation** — applies DPH formulas with rate from graph
- **Validation** — enforces invariant constraints
- **Filing section mapping** — determines KV DPH section, Súhrnný výkaz fields
- **XML/output generation** — KV DPH XML, e-invoice UBL
- **Period control** — fiscal period open/close management
- **Reversals** — storno entries following Slovak conventions

### Mathematical constraints (invariant)
- `SUM(debits) == SUM(credits)` for every journal entry (always)
- `Assets == Liabilities + Equity` (always)
- `Revenue - Expenses == Net Income` (always)
- All amounts: `NUMERIC(19,2)`, ROUND_HALF_EVEN

### Validation rules (invariant)
- Cannot book to a closed fiscal period
- Cannot modify posted entries (immutability)
- Entry must have at least 2 lines
- Each line must have exactly one of debit/credit > 0
- Account must exist in tenant's chart of accounts

### DPH formulas (invariant — rate comes from graph)
- `dph_amount = tax_base * rate / 100`
- `total = tax_base + dph_amount`
- Reverse calculation: `tax_base = total / (1 + rate/100)`

### Rule evaluation pipeline
1. Receive classified transaction event
2. Look up matching rules from graph (by transaction_type + conditions)
3. Resolve priority if multiple rules match (conflict resolution)
4. Calculate amounts using formulas + rate from graph
5. Generate posting lines per rule's `postings` array
6. Validate against invariant constraints
7. Determine report mappings
8. Return complete journal entry

### Implementation
- Python module with pure functions where possible
- No LLM calls, no external AI dependencies
- Deterministic: same input + same rules = same output
- 100% unit testable

### Example flow
```
Input: Classified event {type: "received_supplier_invoice", category: "telecom_service",
       supplier_country: "SK", gross_amount: 120.00, vat_rate: 23}

Engine:
1. Match rule: "purchase_telecom_services_domestic" (conditions match)
2. Calculate: tax_base = 120.00 / 1.23 = 97.56, vat = 22.44
3. Generate postings per rule:
   - 518 debit 97.56
   - 343 debit 22.44
   - 321 credit 120.00
4. Validate: 97.56 + 22.44 = 120.00 ✓, debits = credits ✓
5. Report mapping: kv_b3

Output: {
  journal_entry: [
    {account: "518", debit: 97.56, credit: 0},
    {account: "343", debit: 22.44, credit: 0},
    {account: "321", debit: 0, credit: 120.00}
  ],
  dph: {rate: 23, base: 97.56, amount: 22.44},
  kv_section: "B3",
  legal_source: "Opatrenie MF SR §47 ods. 1"
}
```

---

## Layer 3: AI Interaction Layer

This is where the AI belongs. It does NOT make booking decisions for standard flows.

### AI responsibilities
- **Intake wizard** — help user describe/classify a transaction
- **User Q&A** — answer accounting questions with graph-backed reasoning
- **Explanation** — explain why a posting was made, with legal source references
- **Exception handling** — route ambiguous cases to human accountant
- **Missing-data prompts** — identify what information is needed to complete a transaction
- **Anomaly commentary** — flag unusual patterns, explain concerns
- **Accountant support** — assist professional accountants with regulation interpretation
- **Regulation-diff assistance** — help extract changes from new law text, propose graph updates
- **Software-spec suggestions** — when new rules require new UI fields or logic, describe what needs to change

### When AI enters the flow
```
document/event → classification attempt
  ├─ confident classification → deterministic engine (no AI needed)
  └─ uncertain classification → AI assists:
       ├─ suggests possible classifications with reasoning
       ├─ asks user for clarification
       └─ routes to accountant if still ambiguous
```

### Tech
- Claude API with structured output (tool use / JSON mode)
- Langfuse tracing on every AI interaction
- AI reads from the graph but never writes directly — proposes changes for human approval

---

## Regulation Update Loop

### How regulations change
- MF SR publishes new Opatrenia (amendments to booking procedures)
- Parliament changes DPH rates or thresholds
- Finančná správa updates XML schemas for filings

### Update workflow
1. **Detect change** — monitor slov-lex.sk, financnasprava.sk
2. **AI extracts delta** — Claude reads new regulation, identifies what changed vs current graph
3. **Propose graph update** — new/modified rule objects with effective dates
4. **Human accountant validates** — critical step, AI proposes but human approves
5. **Apply update** — new graph version with effective date
6. **Engine adapts immediately** — no code changes needed, engine reads updated rules

### What stays stable
- Account classes 0-9 structure
- Double-entry math
- Journal entry structure
- Report formats (súvaha, VZaS) — structure is stable, content rules change

### What changes
- DPH rates (changed in 2025: 20% → 23%)
- Booking rules for specific transactions
- Report filing deadlines
- XML schema versions
- Thresholds (fixed asset threshold, DPH registration threshold)

---

## Implementation Plan

### Phase 1: Deterministic Core (Weeks 1-6)

**Goal:** Ledger core + rule schema + deterministic rule executor covering top transaction types.

**Do NOT start with "AI accountant agent." Start with the deterministic engine.**

**Steps:**
1. **Week 1-2:** Ledger core
   - Immutable ledger schema (journal_entries, entry_lines)
   - Double-entry validation (invariant math module)
   - Period control
   - Chart of accounts for s.r.o.

2. **Week 3-4:** Declarative rule schema + executor + Graph 1 & 2
   - Define rule JSON schema (the critical artifact)
   - Build Graph 1 (Posting Rules) — account mappings, transaction types, conditions
   - Build Graph 2 (DPH) — rates, treatments, reverse charge, KV sections
   - Build rule resolution engine (transaction type + conditions → matching rule)
   - Build posting generator (rule + amounts → journal entry)
   - Rule priority / conflict resolution
   - DPH calculation module (reads rates from Graph 2)

3. **Week 5-6:** Rule coverage + validation harness
   - Encode top 20-30 transaction types as declarative rules across Graph 1 + 2
   - Build test fixtures with accountant-approved expected outputs
   - Validate: deterministic engine produces correct entries for all fixtures
   - Target: 90%+ match against certified accountant decisions
   - Cross-graph resolution tested (posting rule → DPH treatment → report section)

**Verification:** Run all test fixtures, compare engine output against expected postings.

### Phase 2: Rule Infrastructure (Weeks 7-10)

**Goal:** Production-grade rule management before any rich UI.

**Steps:**
1. Rule authoring format (JSON schema + validation)
2. Graph versioning with effective dates (per-domain independent versioning)
3. Graph 3 (Reporting) — súvaha structure, VZaS mapping, KV DPH XML, filing rules
4. Rule simulation environment (what-if testing)
5. Accountant approval workflow for rule changes
6. Test fixtures for all transaction scenarios
7. Full cross-graph report mapping (Graph 1 → Graph 2 → Graph 3)

### Phase 3: AI Layer (Weeks 11-14)

**Goal:** AI assists with intake, explanation, and change management — on top of stable deterministic core.

**Steps:**
1. AI intake wizard (document → classify → route to engine)
2. Invoice upload → Claude Vision OCR → classification → deterministic posting
3. User Q&A with graph-backed reasoning
4. Explanation engine (why was this posted this way?)
5. Regulation-diff assistant (new law text → proposed graph updates)
6. Anomaly detection and commentary

### Phase 4: Full Product (Weeks 15-20+)

**Goal:** Self-serve SaaS with bank feeds, compliance exports, onboarding.

**Steps:**
1. Minimal accounting UI (trial balance, súvaha, VZaS)
2. Bank feed integration (Salt Edge)
3. KV DPH XML generation (engine knows which section from graph)
4. E-invoice UBL XML
5. Self-serve onboarding
6. Subscription billing

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Regulatory Model | Supabase PostgreSQL + pgvector + JSONB | Declarative rules as structured data. Vector embeddings for semantic search. |
| Execution Engine | Pure Python module | Deterministic, no LLM dependencies, 100% testable |
| AI Layer | Claude API (Sonnet) + Langfuse | Structured output for intake/explanation. Full traceability. |
| Backend | FastAPI + Python 3.11+ | Decimal precision, AI-native |
| Frontend | Next.js 14 + shadcn/ui | Data tables, forms, dashboards |
| Database | Supabase PostgreSQL | RLS multi-tenancy, NUMERIC(19,2) |

---

## Key Risks

### Primary risk: Rule modeling complexity and governance discipline

With deterministic posting, the risk is no longer "LLM hallucination." It becomes:
- Incomplete rule coverage
- Conflicting rules
- Weak priority ordering
- Bad graph updates
- Poor accountant validation workflow
- Edge-case explosion

**The product challenge shifts from "can AI do accounting?" to "can we maintain a production-grade regulatory rule system?"**

That is a much better problem to have.

### Mitigation
- **Accountant validates every rule before production**
- **Graph is versioned** — can rollback if errors found
- **Rule simulation environment** — test changes before applying
- **Start narrow** — 30 rules covering 80% of transactions, expand iteratively
- **Conflict resolution is explicit** — priority ordering defined, not implicit

---

## Why This Approach Wins

| Traditional approach | Deterministic + declarative approach |
|---------------------|--------------------------------------|
| 400+ if/else rules in code | Rules encoded as declarative objects in graph |
| DPH rate change = code change + deploy | DPH rate change = rule object update |
| New regulation = developer work | New regulation = rule update + accountant review |
| No explanation of decisions | AI explains every decision with legal source |
| LLM in critical path = unpredictable | Deterministic engine = same input, same output |
| Rigid, brittle | Flexible, adaptive, auditable |

---

## Current State

- Architecture plan finalized (2026-03-12)
- **Stage 1 scope defined (2026-03-13):** Posting Rules (Graph 1) + full DPH (Graph 2) + deterministic engine. See `docs/stage_1_scope.md`
- Regulatory sources inventory complete — see `docs/regulatory_sources.md`
- **Stage 1 source extraction complete (2026-03-13):**
  - Gap analysis: `docs/analysis/stage_1_gap_analysis.md` — Graph 1 fully covered, Graph 2 mostly covered (2 minor gaps)
  - 10 source files in `docs/sources/` (5 pairs of .md + .json, 428K total):
    - `chart_of_accounts` — 236 prescribed accounts across 10 classes (0-9)
    - `postupy_uctovania` — Opatrenie MF SR 23054/2002-92, all booking rules §1-§88
    - `dph_law` — Act 222/2004 Z.z., all VAT rules with 2025 rates (23%/19%/5%)
    - `kv_dph_guidelines` — KV DPH section classification (A1/A2/B1/B2/B3/C1/C2/D1/D2)
    - `practical_examples` — 42 worked examples as future test fixtures
  - **Supabase:** project `anhowyrefeyxkaouwmjh` (slovak-accounting, eu-central-1), `regulatory_sections` table with pgvector (512 rows)
- **Engine pojmy (terms) table complete (2026-03-14):**
  - `engine/pojmy.json` — 36 terms: 9 DPH calculations, 4 rates, 14 thresholds, 3 invariants, 3 rounding rules, 1 reverse charge, 2 KV DPH thresholds
  - `engine/pojmy.py` — Python module with Decimal precision, ROUND_HALF_UP, typed functions using exact Slovak legal terminology
  - `engine/test_pojmy.py` — 71 tests (all passing), fixtures from practical_examples
  - All terms verified against source law text (33 exact ✓, 3 standard accounting ⚠)
  - **Re-verified against verbatim Supabase text (2026-03-14):** 31/36 confirmed exact, 5 fixes applied:
    - `prah_zjednodusena_faktura`: §73 → §74 ods. 3 (§73 = invoice timing, not simplified invoices)
    - `prah_investicny_majetok`: §54d → §54 ods. 2 písm. a) (§54d = tax adjustment, not threshold definition)
    - `prah_danova_zaruka_min/max`: §4c doesn't exist in 222/2004 effective 2025-04-01, likely in Daňový poriadok 563/2009 — marked `overene: false`
    - `prah_zasielkovy_predaj`: 10,000 EUR not found in §14 text, may be EU directive — marked `overene: false`
  - Terminology: Slovak-first (základ dane, daň, koeficient, samozdanenie — not English translations)
- **Rule patterns extracted (2026-03-14):**
  - `docs/analysis/rule_patterns_top10.md` — 10 most common s.r.o. transaction types fully reverse-engineered
  - Conditions, posting lines, DPH treatment, KV DPH sections, legal sources, variants, edge cases
- **Execution rule schema + engine complete (2026-03-14):**
  - `engine/schema.py` — Dataclass schema: Pravidlo, Podmienky, RiadokZapisu + enums (SmerTransakcie, TypPlnenia, DphTreatment, KvDphSekcia, etc.)
  - `engine/pravidla.py` — 24 declarative rules (20 transaction types + variants/steps) encoded as Pravidlo objects
  - `engine/motor.py` — Deterministic execution pipeline: najdi_zhody → vyber_pravidlo → generuj_zapis → validuj_zapis → zauctuj
  - `engine/test_motor.py` — 25 pipeline tests (all passing)
  - Conflict resolution: priority + specificity (number of non-None conditions)
  - Multi-step support: krok/celkovo_krokov for DHM purchase (2 steps), preddavok (3 steps)
  - **Total: 95 tests, all passing in 0.08s**
- No accountant available — using practical examples + law text + confidence flags as interim validation
- **Verbatim law text scraper complete (2026-03-14):**
  - `scraper/` module — fetches raw HTML from static.slov-lex.sk, parses into hierarchical sections, stores in Supabase
  - Supabase tables: `law_documents` (raw HTML per law version) + `law_sections` (hierarchical parsed sections)
  - **222/2004 (DPH law):** 2,243 sections (170 §, 1000 odsek, 822 písmeno, 85 bod, 10 príloh, 135 poznámok), 1.9 MB HTML, effective 2025-04-01
  - **431/2002 (Účtovníctvo):** 1,365 sections (101 §, 521 odsek, 478 písmeno, 105 bod, 1 príloha, 158 poznámok), 1.2 MB HTML, effective 2026-01-01
  - Verbatim text verified — §27 (DPH rates) shows exact "23 %", "19 %", "5 %" from law
  - CLI: `python3 -m scraper pipeline 222/2004 --date 20250401` (fetch → parse → verify)
  - **Not yet scraped (PDF only):** ~~Postupy účtovania (Opatrenie MF SR), KV DPH guidelines~~ — NOW DONE (see below)
  - Project `.env` overrides global SUPABASE_URL/KEY to point to `anhowyrefeyxkaouwmjh` project
- **PDF scraper complete (2026-03-14):**
  - `scraper/pdf_parser.py` — pdfplumber parser for Postupy účtovania + KV DPH guidelines
  - **23054/2002-92 (Postupy účtovania):** 1,212 sections (117 §, 632 odsek, 463 písmeno), 318K chars, effective 2024-03-15
  - **KV-DPH (Kontrolný výkaz):** 10 sections (9 KV sections A.1-D.2 + intro), 84K chars
  - CLI: `python3 -m scraper parse-pdf <file> --type postupy --date YYYYMMDD` or `fetch-pdf <url> --type kv-dph --date YYYYMMDD`
  - Source PDFs from financnasprava.sk (downloaded to `scraper/pdfs/`, gitignored)
  - **Supabase total: 4 documents, 4,830 sections of verbatim regulatory text**

## Next Steps

### ~~Step 1: Re-verify engine terms against verbatim law text~~ ✅ DONE
31/36 terms confirmed, 5 fixes applied to pojmy.json. See Current State for details.

### ~~Step 2: Add PDF scraper for Postupy účtovania + KV DPH guidelines~~ ✅ DONE
`scraper/pdf_parser.py` — pdfplumber-based parser. Postupy účtovania: 1,212 sections (117 §, 632 odsek, 463 písmeno, 318K chars). KV DPH guidelines: 10 sections (9 KV sections + intro, 84K chars). Both stored in Supabase.

### Step 3: Find a Slovak accountant willing to validate
Not blocking development. Using practical examples as ground truth. Accountant validates when found.

### ~~Step 4: Expand rule coverage~~ ✅ DONE (2026-03-14)
10 new transaction types added (24 total rules, 95 tests passing):
- Nákup materiálu od neplatiteľa DPH (BEZ_DPH)
- Dovoz z tretej krajiny s clom (VSTUPNA_DAN, B2)
- Predaj do EÚ — oslobodenie (OSLOBODENIE_S_ODPOCTOM, A1)
- Vývoz mimo EÚ (OSLOBODENIE_S_ODPOCTOM, no KV)
- Tuzemský prenos — stavebné práce (PRENOS, A2) — `tuzemsky_prenos` condition added
- Tuzemský prenos — elektronika >5000 EUR (PRENOS, A2)
- Faktúra za energie (VSTUPNA_DAN, B2, účet 502)
- Bankové poplatky (OSLOBODENIE_BEZ_ODPOCTU, no KV, účet 568)
- Hotovostný predaj cez e-kasu (VYSTUPNA_DAN, D1)
- Cestovné náhrady (BEZ_DPH, účet 512/333)
Schema extended: `tuzemsky_prenos` condition on Podmienky, `celkova_suma` on Transakcia.

### ~~Step 5: Graph storage in Supabase~~ ✅ DONE (2026-03-14)
`graph_pravidla` table in Supabase — 24 rules synced (version 1).
- JSONB columns for `podmienky` (conditions) and `riadky` (posting lines)
- GIN index on podmienky for condition queries
- Bi-temporal versioning: `pravidlo_id` + `graph_version` unique constraint
- `engine/sync_pravidla.py` — sync script with `--check` dry-run mode
- RLS enabled with public read, anon write policies

### ~~Step 6: AI classification layer~~ ✅ DONE (2026-03-14)
`engine/klasifikator.py` — Claude-powered transaction classifier (Layer 3).
- `klasifikuj(popis)` → Klasifikacia with confidence score, structured fields, rule match
- `klasifikuj_a_zauctuj(popis)` → classification + journal entry in one call
- Three confidence levels: uspesna (≥0.8), neista (0.5-0.8), neznama (<0.5)
- Tool use for structured output, system prompt with Slovak regulatory context
- `engine/__main__.py` — CLI: `python3 -m engine classify --book "description"`
- Uses claude-sonnet-4-20250514, ANTHROPIC_API_KEY from ~/.zshrc
