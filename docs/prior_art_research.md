# Prior Art Research: Declarative Rule Engines in Accounting, Tax & Compliance

**Date:** 2026-03-12
**Purpose:** Understand how existing systems solve the same problem — separating regulatory knowledge from execution logic.

---

## 1. Rule Engine Architectures (Accounting/Tax/ERP)

### Drools / BRMS (Rete Algorithm)
- **What:** Open-source Business Rules Management System (Apache KIE), forward-chaining pattern matching
- **Rule format:** DRL language with `when`/`then` blocks. Also supports DMN decision tables
- **Engine:** Rete DAG — alpha network (single-condition tests) + beta network (join conditions). Match-resolve-act cycle
- **Accounting use:** Ships with CashFlow/Accounting example. Academic paper (PMC) demonstrates financial-to-management accounting transformation
- **Our takeaway:** Right conceptual model (conditions → actions, pattern matching against facts), but Java-based, operationally heavy, overkill for ~200-500 rules. Don't use Drools itself, adopt the pattern
- **Sources:** [Drools Docs](https://docs.drools.org/6.2.0.Final/drools-docs/html/ch20.html), [PMC Paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC9045965/)

### DMN (Decision Model and Notation)
- **What:** OMG standard for modeling business decisions
- **Rule format:** Decision tables (Excel-like grids: input columns → output columns) + FEEL expression language + decision requirement diagrams showing dependencies
- **Our takeaway:** Decision table format maps well to accounting rules — input = transaction type + country + entity type, output = debit account + credit account + tax rate. Accountant-readable AND machine-executable. Consider as internal format for booking rules
- **Source:** [OMG DMN Standard](https://www.omg.org/dmn/)

### SAP Accounting Rules Engine (ARE)
- **What:** SAP's subledger-to-GL posting engine, built on PaPM Universal Model
- **Rule format:** Configuration workflows define: multiple ledgers, chart of accounts, account derivation rules, posting rules. Declarative via config UI
- **Our takeaway:** Confirms the two-layer pattern: invariant posting logic in code, "which accounts for which event" in configuration. SAP has done this since R/3 in the 1990s. Our graph is a more flexible version of SAP's account determination config
- **Sources:** [SAP ARE Blog](https://community.sap.com/t5/financial-management-blogs-by-sap/introducing-the-accounting-rules-engine-are-powered-by-sap-papm-universal/ba-p/13769111), [SAP Posting Rules](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/3cb1182b4a184bdd93f8d62e3f1f0741/1b16bc98571c435792da966b4e3692b5.html)

---

## 2. Knowledge Graphs in Regulatory/Compliance Domains

### Intuit TurboTax Knowledge Graph (MOST RELEVANT)
- **What:** Intuit replaced hard-coded tax logic with a Tax Knowledge Graph. KDD 2020 workshop paper
- **Rule format:** Tax forms, line items, calculations, and conditional rules as graph nodes and edges. Full U.S. + Canadian income tax compliance logic encoded in graph. Per-user instantiation combines structural graph with user data
- **Engine:** Tax Knowledge Engine traverses instantiated graph to: calculate tax, reason about missing information, explain results by walking graph backward
- **Our takeaway:** **Direct validation of our architecture.** Intuit did exactly what we propose — moved regulatory rules from code to knowledge graph. They handle ~70,000+ rules across U.S. + Canada; we handle ~200-500 Slovak rules. Pattern is identical: graph = regulatory knowledge, engine = graph traversal + calculation
- **Sources:** [arXiv Paper](https://arxiv.org/abs/2009.06103), [Stanford CS520 Presentation](https://web.stanford.edu/class/cs520/2020/abstracts/yu.html)

### Oxford Semantic / RDFox
- **What:** Knowledge graph + reasoning engine (Oxford spinout). In-memory RDF with Datalog-based rules
- **How:** Rules as Datalog clauses that derive new facts from existing graph data. Incremental application as data changes. Used in financial services for compliance checking
- **Our takeaway:** Datalog approach (rules that infer new facts) maps well: "IF purchase of services AND supplier is EU AND VAT registered THEN apply reverse charge"
- **Source:** [Oxford Semantic](https://www.oxfordsemantic.tech/)

### Neo4j Temporal Versioning
- **What:** Bi-temporal versioning pattern for regulatory graphs
- **How:** Two timestamps: business date (when rule should have been effective) + process date (when recorded). Nodes/edges carry `valid_from`/`valid_to`. Historical states reconstructable for any point in time
- **Our takeaway:** Exactly how we need to version DPH rate changes. When Slovakia changed DPH 20% → 23% on 2025-01-01, graph needs both: old rate (valid_to = 2024-12-31) and new rate (valid_from = 2025-01-01)
- **Source:** [Neo4j Temporal Blog](https://medium.com/neo4j/keeping-track-of-graph-changes-using-temporal-versioning-3b0f854536fa)

### AgentiveAIQ — Dual Knowledge Architecture
- **What:** General-purpose AI agent builder (not accounting-specific). Uses LangGraph/LangChain
- **Knowledge architecture:** Dual system — (1) pgvector for semantic search across chunked documents, (2) Neo4j + Graphiti for entity extraction and relationship mapping with temporal awareness
- **Graphiti (by Zep):** Open-source library that builds temporal knowledge graphs — entities and relationships with timestamps. Incremental updates as new data arrives
- **Our takeaway:** Not architecturally relevant (LLM-first, no deterministic engine), BUT the dual knowledge pattern is useful: **graph for structured rule relationships + vector for semantic similarity search**. Maps to our design: graph stores rules/relationships (Layer 1), pgvector enables AI layer to find relevant legal sources when answering questions (Layer 3). Graphiti's temporal graph pattern aligns with our bi-temporal versioning need
- **Source:** [AgentiveAIQ](https://agentiveaiq.com/how-it-works), [Graphiti](https://github.com/getzep/graphiti)

---

## 3. Declarative Accounting Rule Systems (Open Source)

### Odoo Fiscal Positions
- **What:** Declarative tax and account mapping system, 70+ country localizations
- **Rule format:** `FiscalPosition` = named config with two mapping tables: (1) tax mapping ("replace tax X with tax Y"), (2) account mapping ("replace account X with account Y"). Auto-apply based on partner VAT status + country
- **Engine:** On invoice creation, check partner's fiscal position → for each line, transform default tax/account via mappings
- **Our takeaway:** Simple but effective pattern: defaults on product, context-specific overrides via fiscal positions. Limitation: only handles tax/account substitution, not full posting logic (debit/credit sides, KV DPH classification)
- **Source:** [Odoo Fiscal Positions Docs](https://www.odoo.com/documentation/19.0/applications/finance/accounting/taxes/fiscal_positions.html)

### ERPNext / Frappe
- **What:** Open-source ERP (Python) with accounting module
- **Rule format:** Chart of accounts as JSON tree per country. Tax via "Sales/Purchase Tax Templates." Journal Entry Templates predefine account/debit/credit patterns
- **Our takeaway:** Country-specific chart of accounts as JSON = good graph bootstrap precedent. Journal Entry Templates ≈ simplified booking rules, but static (no conditional logic)
- **Sources:** [ERPNext CoA](https://github.com/frappe/erpnext/wiki/Country-wise-Chart-of-Accounts), [Journal Entry Templates](https://docs.frappe.io/erpnext/user/manual/en/journal-entry-template)

---

## 4. Tax Calculation Engines

### Avalara AvaTax
- **What:** Cloud tax compliance, 12,000+ jurisdictions
- **Rule format:** Three abstractions: (1) TaxCodes — product taxability per jurisdiction, (2) Jurisdiction determination via geo-location, (3) Tax Content API returns jurisdiction-specific rules/rates
- **Engine:** API-first — send transaction with line items + tax codes + addresses → returns calculated tax by jurisdiction
- **Our takeaway:** Separates three concerns: (1) product classification (what), (2) jurisdiction determination (where), (3) rule application (what rate/exemption). Maps to our model: (1) transaction classification, (2) entity context (Slovak s.r.o., DPH registered), (3) rule lookup (accounts, rate, KV section)
- **Sources:** [Avalara Taxability](https://www.avalara.com/partner/en/api/calculation/sales-tax/guide/product-taxability/taxcodes-and-exemptions.html), [Tax Content API](https://www.avalara.com/partner/en/api/calculation/sales-tax/guide/calculating-tax-offline/tax-content-api.html)

### Vertex
- **What:** Enterprise tax determination, SAP/Oracle integration
- **Rule format:** Hierarchical product category trees (General → Services → Computer Software → Music Delivered Electronically). GeoCodes (9-digit jurisdiction codes). Tax Decision Maker compares category codes against jurisdiction taxability
- **Engine:** Per line: product category + GeoCode → TDM lookup → specific rule exists? Apply. Else? Apply standard jurisdiction rate. Fallback pattern
- **Our takeaway:** **Hierarchical classification with fallback** is directly applicable. Our rules have same structure: specific ("purchase telecom from EU") → category ("purchase services from EU") → default ("purchase from EU")
- **Source:** [Vertex + Oracle](https://docs.oracle.com/cd/E59116_01/doc.94/e58755/ap_vertex_tax_system.htm)

---

## 5. Domain-Specific Languages for Bookkeeping

### hledger CSV Rules
- **What:** Mature rule-based CSV import system for plain-text accounting
- **Rule format:** `.csv.rules` files with regex pattern matching:
  ```
  if PAYPAL.*NETFLIX
    account2  expenses:entertainment:streaming
  if SALARY|MZDA
    account2  income:salary
  ```
- **Our takeaway:** Simplest working example of declarative accounting rules. Our system is a more sophisticated version: semantic classification instead of regex, full journal entries with DPH instead of simple account assignment
- **Source:** [hledger Manual](https://hledger.org/manual.html)

### Beancount + smart_importer
- **What:** Python plain-text accounting with ML classification plugin
- **Rule format:** smart_importer uses decision trees trained on existing entries to predict accounts. beanhub-import uses declarative YAML rules for transaction import
- **Our takeaway:** Two approaches working together: (1) explicit rules for known patterns, (2) ML for the rest. Exactly our strategy: deterministic engine handles 90% of transactions, AI handles ambiguous classification
- **Sources:** [smart_importer](https://github.com/beancount/smart_importer), [LLM Bookkeeping](https://beancount.io/docs/Solutions/using-llms-to-automate-and-enhance-bookkeeping-with-beancount)

---

## 6. Graph-Based Regulatory Change Management

### AscentAI (RegTech)
- **What:** Regulatory Lifecycle Management platform for financial institutions
- **Rule format:** AI extracts individual obligations from regulatory text as versioned data objects. Each obligation = atomic unit with metadata: source, effective date, jurisdictions, mapped controls. Side-by-side version comparisons
- **Change pipeline:** Monitor regulatory sources → NLP extracts obligations → diff against current inventory → impact analysis → human review → update
- **Our takeaway:** **Closest commercial analog to our Regulation Update Loop.** Their obligation extraction = our "Claude reads new Opatrenie and extracts graph changes." Key pattern: regulations → atomic objects → versioned inventory → mapped to controls
- **Source:** [AscentAI](https://www.ascentregtech.com/rlm-platform/)

### Corlytics
- **What:** Regulatory intelligence platform (built FCA's intelligent handbook, 3000+ metadata tags)
- **Model:** Regulation → Obligations → Controls → Risks, with version tracking at each level. Regulatory Taxonomy categorizes notices
- **Our takeaway:** Validates our graph schema design. Their hierarchy maps to ours: Legal Source → Rules → Accounts/Rates → Reports
- **Source:** [Corlytics](https://www.corlytics.com/solutions/regulatory-rules-mapping/)

### Be Informed
- **What:** RegTech platform (20+ years, Netherlands). Transforms regulations into executable decision models
- **How:** Model-driven development — regulations translated to machine-readable decision models, not code. Update model, not application. Full traceability to legal source. Used by tax authorities
- **Our takeaway:** Most mature example of "regulations as data, not code." 20+ years in production at tax authority scale. Confirms our approach is proven
- **Source:** [Be Informed](https://www.beinformed.com/)

---

## 7. AI-Native Accounting Products (2025-2026 Wave)

### Digits — Autonomous General Ledger (WATCH CLOSELY)
- **What:** AI-native GL that replaces QuickBooks. $825B in training data, dozens of specialized models
- **Architecture:** Orchestrates multiple specialized models (NOT generic LLMs). Custom models outperform GPT-4o by 54% on accounting tasks. Bookkeeping Agent categorizes continuously, flags low-confidence entries to human inbox
- **Key pattern:** AI does classification + categorization, but maintains tight human feedback loops with US-based accountants. 97.8% accuracy (vs 79.1% from outsourced humans). Automates 90%+ of SMB bookkeeping
- **Our takeaway:** Validates our confidence-based routing: deterministic for high-confidence, human review for low-confidence. But Digits is LLM-first (AI makes the booking decision), we are rule-first (deterministic engine makes the decision). Different philosophy — we bet on explainability and regulatory traceability over raw ML accuracy
- **Source:** [Digits AGL Launch](https://www.globenewswire.com/news-release/2025/03/10/3039814/0/en/AI-Startup-Digits-Takes-on-QuickBooks-with-the-World-s-First-Autonomous-General-Ledger-for-Accounting-Xero-Co-founder-Craig-Walker-Joins-Digits.html)

### Sphere — TRAM Tax Compliance (RELEVANT PATTERN)
- **What:** AI-native global sales tax / VAT compliance. $21M Series A from a16z. 100+ jurisdictions
- **Architecture:** Proprietary TRAM (Tax Review and Assessment Model) — fine-tuned LLM trained to index and understand tax law. Determines taxability across jurisdictions with backing citations
- **Critical design:** Human teams review and approve every TRAM output before it hits the live tax engine. "That part of the system has no AI so there is zero chance of hallucinations"
- **Our takeaway:** **Exactly our two-layer pattern.** AI analyzes and proposes (TRAM), deterministic engine executes (live tax engine), human validates in between. Sphere proves this hybrid works at scale with a16z validation. Their TRAM = our Layer 3 + knowledge graph. Their live tax engine = our Layer 2
- **Sources:** [TechCrunch](https://techcrunch.com/2025/11/18/a16z-leads-21m-series-a-into-tax-compliance-platform-sphere/), [Sphere](https://www.getsphere.com/)

### Tellen.ai — Audit Automation with Traceability
- **What:** AI audit automation platform. Deploys within client's own cloud (Azure/AWS/GCP). SOC 2 Type II certified
- **Architecture:** AI agents automate audit fieldwork — read from client systems → execute audit procedures → write workpapers. Uses firm's own templates for output standardization
- **Key pattern:** 100% traceability — every AI decision, consideration, and rationale is logged. All outputs backed by verifiable sources. ISQM 1/SQMS 1 compliance
- **Our takeaway:** Different domain (audit vs. posting), but the **traceability principle** is directly relevant — every booking decision should trace back to a rule + legal source. Template-driven output also maps to how our engine uses declarative rules to produce standard journal entries
- **Source:** [Tellen.ai](https://www.tellen.ai/)

### TigerGraph — Graph Analytics Platform
- **What:** High-performance graph database with hybrid graph+vector search. GSQL query language + OpenCypher support
- **Architecture:** Native parallel graph processing. In-memory graph computation. Supports hybrid Graph+Vector search for combining structured relationships with semantic similarity
- **Our takeaway:** Alternative to Neo4j if graph traversal becomes a performance bottleneck. Hybrid graph+vector search natively combines what we'd otherwise need PostgreSQL (graph tables) + pgvector (semantic search) to achieve. Monitor as potential future migration target, but PostgreSQL-first is correct for our scale
- **Source:** [TigerGraph Docs](https://docs.tigergraph.com/home/)

---

## 8. Compliance Graph Patterns

### Compliance Graph Architecture (PuppyGraph)
- **What:** Formal model for how compliance data should be structured as a graph
- **Structure:** Two linked chains: (1) Intent chain: Requirement → Policy → Control, (2) Implementation chain: Control → Assets/Identities → Evidence
- **Temporal:** Each node and edge includes provenance and timestamps. Point-in-time compliance views without rebuilding reports
- **Rule enforcement:** Graph pattern matching queries detect violations (e.g., find all roles with privileged access missing MFA control)
- **Our takeaway:** Our graph has a parallel structure: Legal Source → Rule → Account/Rate → Report Section → Filing. The intent/implementation split maps to: graph defines what should happen (intent), engine executes what actually happens (implementation), audit trail proves they match
- **Source:** [PuppyGraph Compliance Graph](https://www.puppygraph.com/blog/compliance-graph)

### RAGulating Compliance — Multi-Agent KG for Regulatory QA
- **What:** Academic paper (2025). Ontology-free knowledge graph from regulatory documents + RAG + multi-agent system
- **Architecture:** Schema-light — no predefined ontology, schemas emerge naturally from data. Subject-Predicate-Object triplets extracted from regulatory text. Each triplet maintains provenance (reference to original source)
- **Pipeline:** 5 specialized agents: Document Ingestion → Extraction (LLM detects SPO triplets) → Normalization → Indexing (vector store) → Retrieval & Generation
- **Key result:** With triplets, average shortest path between related regulatory sections decreased from 2.0 to 1.3 — faster navigation through regulatory interconnections
- **Our takeaway:** Schema-light approach is interesting for initial graph construction — let the schema emerge from Postupy účtovania rather than pre-designing it. But for execution rules, we DO need a strict schema. Use schema-light for knowledge ingestion, strict schema for the execution contract
- **Source:** [arXiv 2508.09893](https://arxiv.org/html/2508.09893v1)

---

## 9. Programmable Ledger Infrastructure

### GoDBLedger — Programmable Double-Entry Server
- **What:** Open-source accounting system in Go. GRPC endpoints + SQL backends (SQLite, MySQL)
- **Architecture:** Central server for financial transactions. Apps transmit transactions via API, server records them in user-controlled database. Clear schema for external analysis
- **Design philosophy:** Make double-entry bookkeeping programmable. API-first, database-first. Influenced by Go-Ethereum (Geth) architecture. Schema influenced by GnuCash
- **Our takeaway:** Closest open-source analog to our Layer 2 concept — a programmable ledger server that receives structured transactions and records them with double-entry validation. We add: declarative rule resolution before posting, DPH calculation, KV DPH section mapping. GoDBLedger is the bare ledger; we add the regulatory intelligence layer on top
- **Source:** [GitHub](https://github.com/darcys22/godbledger), [GoDBLedger.com](https://godbledger.com/)

---

## Synthesis: Validated Patterns for Our Architecture

### 1. Knowledge graph for regulatory rules works at scale
Intuit proved it with TurboTax (70,000+ rules). Our ~200-500 rules are well within feasibility.

### 2. Temporal versioning with valid_from/valid_to
Neo4j, Corlytics, AscentAI all use this. Apply to DPH rates, thresholds, booking rules. Consider bi-temporal (business date + process date).

### 3. AI proposes, human validates
AscentAI, Corlytics, Be Informed all follow: AI extracts changes → human validates → update inventory. Exactly our Layer 4 regulation update loop.

### 4. Decision table format for rule representation
DMN standard, Drools, Vertex all use condition → action tables. Consider DMN-style decision tables as internal format: input columns (transaction type, supplier type, DPH status) → output columns (debit account, credit account, DPH rate, KV section). Accountant-readable AND machine-executable.

### 5. Hierarchical classification with fallback
Vertex pattern: specific rule → category rule → default rule. Build this into our rule resolver.

### 6. Deterministic first pass + AI fallback
Beancount smart_importer pattern: explicit rules for known patterns, ML/AI for the rest. Matches our design: deterministic engine handles standard flows, AI assists on ambiguous cases.

### 7. AI proposes → human validates → deterministic engine executes
Sphere's TRAM model: AI analyzes tax law, human approves determination, live engine executes with zero AI. a16z-validated at $21M Series A.

### 8. Schema-light for ingestion, strict schema for execution
RAGulating Compliance paper: let graph schema emerge from source material during ingestion. But execution rules need a strict, machine-interpretable contract.

### 9. Programmable ledger as API-first server
GoDBLedger: double-entry server with GRPC endpoints. Transactions arrive via API, validated and recorded. Our engine adds rule resolution + tax calculation on top of this pattern.

### 10. Domain-decomposed knowledge graphs
Regulatory knowledge decomposes into atomic domains with independent versioning. Validated by DDD (bounded contexts), compliance graph patterns (PuppyGraph), and Avalara's three-concern separation. Applied to Slovak accounting: four domain graphs (Posting Rules, DPH/VAT, Reporting, Payroll), each with different density, update frequency, and legal sources. Cross-graph references link them without coupling versioning.

---

## Architecture Recommendations from Research

| Decision | Recommendation | Based on |
|----------|---------------|----------|
| Rule engine | Don't use Drools/BRMS. Python + PostgreSQL with structured rules | Too heavy for our scale, wrong language |
| Rule format | DMN-style decision tables within graph nodes | Accountant-readable, machine-executable, industry standard |
| Versioning | Bi-temporal (business date + process date) on rules and rates | Neo4j pattern, AscentAI, regulatory best practice |
| Classification | Hierarchical with fallback: specific → category → default | Vertex tax engine pattern |
| Change management | AI extracts → proposes diff → human validates → apply with effective date | AscentAI, Corlytics, Be Informed (20+ years proven) |
| AI boundary | Deterministic first pass, AI only for uncertain classification | Beancount smart_importer, Digits confidence routing |
| Separation | Classification (what) → Context (who/where) → Rule lookup (how to book) | Avalara three-concern separation |
| AI ↔ Engine boundary | AI proposes, human validates, deterministic engine executes (no AI in posting) | Sphere TRAM pattern (a16z validated) |
| Graph ingestion | Schema-light initial extraction, strict schema for execution rules | RAGulating Compliance paper |
| Ledger architecture | API-first programmable server, double-entry validation at core | GoDBLedger pattern |
| Knowledge dual layer | Graph for rule relationships + pgvector for semantic search | AgentiveAIQ, Graphiti |
| Domain decomposition | Four atomic graphs (Posting Rules, DPH, Reporting, Payroll) with independent versioning | DDD bounded contexts, Avalara separation, compliance graph patterns |
| Traceability | Every AI output backed by verifiable source, full audit trail | Tellen.ai, Intuit TKG, compliance best practice |
| Graph scaling | Start PostgreSQL, monitor TigerGraph as hybrid graph+vector alternative to Neo4j | TigerGraph hybrid search capability |
