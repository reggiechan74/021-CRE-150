---
title: Tender Evaluation Methodology — Roofing (Ontario)
date: 2026-04-15
keywords: [tender-evaluation, roofing, ontario, ccdc, bps-directive, contract-a-contract-b, mcda, bid-scoring]
lastUpdated: 2026-04-15
category: domain-knowledge
documentType: reference
status: draft-v1
---

# Tender Evaluation Methodology — Roofing Contractor Bids (Ontario)

> Reference material for an AI plugin evaluating roof replacement tender submissions. Every evaluation recommendation the plugin produces should be traceable to an authoritative source cited here. Sources are listed at the bottom with retrieval dates.

## 1. Tender Document Standards in Ontario

Ontario roofing procurement sits on top of a stack of nationally standardized instruments (CCDC/CCA contract forms), a body of Supreme Court of Canada tendering law (the *Contract A / Contract B* doctrine), and — for public sector owners — the Ontario Broader Public Sector (BPS) Procurement Directive. An AI evaluator should know which layer governs the file it is reading before it scores anything.

### 1.1 CCDC 23 — *A Guide to Calling Bids and Awarding Contracts* (2018)

CCDC 23 is the Canadian Construction Documents Committee's authoritative practice guide for owners and consultants on how to call and award a construction tender. It is not itself a contract — it is the "how to run a bid" manual the rest of the CCDC form family assumes you followed. The 2018 edition covers:

- Fundamental principles of the law of competitive bidding (including the obligations *Contract A* imposes on both owner and bidder);
- Calling for bids: solicitation, bidding period, pre-bid meetings, site visits, inquiries, and addenda;
- Receiving bids: closing dates, modifications, bid opening, two-stage closings, electronic receipt;
- Awarding the contract: compliance evaluation, selection of the successful bidder, post-bid negotiation, and re-bidding.

An AI evaluator should treat CCDC 23 as the baseline checklist for *procedural fairness* — if the tender package the owner issued violates a CCDC 23 principle (e.g. accepting bids after closing, evaluating on undisclosed criteria), that is itself a red flag independent of contractor quality.

### 1.2 CCDC 2 — *Stipulated Price Contract* (2020)

CCDC 2 is the industry-standard prime contract between Owner and prime Contractor in Canada, establishing a single, pre-determined fixed (lump sum) price for the project. It governs the role of the consultant, change procedures, insurance, Ready-for-Takeover, dispute resolution, and early occupancy. On commercial roof replacements above roughly $250K, or on any occupied commercial building, most Ontario owners will specify CCDC 2 – 2020 as the prime contract. The 2020 edition introduced a Ready-for-Takeover milestone that replaced the older Substantial Performance trigger for owner occupancy.

### 1.3 CCA 1 — *Stipulated Price Subcontract* (2021)

CCA 1 is the Canadian Construction Association's standard subcontract form between a prime contractor and a subcontractor, paired with a fixed/stipulated price. On larger tenders, the roofing scope is frequently subcontracted; the plugin should flag any bid that fails to name the actual roofing sub or attempts to rely on an unexecuted/unpriced CCA 1.

For *direct* (small to mid-size) roofing procurements — typical residential-institutional roof-only replacements up to roughly $500K — owners commonly issue the work under a fixed-price form modelled on CCA-1 rather than the heavier CCDC 2, using the roofing contractor as the prime. The key point is that the dominant procurement archetype for Canadian roof replacement is *stipulated price* (fixed lump sum), not unit price or cost-plus. This is what the plugin should assume unless the tender document says otherwise.

### 1.4 The *Contract A / Contract B* Doctrine — *R v Ron Engineering* (1981 SCC)

All Canadian tender evaluation sits under the two-contract framework established by the Supreme Court of Canada in *The Queen (Ont.) v. Ron Engineering and Construction (Eastern) Ltd.*, 1981 CanLII 17 (SCC). The doctrine:

- **Contract A** is formed the instant a compliant bid is submitted in response to a formal tender call. Its principal term is the *irrevocability of the bid* during the bid-acceptance period; bid security exists to enforce it.
- **Contract B** is the actual construction contract, formed only with the successful bidder when the owner accepts the tender.

The owner "writes the rules of the tender" in the Instructions to Bidders; both the owner and the bidders must then follow those rules to the letter. Deviation creates Contract A liability. This is why an AI evaluator must rigidly distinguish *mandatory* (pass/fail) requirements from *rated* (scored) criteria, and must never reward a bid that fails a mandatory — doing so breaches Contract A with every compliant bidder the owner did not award the work to.

### 1.5 Privilege Clauses and Their Limits — *MJB Enterprises v. Defence Construction* (1999 SCC) and *Tercon* (2010 SCC)

A standard *privilege clause* reads: "the lowest or any other tender shall not necessarily be accepted." In *M.J.B. Enterprises Ltd. v. Defence Construction (1951) Ltd.*, [1999] 1 SCR 619, the SCC held that Contract A contains an implied term that *only a compliant tender can be accepted* — and the privilege clause does **not** override this. An owner may choose among compliant bidders on grounds beyond price (value, qualifications, schedule), but cannot use the privilege clause as cover to award to a materially non-compliant bid.

*Tercon Contractors Ltd. v. British Columbia (Transportation and Highways)*, 2010 SCC 4, tightened this further: even broadly drafted exclusion-of-liability clauses will not protect an owner who awards to a bidder who was *ineligible to bid in the first place*. The majority held that accepting an ineligible bid sits *outside* the tender process and therefore outside the exclusion clause's protection.

Practical implications for the AI evaluator:

1. A privilege clause is **not** a license to pick any bidder. It narrows the owner's discretion to the pool of compliant bidders only.
2. A clearly non-compliant bid must be recommended for rejection, regardless of price.
3. An "ineligible" bidder (e.g. not pre-qualified, not manufacturer-certified where the spec requires it, WSIB not in good standing) cannot be rehabilitated by a privilege or exclusion clause.

## 2. Mandatory vs Rated Evaluation Structure

The Ontario BPS Procurement Directive (v. February 2024) requires that competitive procurement documents "clearly outline mandatory, rated, and other criteria that will be used to evaluate submissions, including weight of each criterion," and that criteria be developed, reviewed, and approved *before* the procurement is issued. This separation between mandatory gates and rated criteria is also the structure CCDC 23 assumes.

### 2.1 Mandatory Requirements (Pass/Fail Gates)

Mandatory requirements are *compliance* tests. A bid either clears them or is rejected — there is no scoring. For an Ontario roof replacement, the typical mandatory set includes:

| Gate | Typical Threshold | Source |
|---|---|---|
| **WSIB clearance certificate** | In good standing; not expired as of bid closing (and re-verified before award) | Ontario expanded compulsory coverage for construction (WSIB) |
| **Certificate of Insurance — CGL** | $2M/occurrence minimum for most work; $5M typical for commercial, occupied, or institutional | Ontario market standard; typically specified in tender package |
| **Bid bond** | 10% of bid price (public sector and larger private projects) | CCDC 220 form; CCA practice |
| **Consent of Surety** | Commitment to provide Performance Bond and Labour & Material Payment Bond, each 50% of contract price | CCA practice; standard Ontario public bid form |
| **Addenda acknowledgment** | Every addendum issued must be signed/acknowledged on the bid form | CCDC 23 |
| **Working-at-heights training** | Current Ontario MOL-approved WAH training for all field workers | O. Reg. 297/13 under OHSA |
| **Non-collusion / bid-rigging declaration** | Signed declaration required under *Competition Act* s.47 | Competition Bureau guidance |
| **Manufacturer certification** (if spec calls out a system) | Bidder is a current authorized/certified installer for the specified membrane system | Required for most NDL warranties |
| **Bid form completeness** | All price lines filled, unit prices where required, no qualifications or exclusions beyond those the tender expressly permits | CCDC 23; *MJB Enterprises* |

Failure on any one of these is fatal. An AI evaluator should produce a single "Mandatory Compliance" section that is binary per gate; a bid with any FAIL does not proceed to rated scoring.

### 2.2 Rated Criteria (Scored)

Rated criteria are where judgment enters. Typical categories for a roof replacement RFP:

- **Technical approach / methodology** — tear-off sequencing, temporary weatherproofing strategy, dust and odour controls, tie-in details, flashing design.
- **Experience with similar projects** — same system type (e.g. 2-ply SBS, TPO, EPDM, PVC), comparable size, comparable complexity (mechanical congestion, occupied building, heritage).
- **References** — typically 3–5 recent (last 5 years) similar projects, owner-verifiable.
- **Project schedule** — realistic durations, weather contingency, milestones, crew size.
- **Key personnel** — named site superintendent, roofing foreman with verifiable project history; some tenders require CVs and named crew leads.
- **Price** — almost always the single largest rated category (see §3).

## 3. MCDA Weighting Patterns for Roofing Tenders

Multi-criteria decision analysis (MCDA) frameworks dominate private-sector and best-value public-sector roofing evaluations. Weights vary by project archetype. The ranges below are representative of Ontario commercial/institutional practice and are consistent with the weighted-scoring literature (Mastt, Thornton & Lowe, Tasmanian *Guidelines on Tender Evaluation using Weighted Criteria for Building Works and Services*).

### 3.1 Baseline Owner-Side Weighting — Commercial Roof Replacement

| Criterion | Typical Weight | Notes |
|---|---|---|
| Price | 40–50% | Floor is ~35% (heritage/hospital); BPS low-price evaluations push to 70%+ |
| Technical/Experience | 20–30% | Methodology, similar-project experience, references |
| Warranty & Materials Quality | 15–20% | NDL vs prorated; system vs materials-only |
| Schedule | 5–10% | Higher on occupied buildings and weather-sensitive timing |
| Qualifications/Certifications | 10–15% | Manufacturer certification, WSIB/IHSA standing, safety record |

These ranges are defensible baselines — not floors or ceilings — and should shift for project context.

### 3.2 How Weightings Shift by Project Type

- **Occupied commercial building** — Schedule and technical approach weight up (shift ~5 points from Price into Schedule+Technical). Tenant disruption, interior leak risk during tear-off, and noise/odour controls dominate owner concerns. Expect Price 35–40%, Technical 25–30%, Schedule 10–15%.
- **Heritage or architecturally complex roof** — Technical and Qualifications weight up. Flashing details, copings, drainage complexity, and custom fabrication skill matter more than unit price. Expect Technical 30–35%, Qualifications 15–20%, Price 30–40%.
- **Straightforward re-roof** (vacant warehouse, simple membrane replacement) — Price weight up to 50–60%. Technical differentiation between qualified bidders is low; commodity pricing wins.
- **Public / BPS procurement** — The Ontario BPS Procurement Directive does not set a fixed weight, but public procurement culture and the *CFTA/CETA* non-discrimination framework pushes toward *lowest-compliant-bid* or price-heavy weighted models. Price 60–70% is common; full lowest-compliant-bid with pass/fail gates is also common for well-defined scopes.

### 3.3 Price Scoring Formula

The standard Canadian weighted-price scoring formula:

```
Price Score = (Lowest Compliant Bid / This Bid) × Price Weight
```

So if the price weight is 50% and the lowest bid is $100K and this bid is $110K, this bidder earns (100/110) × 50 = 45.5 out of 50 available price points. This formula is widely used because it is bounded (max score at lowest bid, asymptotic toward zero as price rises), and because it penalizes outliers symmetrically.

### 3.4 Rated-Criterion Rubrics

Rated criteria should be anchored on a 0–5 or 0–10 scale with written descriptors at each level. Typical 5-point anchors:

- **5 — Exceeds**: Demonstrates depth beyond the requirement; adds value the owner hadn't requested.
- **4 — Strong**: Fully meets with high confidence; minor gaps only.
- **3 — Adequate**: Meets the minimum; no concerns but no standout.
- **2 — Weak**: Meets partially; non-trivial gaps that would require clarification.
- **1 — Poor**: Major deficiencies; would not award on this criterion alone.
- **0 — Non-responsive**: Missing or wholly inadequate.

Anchor descriptors must be drafted *before bids are opened* and shared with the evaluation team — this is explicit in the BPS Procurement Directive and in CCDC 23. An AI evaluator should refuse to score against rubrics that were introduced after bid opening.

### 3.5 Normalization

For rated criteria with raw scores from different scales, min-max linear normalization is standard:

```
Normalized = (Raw − Min) / (Max − Min)
```

For price, the ratio formula in §3.3 is the normalization.

## 4. Common Red Flags and Bid Pathologies

The plugin should surface each of these as a named red flag with a confidence level. Each is drawn from the construction-procurement and roofing-warranty literature cited in the Sources section.

### 4.1 Unbalanced Bidding

A contractor *front-loads* by overpricing early line items (mobilization, tear-off) and underpricing late items (allowance-driven wood decking replacement, flashing, cap metal). Two variants:

- **Mathematically unbalanced** — line prices deviate significantly from reasonable costs. Not per se prohibited.
- **Materially unbalanced** — the bid *advantages the contractor if quantities change*, or the front-loading creates a cash-flow risk for the owner. This is a rejectable condition under most Canadian public-sector rules (and under the US FHWA standard, which Canadian owners often cite).

**Evaluator test**: Compare each line item against the spread of other bidders. Flag items more than ~25% above or below the mean where the line item is likely to grow via change order (decking, insulation above R-value, flashing LF).

### 4.2 Vague Exclusions and Carried-Out Scope

Bids that add "exclusions" the tender did not permit, or that use vague qualifiers ("subject to site conditions," "additional flashing by change order"), are creating scope gaps the contractor intends to convert into change orders. Under *MJB*, a bid with material unrequested exclusions is non-compliant and must be rejected.

**Evaluator test**: Any exclusion or clarification not expressly invited by the tender is a flag. Quote the exact language.

### 4.3 Low-Bid Trap

Empirical pattern: bids 15% or more below the next-lowest carry meaningfully higher probability of (a) contractor bankruptcy mid-project, (b) quality disputes, (c) aggressive change-order behaviour, and (d) scope cuts via "value engineering" after award. "Beware the Low Bid" (Partner Engineering) and CMAA guidance both call this out.

**Evaluator test**: Compute the gap between lowest and second-lowest. If >15%, flag and require the plugin to (i) scrutinize the contractor's financial standing, (ii) check for missing scope, (iii) recommend a bid-verification meeting before award.

### 4.4 Allowance Manipulation

For roof replacement, the specification almost always carries allowances for wood decking replacement (board-feet), wet insulation replacement (sqft), and sometimes mechanical curb rework. Bidders can game this by carrying below-market unit prices for the allowance (undercutting the base bid) while the real-world quantity will exceed the allowance.

**Evaluator test**: Cross-check unit prices against the CRCA-typical ranges and against the other bidders' unit prices. Flag deviations >20%.

### 4.5 "Or Equivalent" Substitutions Without Naming

The spec named a particular manufacturer system (e.g. "Soprema SOPRALENE 2-ply SBS or equivalent"). The bidder writes "or equivalent" without naming which product they will actually supply. This is both a scope ambiguity *and* a warranty risk (see §4.8).

**Evaluator test**: Any "or equivalent" line without a named product is a mandatory-level clarification before award.

### 4.6 Incomplete or Missing Product Data Sheets

Commercial roof specs typically require submittal of product data sheets (PDS), SDS, CCMC listings (Canadian Construction Materials Centre), and sometimes independent test reports (ASTM, CSA, UL). Bids that decline to attach these are hiding either a substitution or a non-listed product.

### 4.7 Warranty Language Games

Watch for:

- **"25-year warranty" that is materials-only and prorated** — coverage falls year-over-year. A prorated warranty at year 15 may cover 40% of material cost and 0% labour.
- **Material-and-labour warranty** offered by the *contractor* rather than the *manufacturer* — contractor companies churn; a 20-year contractor workmanship warranty from a small regional outfit is effectively unsecured.
- **NDL (No Dollar Limit) warranty** — the top tier: manufacturer covers full repair/replacement cost (material + labour) with no annual or lifetime cap, for the stated term (typically 20 years). Requires manufacturer-certified installer.

**Evaluator test**: The plugin should parse the warranty offered into a canonical form (Manufacturer vs Contractor, Material-only vs System, Prorated vs Non-prorated, NDL vs Capped, Term years, Required annual maintenance Y/N) and score against the tender's stated warranty requirement. Anything less than what the spec demanded is non-compliant.

### 4.8 Contractor Not Certified to Install the Specified System

Manufacturers (GAF, Soprema, Firestone/Holcim, Carlisle, Sika, IKO, Johns Manville, etc.) only issue NDL warranties when the install is performed by a contractor currently authorized and in good standing on their certified installer list. A bidder who is not currently certified cannot deliver the spec'd warranty, even if they are a competent roofer.

**Evaluator test**: Verify the bidder appears on the named manufacturer's current certified-contractor list at bid closing. If not, the bid fails the warranty mandatory.

### 4.9 Unnamed Subcontracted Crew

Some roofing "contractors" are brokers who subcontract the roof work to whoever is cheapest that week. Under CCA 1 discipline and under CCDC 2 §3.7, the prime must identify material subcontractors. A bid that refuses to name the actual crew performing the roof work is a red flag.

**Evaluator test**: Require the bid form to name the field subcontractor (if any) and the named foreman. Flag bids that leave these blank or reserve "to be determined."

## 5. Bid Scoring Methods

### 5.1 Lowest-Compliant-Bid (Pure Price + Pass/Fail Mandatories)

The default BPS model for well-scoped work. The evaluator:

1. Applies each mandatory gate in §2.1. Any fail → reject.
2. Ranks remaining compliant bids by price.
3. Recommends award to the lowest-priced compliant bid.

Defensible, simple, hard to litigate under the Ron Engineering framework. Weakness: rewards the low-bid trap (§4.3) when scope is ambiguous.

### 5.2 Weighted Scoring / Best Value

Used where technical, schedule, or warranty factors materially affect lifecycle cost. Mandatories still gate; surviving bids are scored against the MCDA weight matrix in §3. The highest-weighted-score bid wins.

### 5.3 Two-Envelope / Two-Stage

Technical envelope opens first; technical score must meet a threshold (typically 70% of rated points) before price envelope is opened. Used for complex roofs where owners want to eliminate underqualified low bidders before price becomes visible. Permitted under BPS if disclosed in the tender package.

### 5.4 Life-Cycle / Total Cost of Ownership Scoring

Scoring formula folds warranty and expected maintenance into bid price, e.g.:

```
TCO = Bid Price + PV(Expected Maintenance over Warranty Term) − PV(Residual Warranty Value)
```

Weight Price on TCO rather than nominal bid. More defensible for owners replacing a 25-year-life asset. Less common in Ontario public practice because the discount-rate assumptions invite challenge.

## 6. Recommendation Memo Structure

What owners, property-management boards, and institutional procurement committees want to see in the evaluator's output memo. The plugin should default to this structure:

### 6.1 Executive Summary
- Recommended awardee: **[Company, $Amount, Date]**
- One-paragraph rationale: why this bid wins on the stated criteria.
- Conditions of award (if any) listed inline (see §6.7).

### 6.2 Bid Tabulation
A table with one row per bidder:

| Bidder | Base Bid | Allowances Carried | Bonding | Mandatory Compliance | Notable Exclusions |
|---|---|---|---|---|---|

### 6.3 Scoring Matrix
The full MCDA matrix showing raw scores, weights, weighted scores, and total. If the method is lowest-compliant-bid, show price rank and compliance status.

### 6.4 Red Flag Summary
Every §4 pathology detected, per bidder, with the evidence (quoted from the bid document) and a confidence level (High / Medium / Low).

### 6.5 Risk Assessment
- Contractor financial risk (years in business, references, litigation/lien history, bond capacity).
- Schedule risk (is the proposed schedule achievable? weather contingency? crew availability?).
- Scope risk (what exclusions or ambiguities could become change orders?).
- Warranty risk (gap between spec requirement and offered warranty).

### 6.6 Alternates and Add-Ons Analysis
Most roofing tenders carry alternates (e.g. upgrade from 2-ply SBS to 3-ply, cover board upgrade, increased R-value). Tabulate each alternate's net cost across all bidders and note the owner's decision.

### 6.7 Conditions of Award
What must be clarified, negotiated, or produced before the owner signs Contract B:
- Refreshed WSIB clearance and current COI with owner/consultant as additional insured.
- Executed Performance and L&M bonds.
- Named manufacturer-certified foreman and roofing sub.
- Written confirmation of warranty terms matching spec.
- Any ambiguity in exclusions resolved in writing.
- Schedule confirming start date, weather-sensitive milestones, and Ready-for-Takeover date.

### 6.8 Appendix
- Cross-reference each evaluator finding to the page of the bid document that supports it.
- List all sources (spec sections, CCDC/CCA references, legal authorities) the memo relies on.

## 7. Evaluator Plugin Operating Rules

Operational rules for the plugin to enforce on itself, distilled from the above:

1. **Cite or stay silent** — every scoring call or red-flag finding cites a source (spec clause, bid page, authority from this document).
2. **Mandatories first, always** — never proceed to rated scoring until every bid has been run through §2.1.
3. **Do not invent criteria** — score only against criteria disclosed in the tender package. Undisclosed criteria breach *Ron Engineering* / *MJB*.
4. **Flag, do not hide** — when two bids are close on total score, produce the memo with both; do not manufacture differentiation the scoring does not support.
5. **Privilege clause is not a hall pass** — the plugin never recommends awarding to a non-compliant or ineligible bidder, regardless of any privilege clause language in the tender package.
6. **Low-bid delta check** — when the lowest bid is >15% below the second-lowest, the plugin recommends a bid-verification meeting before award and explicitly names the low-bid trap as a surfaced risk.
7. **Warranty-to-spec match** — the plugin parses warranty offers into canonical form and compares to spec. A mismatch is either a mandatory failure (if warranty was a mandatory) or a rated deduction (if rated).
8. **Name the installer** — the plugin requires the bid to name the actual roofing foreman and any subcontracted crew before it will score the bid on experience or qualifications.

---

## Sources

Sources consulted April 15, 2026. Prefer the 2020+ editions where cited.

- [CCDC 23 – 2018 A Guide to Calling Bids and Awarding Contracts (table of contents PDF)](https://www.ccdc.org/wp-content/uploads/2015/06/2018CCDC23TOC.pdf) — ccdc.org
- [CCDC 23 – 2018 product page](https://www.ccdc.org/document/ccdc23/) — ccdc.org
- [CCDC 23 – 2018 via Ontario General Contractors Association](https://ogca.ca/product/ccdc-23-ev/) — ogca.ca
- [CCDC 2 – 2020 Stipulated Price Contract product page](https://www.ccdc.org/document/ccdc-2-2020/) — ccdc.org
- [Construction Contracts in Canada: The New CCDC 2 – 2020 Stipulated Price Contract (Clark Wilson)](https://www.cwilson.com/construction-contracts-in-canada-the-new-ccdc-2-2020-stipulated-price-contract/)
- [What the new CCDC 2 Stipulated Price Contract means for you (Gowling WLG, 2020)](https://gowlingwlg.com/en/insights-resources/articles/2020/what-the-new-ccdc-2-stipulated-price-contract-mean)
- [CCA-1 – 2021 Stipulated Price Subcontract (Canadian Construction Association)](https://www.cca-acc.com/cca_documents/cca-1-2021-stipulated-price-subcontract/)
- [R v Ron Engineering and Construction (Eastern) Ltd., 1981 CanLII 17 (SCC)](https://www.canlii.org/en/ca/scc/doc/1981/1981canlii17/1981canlii17.html) — CanLII
- [R v Ron Engineering — Wikipedia summary](https://en.wikipedia.org/wiki/R_v_Ron_Engineering_and_Construction_(Eastern)_Ltd)
- [Contract A and Contract B in Canadian contract law — Wikipedia](https://en.wikipedia.org/wiki/Contract_A_and_Contract_B_in_Canadian_contract_law)
- [The "Privilege Clause" in Construction Tender Documents — M.J.B. Enterprises v. Defence Construction (Clark Wilson)](https://www.cwilson.com/the-qprivilege-clauseqin-construction-tender-documents-supreme-court-of-canada-decision-in-mjb-enterprises-v-defence-construction-ltd/)
- [M.J.B. Enterprises v. Defence Construction (1951) — CanLII Connects summary](https://canliiconnects.org/en/summaries/32014)
- [Tercon Contractors Ltd. v. British Columbia (Transportation and Highways), 2010 SCC 4](https://decisions.scc-csc.ca/scc-csc/scc-csc/en/item/7843/index.do)
- [Tercon — Wikipedia](https://en.wikipedia.org/wiki/Tercon_Contractors_Ltd._v._British_Columbia_(Transportation_and_Highways))
- [Procurement 101: How Not To Turn Your Next Procurement Into New Case Law (Fasken, 2020)](https://www.fasken.com/en/knowledge/2020/08/procurement-101-how-not-to-turn-your-next-procurement-in-to-new-case-law)
- [Ontario Broader Public Sector Procurement Directive (February 2024)](https://www.ontario.ca/files/2024-02/tbs-bps-procurement-directive-en-2024-02-08.pdf)
- [Ontario BPS Procurement Directive — Supply Ontario landing](https://www.doingbusiness.mgs.gov.on.ca/mbs/psb/psb.nsf/Attachments/BPSProcDir-eng/$FILE/BPSProcDir-eng.html)
- [BPS Procurement Directive Implementation Guidebook (Ontario)](https://www.doingbusiness.mgs.gov.on.ca/mbs/psb/psb.nsf/Attachments/BPSProc_procurement_implementation-eng/$FILE/bps_procurement_implementation.html)
- [BPS Procurement Directive Toolkit (Ontario)](https://www.doingbusiness.mgs.gov.on.ca/mbs/psb/psb.nsf/attachments/bpsproc-toolkit-pdf-eng/$file/bpsproctoolkit-eng.pdf)
- [Canadian Roofing Contractors Association — Manuals hub](https://roofingcanada.com/technical-guidance/manuals/)
- [Canadian Roofing Reference Manual — Online (CRCA)](https://roofingcanada.com/technical-guidance/manuals/crrm-online/)
- [CRCA Technical Bulletins](https://roofingcanada.com/technical-guidance/bulletins/technical-bulletins/)
- [Roofing Specifications Manual available (Construction Canada, CRCA)](https://www.constructioncanada.net/roofing-specifications-manual-available/)
- [WSIB — Clearances](https://www.wsib.ca/en/businesses/premiums-and-payment/clearances)
- [WSIB — Clearance Certificate in Construction (Operational Policy Manual)](https://www.wsib.ca/en/operational-policy-manual/clearance-certificate-construction)
- [WSIB — Expanded compulsory coverage in construction](https://www.wsib.ca/en/businesses/registration-and-coverage/expanded-compulsory-coverage-construction-industry)
- [IHSA — Mandatory WSIB coverage in construction](https://www.ihsa.ca/pdfs/businessowners/mandatory_coverage_in_construction.pdf)
- [How to Request & Verify a Contractor's Certificate of Insurance (COI) in Ontario (Reith & Associates)](https://www.reithandassociates.com/blog/how-to-request-verify-a-contractors-certificate-of-insurance-coi-in-ontario-k45ef)
- [Construction Insurance Requirements Ontario 2026 (SmartSMS)](https://smartsmssolutions.com/resources/blog/ca/construction-insurance-requirements-ontario)
- [Contractor Insurance Requirements Ontario — 2026 (Niagara Stands Out)](https://niagarastandsout.ca/blogs/news/contractor-insurance-requirements-ontario-wsib-liability-guide)
- [FHWA — Rejection of Unbalanced Bids](https://www.fhwa.dot.gov/construction/contracts/870729.cfm)
- [CMAA — Unbalanced Bids and Avoiding Disputes (PDF)](https://www.cmaanet.org/sites/default/files/resource/Unbalanced%20Bids%20and%20Avoiding%20Disputes.pdf)
- [Levelset — Avoid Unbalanced Bids to Prevent Payment Disputes](https://www.levelset.com/blog/unbalanced-bids/)
- [Partner Engineering — Beware the Low Bid](https://www.partneresi.com/resources/articles/beware-the-low-bid/)
- [Well Built Construction Consulting — Escaping the Low-Bid Trap](https://www.wellbuiltconsulting.com/newsletter-archive/the-high-price-of-low-bidding)
- [Understanding Commercial Roofing Warranties: NDL, Material, and Workmanship (Windward Roofing)](https://windwardroofing.com/blog/commercial-roofing-warranties)
- [Understanding NDL Warranties in Commercial Roofing (United Roofing)](https://roofingunited.com/understanding-ndl-warranties-in-commercial-roofing/)
- [Prorated vs Non-Prorated Commercial Roof Warranties (DuraTec)](https://duratecroofing.com/understanding-commercial-roof-warranties/)
- [GAF Commercial Roof Warranty and Guarantee Comparison Guide](https://www.gaf.com/en-us/resources/warranties/commercial-guarantees)
- [Mastt — Tender Evaluation in Construction: Process, Scoring, & Compliance](https://www.mastt.com/guide/tender-evaluation)
- [Mastt — Tender Evaluation Criteria: A Practical Guide](https://www.mastt.com/blogs/evaluation-criteria)
- [Thornton & Lowe — Moderated Scoring: Tender Evaluation Best Practice](https://thorntonandlowe.com/moderated-scoring-tender-evaluation/)
- [Tasmanian Government — Guidelines on Tender Evaluation using Weighted Criteria for Building Works and Services (PDF)](https://www.purchasing.tas.gov.au/Documents/Guidelines-on-Tender-Evaluation-using-Weighted-Criteria-for-Building-Works-and-Services.pdf)
- [LDCA — Bidding and Awarding Construction Contracts (PDF)](https://cdn.ymaws.com/ldca.on.ca/resource/resmgr/policies/bidding_and_awarding_constru.pdf)
- [CanadaBuys — Sample Roof Replacement Tender Package (M35 Section 4-7)](https://canadabuys.canada.ca/sites/default/files/webform/tender_notice/72462/25-58119---m35-section-4---7-roof-replacement---tender-package-english.pdf)
