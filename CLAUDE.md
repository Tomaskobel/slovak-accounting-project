# Slovak AI Accountant Agent — Knowledge Graph Architecture

## Vision

Build an AI accountant agent grounded in a knowledge graph of Slovak accounting law. The agent reasons over structured regulatory knowledge (not hard-coded rules) to make accounting decisions. When regulations change, update the graph — not the code. The agent then also drives what the software needs to do.

**Core insight:** Accounting has two layers:
- **Invariant math** (double-entry, debits=credits, balance sheet equation) — hasn't changed since 1494
- **Regulatory rules** (DPH rates, booking rules, reporting requirements) — changes every year

Separate them. Hard-code the math. Put the rules in a knowledge graph. Let an AI agent reason over both.

---

## Architecture

```
┌─────────────────────────────────────────────┐
│  Layer 5: Software Architect Agent          │
│  AI accountant defines software specs       │
│  Generates update requests when rules change│
├─────────────────────────────────────────────┤
│  Layer 4: Regulation Update Loop            │
│  New laws → graph update → agent adapts     │
│  Core graph stable, only edges change       │
├─────────────────────────────────────────────┤
│  Layer 3: AI Accountant Agent               │
│  Reasons over graph + guardrails            │
│  Makes booking decisions, explains reasoning│
├─────────────────────────────────────────────┤
│  Layer 2: Guardrails + Formulas             │
│  Invariant: debits=credits, DPH math        │
│  Validation constraints, period controls    │
├─────────────────────────────────────────────┤
│  Layer 1: Knowledge Graph                   │
│  Slovak accounting law as structured data    │
│  Accounts, rules, rates, conditions, links  │
└─────────────────────────────────────────────┘
```

---

## Layer 1: Knowledge Graph

### What goes in
- **Act 431/2002 Coll.** (Zákon o účtovníctve) — full text, structured
- **Opatrenie MF SR 23054/2002-92** — chart of accounts framework
- **DPH law (222/2004 Z.z.)** — all VAT rules
- **Postupy účtovania** — detailed booking procedures for entrepreneurs
- **Finančná správa methodical guidelines** — KV DPH, Súhrnný výkaz instructions
- **E-invoicing regulation** — EN 16931, 2027 mandate rules

### Graph structure
**Entities (nodes):**
- `Account` — code, name, class, type (asset/liability/equity/revenue/expense)
- `Rule` — booking rule with conditions and actions
- `Rate` — DPH rate with effective dates and applicable categories
- `Report` — required report with structure and filing rules
- `FormSection` — KV DPH sections (A1, A2, B1...), Súhrnný výkaz fields
- `LegalSource` — reference to specific law paragraph

**Relationships (edges):**
- `Account --DEBITED_WHEN--> Rule` (when this rule triggers, debit this account)
- `Account --CREDITED_WHEN--> Rule` (when this rule triggers, credit this account)
- `Rule --APPLIES_WHEN--> Condition` (purchase of material, sale of service, etc.)
- `Rule --REQUIRES_RATE--> Rate` (which DPH rate applies)
- `Rule --PRODUCES_REPORT_DATA--> FormSection` (which report section gets this data)
- `Rate --EFFECTIVE_FROM--> Date` (rate validity)
- `Rule --SOURCE--> LegalSource` (traceability to law)

### Technology
- **Neo4j** or **Supabase + pgvector + JSONB** for graph storage
- Option A: Neo4j (native graph DB, Cypher queries, great for traversal)
- Option B: PostgreSQL with JSONB nodes + foreign keys for edges + pgvector for semantic search
- Recommendation: Start with PostgreSQL/Supabase (consistent with rest of stack), migrate to Neo4j if graph queries become bottleneck

### Ingestion pipeline
1. Collect all legal texts (available on slov-lex.sk, financnasprava.sk)
2. Use Claude to extract structured entities and relationships
3. Human accountant validates extracted graph
4. Version the graph (each regulatory change = new graph version with effective date)

---

## Layer 2: Guardrails + Formulas

These are **invariant** — they don't change with regulations:

### Mathematical constraints
- `SUM(debits) == SUM(credits)` for every journal entry (always)
- `Assets == Liabilities + Equity` (always)
- `Revenue - Expenses == Net Income` (always)
- All amounts: `NUMERIC(19,2)`, ROUND_HALF_EVEN

### Validation rules
- Cannot book to a closed fiscal period
- Cannot modify posted entries (immutability)
- Entry must have at least 2 lines
- Each line must have exactly one of debit/credit > 0
- Account must exist in tenant's chart of accounts

### DPH formulas
- `dph_amount = tax_base * rate / 100` (formula is invariant, rate comes from graph)
- `total = tax_base + dph_amount`
- Reverse calculation: `tax_base = total / (1 + rate/100)`

### Implementation
- Python module with pure functions
- No external dependencies, no database calls
- 100% unit testable
- These functions NEVER change (they're math, not law)

---

## Layer 3: AI Accountant Agent

### How it works
Given a business event (invoice received, bank transaction, etc.), the agent:

1. **Classifies the event** — what type of transaction is this?
2. **Queries the knowledge graph** — which rules apply to this event?
3. **Traverses relationships** — which accounts to debit/credit? Which DPH rate?
4. **Applies guardrails** — validates the proposed entry against Layer 2
5. **Returns a decision** with explanation and confidence score

### Example flow
```
Input: "Received invoice from Telekom for €120 including DPH"

Agent reasoning:
1. Event type: received invoice, services (telekomunikačné služby)
2. Graph lookup: Rule "purchase_of_services" →
   - Debit account 518 (Ostatné služby)
   - Debit account 343 (DPH - vstupná daň)
   - Credit account 321 (Dodávatelia)
3. DPH rate: Graph says telecom = 23% standard rate
   - Tax base: €120 / 1.23 = €97.56
   - DPH: €22.44
4. Guardrail check: 97.56 + 22.44 = 120.00 ✓, debits = credits ✓
5. KV section: B3 (received invoice ≤ €5000 with IČ DPH)

Output: {
  journal_entry: [
    {account: "518", debit: 97.56, credit: 0},
    {account: "343", debit: 22.44, credit: 0},
    {account: "321", debit: 0, credit: 120.00}
  ],
  dph: {rate: 23, base: 97.56, amount: 22.44},
  kv_section: "B3",
  confidence: 0.94,
  reasoning: "Classified as purchase of telecom services per §X of Postupy účtovania...",
  legal_source: "Opatrenie MF SR §47 ods. 1"
}
```

### Tech
- Claude API with structured output (tool use / JSON mode)
- System prompt includes: graph schema, available accounts, current rules
- RAG over knowledge graph: retrieve relevant rules before asking Claude to reason
- Langfuse tracing on every decision

---

## Layer 4: Regulation Update Loop

### How regulations change
- MF SR publishes new Opatrenia (amendments to booking procedures)
- Parliament changes DPH rates or thresholds
- Finančná správa updates XML schemas for filings

### Update workflow
1. **Detect change** — monitor slov-lex.sk, financnasprava.sk (can automate with web scraping + Claude)
2. **Extract delta** — Claude reads the new regulation, identifies what changed vs current graph
3. **Propose graph update** — new nodes/edges, modified relationships, updated rates with effective dates
4. **Human accountant validates** — this is the critical step, AI proposes but human approves
5. **Apply update** — new graph version with effective date
6. **Agent adapts immediately** — no code changes needed, agent reads updated graph

### What stays stable
- Account classes 0-9 structure (hasn't changed fundamentally in 20+ years)
- Double-entry math
- Journal entry structure
- Report formats (súvaha, VZaS) — structure is stable, content rules change

### What changes
- DPH rates (changed in 2025: 20% → 23%)
- Booking rules for specific transactions
- Report filing deadlines
- XML schema versions
- Thresholds (e.g., fixed asset threshold, DPH registration threshold)

---

## Layer 5: Software Architect Agent

### Concept
The AI accountant agent doesn't just make booking decisions — it also knows what the SOFTWARE needs to do. When regulations change:

1. Agent detects that new rule requires a new UI field (e.g., new KV section)
2. Agent generates a software spec: "Add section C3 to KV DPH form, triggered when..."
3. Developer (or Claude Code) implements the spec
4. Agent validates the implementation against the knowledge graph

### This is the long-term vision
- Phase 1: Knowledge graph + AI accountant making booking decisions
- Phase 2: Agent suggests software changes based on regulation changes
- Phase 3: Agent autonomously proposes PRs for regulatory updates

---

## Implementation Plan

### Phase 1: Knowledge Graph Foundation (Weeks 1-6)

**Goal:** Build the knowledge graph with core Slovak accounting rules. AI agent can correctly book 20 most common s.r.o. transaction types.

**Steps:**
1. **Week 1-2:** Set up project (FastAPI + Next.js + Supabase). Design graph schema in PostgreSQL (nodes table, edges table, or JSONB document model).
2. **Week 3-4:** Ingest core content:
   - Slovak chart of accounts (rámcová účtová osnova) → Account nodes
   - Top 50 booking rules from Postupy účtovania → Rule nodes + edges
   - Current DPH rates with conditions → Rate nodes
   - KV DPH section classification rules → FormSection nodes
3. **Week 5-6:** Build AI accountant agent that:
   - Takes a transaction description
   - Queries relevant graph nodes via semantic search
   - Returns journal entry suggestion with reasoning
   - Guardrail layer validates the entry

**Verification:** Feed 20 common transactions (material purchase, service purchase, issued invoice, bank payment, salary, depreciation, etc.) → compare agent's booking against what a certified accountant would do → target 90%+ match.

### Phase 2: Software Shell (Weeks 7-10)

**Goal:** Minimal accounting UI driven by the agent's decisions.

**Steps:**
1. Immutable ledger schema (journal_entries, entry_lines)
2. Agent-powered journal entry creation (user describes event, agent proposes entry)
3. Trial balance, basic súvaha, basic VZaS
4. Invoice upload → Claude Vision OCR → agent booking

### Phase 3: Regulation Loop (Weeks 11-14)

**Goal:** Agent can process a regulation update and adapt.

**Steps:**
1. Build graph update pipeline (new law text → Claude extracts changes → proposed graph diff)
2. Accountant review UI for approving graph changes
3. Version the graph with effective dates
4. Test: simulate a DPH rate change, verify agent adapts without code changes

### Phase 4: Full Product (Weeks 15-20+)

**Goal:** Self-serve SaaS with bank feeds, compliance exports, onboarding.

**Steps:**
1. Bank feed integration (Salt Edge)
2. KV DPH XML generation (agent knows which section from graph)
3. E-invoice UBL XML
4. Self-serve onboarding
5. Subscription billing

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Knowledge Graph | Supabase PostgreSQL + pgvector | Graph as tables with vector embeddings for semantic search. Consistent with rest of stack. |
| Guardrails | Pure Python module | Invariant math, no dependencies, 100% testable |
| AI Agent | Claude API (Sonnet) + Langfuse | Structured output for booking decisions. Full traceability. |
| Backend | FastAPI + Python 3.11+ | Decimal precision, AI-native |
| Frontend | Next.js 14 + shadcn/ui | Data tables, forms, dashboards |
| Database | Supabase PostgreSQL | RLS multi-tenancy, NUMERIC(19,2) |

---

## Key Risk: Graph Quality

The entire system's correctness depends on the knowledge graph being right. Mitigation:
- **Accountant validates every graph node/edge before production**
- **Graph is versioned** — can rollback if errors found
- **Agent always shows reasoning + legal source** — user/accountant can verify
- **Confidence threshold** — low confidence = human review
- **Start narrow** — 50 rules covering 80% of transactions, expand iteratively

---

## Why This Approach Wins

| Traditional approach | Knowledge graph approach |
|---------------------|------------------------|
| 400+ if/else rules in code | Rules encoded as graph relationships |
| DPH rate change = code change + deploy | DPH rate change = graph node update |
| New regulation = developer work | New regulation = graph update + accountant review |
| No explanation of decisions | Agent explains every decision with legal source |
| Rigid, brittle | Flexible, adaptive |
| 12+ months to cover all rules | Start with 50 rules covering 80% of cases, expand |

---

## First Step

Before writing any code: collect and organize the source material.

1. Download Postupy účtovania (MF SR 23054/2002-92 with all amendments)
2. Download DPH law (222/2004 Z.z. current consolidated version)
3. Download Finančná správa methodical guidelines for KV DPH
4. Find a Slovak accountant willing to validate the knowledge graph

The knowledge graph is only as good as the source material and its validation.
