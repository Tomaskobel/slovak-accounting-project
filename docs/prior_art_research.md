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

---

## Architecture Recommendations from Research

| Decision | Recommendation | Based on |
|----------|---------------|----------|
| Rule engine | Don't use Drools/BRMS. Python + PostgreSQL with structured rules | Too heavy for our scale, wrong language |
| Rule format | DMN-style decision tables within graph nodes | Accountant-readable, machine-executable, industry standard |
| Versioning | Bi-temporal (business date + process date) on rules and rates | Neo4j pattern, AscentAI, regulatory best practice |
| Classification | Hierarchical with fallback: specific → category → default | Vertex tax engine pattern |
| Change management | AI extracts → proposes diff → human validates → apply with effective date | AscentAI, Corlytics, Be Informed (20+ years proven) |
| AI boundary | Deterministic first pass, AI only for uncertain classification | Beancount smart_importer, our corrected architecture |
| Separation | Classification (what) → Context (who/where) → Rule lookup (how to book) | Avalara three-concern separation |
