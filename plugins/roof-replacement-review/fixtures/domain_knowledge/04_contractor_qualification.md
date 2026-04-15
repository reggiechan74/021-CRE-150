---
title: Ontario Roofing Contractor Qualification Reference
date: 2026-04-15
keywords: [ontario, roofing, contractor-qualification, wsib, cgl-insurance, skilled-trades, tender-evaluation, bps-procurement]
lastUpdated: 2026-04-15
category: domain-knowledge
documentType: reference
status: active
---

# Ontario Roofing Contractor Qualification & Compliance Reference

**Purpose.** Reference material for an AI plugin that evaluates roofing contractor tender submissions in Ontario. Every claim below is linked to a primary or industry-authority source in the Sources section. Plugin output must cite these sources when flagging qualification issues.

**Jurisdictional scope.** Ontario only. Rules differ materially in other provinces (e.g., WorkSafeBC, CNESST).

---

## 1. WSIB (Workplace Safety & Insurance Board) — Ontario

### 1.1 Clearance certificate — what it shows

A WSIB clearance certificate is issued under the *Workplace Safety and Insurance Act, 1997* and confirms that, as of the issue date, the contractor is:

- Registered with WSIB
- Reporting insurable earnings
- Paying premiums
- Otherwise in compliance with the Act

The certificate names the contractor's legal business name, WSIB account number, classification, issue date, and validity period. **Hiring parties ("principals") who contract with construction firms are required to obtain a clearance from each contractor and keep it on file for at least three years.** Without a valid clearance, the principal can become liable for the contractor's unpaid WSIB premiums. [Source: WSIB Operational Policy — Clearance Certificate in Construction]

### 1.2 How to verify authenticity

Clearance certificate numbers must be verified directly on WSIB's online system (`clearances.wsib.ca`). Never accept a scanned PDF at face value — certificate numbers can be faked; WSIB's online verifier is authoritative and returns a live "valid / not valid" response against a certificate number and account number. [Source: WSIB — Get a clearance certificate / Clearances FAQs]

### 1.3 Validity period

The standard validity period is **up to 90 calendar days** from issue, after which the clearance must be renewed. WSIB has operated a **temporary validity-extension program**: clearances issued on or after Aug 20, 2025 were extended to Feb 19, 2026, with renewal cycles every three months through 2026 (Feb 20 / May 20 / Aug 20 / Nov 20). Evaluators should check the current renewal cycle at WSIB's site rather than assume a fixed 60/90-day rule. [Source: WSIB — Clearances page]

### 1.4 "In good standing" vs "not in good standing"

A clearance is only issued when the account is "in good standing" — all returns filed, all premiums paid, no past-due reconciliations. An account flagged "not in good standing" indicates outstanding premiums, unfiled reconciliations, or open compliance issues. A bidder who cannot produce a current clearance is, by WSIB's definition, not in good standing on the issue date. [Source: WSIB — Understanding your rate]

### 1.5 Construction is compulsory coverage (Bill 119)

Effective **January 1, 2013**, under *Bill 119 — Workplace Safety and Insurance Amendment Act, 2008*, WSIB coverage is mandatory for virtually all persons working in the construction industry in Ontario, including:

- Independent operators (IOs)
- Sole proprietors
- Partners in partnerships
- Executive officers of corporations

A narrow exemption allows a construction business to designate **one** partner or executive officer as exempt — but only if that person performs **no** construction work on site, including on-site supervision. Home-renovation-only work performed directly for the occupant (or a family member of the occupant) is also exempt. [Source: WSIB — Expanded compulsory coverage; IHSA — Mandatory Coverage in Construction]

**Implication for bid evaluation:** Any roofing company bidding commercial work must carry WSIB coverage — there is no "we're all subs / we're all principals" exemption. The plugin should flag any claim of WSIB exemption on a commercial roofing tender.

### 1.6 Rate Framework & experience rating (2020 transition complete)

WSIB fully transitioned to its new **Rate Framework** by 2024. Key points:

- Premium rates are set by classification within six construction subclasses and adjusted by **risk band** based on the firm's own six-year claims experience (insurable earnings, claims costs, number of allowed claims).
- A firm can move a **maximum of three risk bands** per year (≈ 15% movement) until its rate reaches the actuarially projected level.
- The **CAD-7 program and NEER experience-rating rebate/surcharge programs have been discontinued** — the old model of back-end rebates and surcharges is gone. Rates themselves now reflect individual experience.
- The Ontario average premium rate was **$1.30 per $100 of insurable payroll in 2024**, the lowest in more than 20 years.

[Source: WSIB — Rate Framework: Construction; WSIB — 2024 premium rates; AWCBC — WSIB 2024 premium rates]

### 1.7 How an evaluator spots a contractor with a poor safety record

1. **Request the contractor's WSIB premium rate or risk band position** within its construction subclass. A firm sitting several risk bands above the subclass average has a worse-than-typical claims history.
2. **Ask for a WSIB Rate Statement** (annual document mailed to the employer). It shows the firm's current rate vs. the projected rate.
3. **Request frequency/severity data for the past 3–5 years** (lost-time injuries, fatalities, critical injuries reported under OHSA s. 51).
4. **Cross-reference Ministry of Labour orders** (see §5 below).
5. **Check COR™ certification status** via IHSA — COR-certified firms have passed an externally audited safety management system (min. 65% on each element, 80% overall). [Source: IHSA — COR Certification]

---

## 2. Commercial General Liability (CGL) Insurance

### 2.1 Typical minimum limits

- **$2M per occurrence** is the default minimum for most Ontario commercial tenders and municipal contracts.
- **$5M** for larger commercial or mid-size institutional work.
- **$10M+** for institutional/BPS (hospital, school board, university, large municipal) or where the project involves significant occupied-building exposure, high-value contents below the roof, or heritage structures.

Limits below these thresholds are a routine disqualifier on public tenders. [Source: ThinkInsure — CGL in Ontario; BrokerForce — CGL in Ontario]

### 2.2 Certificate of Insurance (COI) requirements

A compliant COI for a roofing tender should show:

- **Named insured** matching the bidder's legal entity exactly (watch for shell-company mismatches — see §6).
- **The owner (and often the consultant, construction manager, and property manager) named as additional insured** with respect to the operations of the named insured.
- **Per-occurrence and aggregate limits** at or above RFP requirements.
- **Cross-liability / severability of interests** clause.
- **Waiver of subrogation** in favour of the owner if the contract requires it.
- **30-day notice of cancellation / material change** in favour of the certificate holder.

### 2.3 Completed-operations coverage (critical for roofing)

Completed operations covers claims arising after the work is finished — the classic roofing exposure (leak causes interior water damage six months after installation; ponding triggers structural failure; flashing failure during the next wind event). Without it, the contractor's CGL only covers incidents **during** construction.

**Ask for explicit confirmation of completed-operations coverage on the COI, and a "tail" of at least the length of the manufacturer's system warranty or the contract's warranty period — whichever is longer.** [Source: Surnet — Who Needs CGL; BrokerForce — CGL in Ontario]

### 2.4 Common exclusions in roofing CGL policies (watch-outs)

- **Hot work / torch-on exclusion.** Mod-bit roofing is frequently installed with open-flame torches. Many CGL policies exclude or sub-limit hot-work operations; insurer-required hot-work protocols (fire watch, permits) become contract conditions.
- **Height / elevation exclusion.** Some carriers attach height sub-limits or exclusions above a stated elevation.
- **Contractor pollution liability (CPL) exclusion.** Standard CGL typically excludes pollution. For re-roofing projects with asbestos, lead, or hazmat exposures (see §4), a separate CPL policy is required — usually $2M–$5M.
- **Subcontractor exclusion / warranty.** Some CGL policies exclude liability arising from uninsured subcontractors.
- **Residential-only vs commercial.** A residential roofer's CGL may not cover ICI (industrial/commercial/institutional) work.

### 2.5 When umbrella/excess is appropriate

Umbrella/excess policies sit above the primary CGL and extend limits across multiple underlying policies (CGL, auto, employer's liability). Require an umbrella when:

- The contract minimum exceeds the contractor's primary limit (e.g., $10M required, $2M primary).
- Multiple projects are running concurrently that could erode the aggregate.
- The project involves high-value contents, occupied premises, or institutional use.

---

## 3. Skilled Trades Ontario (formerly Ontario College of Trades)

### 3.1 Roofer — Trade Code 449A, **voluntary** trade

- **Trade code:** 449A — Roofer.
- **Classification:** Non-compulsory (voluntary) trade in Ontario. A worker does **not** need a Certificate of Qualification (C of Q) to perform roofing work, and the trade is **not** listed on Skilled Trades Ontario's Public Register.
- **Apprenticeship:** 4,000 hours total — 3,520 hours on-the-job + 480 hours in-school, roughly two years.
- **Certifying exam** leads to the C of Q 449A, issued by Skilled Trades Ontario after passing. Because the trade is non-compulsory, the certificate **does not require renewal**.

[Source: Skilled Trades Ontario — Roofer trade page; Skilled Trades Ontario — Certificate of Qualification]

### 3.2 What to ask for in a tender

Because 449A is voluntary, "roofer" is an unregulated job title — anyone can work on a roof in Ontario. Quality bidders distinguish themselves via:

- **Number of C of Q 449A holders** on staff. A reasonable ask for commercial tenders: at least one C of Q holder as foreman per crew, plus apprentices registered with STO.
- **Apprentice-to-journeyperson ratio** actually deployed on site (vs. claimed).
- **Copies of C of Q certificates** for the proposed foreman and lead hands.
- **Manufacturer-specific installer certifications** (see §7) — these fill the gap left by the voluntary-trade status.

### 3.3 Working-at-Heights training — mandatory, O. Reg. 297/13

Under **Ontario Regulation 297/13 (Occupational Health and Safety Awareness and Training)**, every worker on a construction project who may use fall-protection equipment must complete an approved Working-at-Heights (WAH) training program **before** working at heights.

- **Initial training:** Approved full program (typically 8 hours, two modules).
- **Validity:** 3 years from successful completion.
- **Refresher:** A 4-hour refresher must be completed before the 3-year expiry to maintain valid certification; if allowed to lapse, the full initial program must be repeated.
- **Provider:** Must be a training provider approved by Ontario's Chief Prevention Officer (CPO) under the *Working at Heights Training Provider Standard*. The CPO maintains the list of approved providers.

**For tender review:** require a roster of all workers who will be on site, each with WAH certificate number, issue date, expiry date, and CPO-approved provider name. Spot-check two or three against the provider's records.

[Source: Ontario.ca — Training for working at heights; O. Reg. 297/13 (CanLII); Ontario.ca — Provider Standard]

### 3.4 Fall-protection equipment inspection

Under **O. Reg. 213/91 (Construction Projects)** s. 26.1 and CSA Z259 series:

- **Pre-use inspection:** Every component (harness, lanyard, SRL, anchor) must be visually and physically inspected by the worker before each shift/use.
- **Annual formal inspection:** At least every 12 months, a **Competent Person** must formally inspect each fall-protection component and record the result. CSA Z259.10-18 recommends annual or more frequent formal inspection.
- **Components must meet the applicable CSA Z259 standard.**
- **Records of formal inspections** should be traceable to individual equipment serial numbers.

For tender review, request a sample of the contractor's fall-protection inspection log and confirm the inspector's credentials (training as a "Competent Person").

[Source: O. Reg. 213/91 (CanLII); IHSA — Personal Fall Protection Chapter 19]

---

## 4. Environmental / Hazmat — Older Buildings

### 4.1 Designated Substances Assessment (DSA) — OHSA s. 30

Under **Section 30 of the Occupational Health and Safety Act**, the **owner** of a building must, before the start of a construction project, determine whether any of the 11 **designated substances** are present, prepare a **Designated Substances Assessment (DSA)**, and provide it to every prospective bidder as part of the tender package. The constructor must ensure the DSA is provided to every contractor and subcontractor before they bid or begin work.

The 11 designated substances in Ontario: acrylonitrile, arsenic, asbestos, benzene, coke oven emissions, ethylene oxide, isocyanates, lead, mercury, silica, and vinyl chloride. On roof replacements, **asbestos, lead, and silica** are the usual suspects.

**Red flag:** A tender that does not include a DSA for a pre-1990 building is non-compliant with OHSA s. 30. Bidders should not price the work without one.

[Source: Ontario.ca — Guide to Designated Substances; Ontario.ca — Guide to the Asbestos Regulation; IHSA — Designated Substances guidance]

### 4.2 Asbestos — O. Reg. 278/05

**Ontario Regulation 278/05 (Designated Substance — Asbestos on Construction Projects and in Buildings and Repair Operations)** governs all asbestos work. Built-up roofing (BUR) systems installed **pre-1980** frequently contain asbestos in felts, mastics, flashing compounds, and roof coatings.

The regulation classifies asbestos work into three types based on risk:

- **Type 1** — lowest-risk non-friable work (e.g., removing a small quantity of intact ACM with hand tools, no power tools). Basic dust controls.
- **Type 2** — medium risk (e.g., removing gasket material, removing small amounts of friable ACM, breaking non-friable ACM with power tools). Enclosed work area, HEPA vacuums, respirators, worker training.
- **Type 3** — highest risk (e.g., removal of >1 m² of friable ACM, spray-applied asbestos removal). Full containment, negative air, decontamination facility, air monitoring, licensed abatement contractor, notice to Ministry of Labour.

Testing for asbestos content must follow **EPA/600/R-93/116** (Method for Determination of Asbestos in Bulk Building Materials).

**For tender review on pre-1980 buildings:** require the DSA, the bidder's abatement sub's licence and training records, and a work plan that classifies the roofing-removal task by type.

[Source: O. Reg. 278/05 (CanLII); Ontario.ca — Asbestos Regulation Guide]

### 4.3 Lead in older flashings and paint

Lead-bearing flashings, coatings, and painted rooftop equipment were common in older buildings. Lead is a designated substance under OHSA; work that disturbs lead-containing materials requires worker training, controls, and (for higher-exposure tasks) air monitoring under the designated-substance regulation framework. The DSA should identify lead if present.

### 4.4 Mould remediation if wet insulation is found

Ontario has no standalone mould regulation, but mould work is governed by general OHSA worker-protection duties and is industry-standardized via the **EACO Mould Abatement Guidelines** (commonly referenced by insurers and BPS owners). Expect the contractor to scope mould remediation as a changed/extra condition if wet insulation is uncovered during tear-off; the tender should include a provisional allowance or unit rate for this.

---

## 5. Financial Capacity Indicators

### 5.1 Surety bonding — independent financial vetting

In Ontario, **bid bonds and performance bonds are mandatory on all publicly funded construction projects over $500,000** (under the *Construction Act* amendments). The common standard is:

- **Bid bond:** 10% of contract price (CCDC 220 form).
- **Performance bond:** 50% of contract price (CCDC 221 form).
- **Labour & Material Payment bond:** 50% of contract price (CCDC 222 form).

The **CCDC bond forms were updated in 2024** with tighter claim-response timelines and dispute-resolution provisions — check which edition is specified in the RFP.

A surety underwriter independently vets the contractor's financial statements, credit history, management experience, equipment capacity, and work-in-progress before issuing any bond. **If a surety will bond the contractor, a sophisticated third party has already cleared the firm's finances.** A pre-qualification letter from a surety is a strong indicator of financial solidity.

[Source: Surety Association of Canada — Bonds for Tendering; FCA — Contract Surety Bonds in Ontario]

### 5.2 Bonding capacity

- **Single-project limit:** Typically 10–20% of the firm's annual work program, or 5–10× working capital — surety-specific.
- **Aggregate limit:** Typically 2–3× single-project limit.
- A bidder whose bonding capacity is close to the tender value is stretched thin; a bidder well below their aggregate limit has headroom for change orders and warranty claims.

### 5.3 WSIB premium rate as a financial signal

A firm sitting significantly above its construction subclass rate has elevated claims costs → elevated premiums → margin pressure → financial risk. Under the Rate Framework, rates take up to several years to normalize, so an elevated rate often reflects systemic safety issues rather than a one-off incident.

### 5.4 Years in business

- **5+ years** is a reasonable floor for commercial roofing.
- **10+ years** for institutional / BPS work.
- Watch for "phoenix" companies — same principals, new corporate entity — used to shed judgment, warranty, or WSIB-premium liabilities. Cross-check directors via Ontario Business Registry.

### 5.5 References — similar-size projects in past 3 years

- At least 3 references for projects of similar scope, roofing system, and building type, completed in the past 3 years.
- Owner, consultant, and property-manager contacts — **not** the contractor's own subcontractors or suppliers (which are self-interested).
- Confirm references actually respond and are not affiliates of the bidder (see §6).

---

## 6. Red Flags in Contractor Qualifications

| # | Red flag | What it signals |
|---|---|---|
| 1 | **Expired or suspended WSIB clearance** | Premium arrears; hiring party inherits liability |
| 2 | **COI limits below RFP requirements** | Non-compliant bid; also signals undersized firm |
| 3 | **Named insured on COI ≠ bidder's legal entity** | Shell company, assignment issue, possible fraud |
| 4 | **No completed-operations coverage** | Post-install defect claims uncovered |
| 5 | **Hot-work, height, or pollution exclusions** on CGL | Core roofing exposures uninsured |
| 6 | **Ministry of Labour orders, charges, or convictions** in past 3 years | Documented safety failures. MOL orders are posted at workplaces and surfaced via OLRB appeals and POA prosecutions. Charges and convictions are searchable via Ontario Ministry of Labour news releases and court records |
| 7 | **CRCA / ORCA membership claimed but lapsed** | Misrepresentation; no industry peer accountability |
| 8 | **Manufacturer certification lapsed** | Voids or limits the manufacturer warranty (see §7) |
| 9 | **References won't respond or are affiliates** | Thin real track record |
| 10 | **Pattern of litigation** (search CanLII + Superior Court of Justice records) | Disputes over scope, quality, payment, or defects |
| 11 | **Subcontracting actual roofing to unnamed crews** | Quality control gap; labour/insurance risk transfer |
| 12 | **No DSA referenced** on pre-1990 building tender | OHSA s. 30 non-compliance by bidder (or by owner) |
| 13 | **No WAH certificates or expired WAH training** | O. Reg. 297/13 non-compliance |
| 14 | **Cannot produce current fall-protection inspection logs** | O. Reg. 213/91 / CSA Z259 non-compliance |

[Source: Ontario.ca — Guide to OHSA Enforcement (Part VIII); WSIB — Clearances FAQs]

---

## 7. Manufacturer Certifications (Ontario-active programs)

Manufacturer certifications are the de facto quality signal in a voluntary-trade province. They matter because the **manufacturer's extended system warranty** (typically 20–30 years for commercial systems) is conditional on installation by a certified contractor; a lapsed certification at install time voids the warranty, no matter what the contract says.

### 7.1 Residential

- **GAF Master Elite** — asphalt shingle. Approximately 2% of roofing contractors in North America qualify. Enables GAF's top-tier warranties (Golden Pledge, System Plus). Requires good-standing licensing, insurance, and training.
- **IKO ROOFPRO** — asphalt shingle. Two tiers: Select and Craftsman Premier. Unlocks IKO's Iron Clad Extended Protection Limited Warranty.

[Source: GAF — Why Choose a GAF Certified Roofer; IKO — ROOFPRO Program]

### 7.2 Commercial

- **Firestone / Holcim Elevate Red Shield & Platinum** — TPO, EPDM, mod-bit. Platinum is the top tier; enables longest extended warranties.
- **Soprema Sopra-Garantie / PAQ+S (Select)** — SBS-modified bitumen (torch-on). Soprema's program ensures crew training on current mod-bit membrane techniques and unlocks extended warranties.
- **Carlisle SynTec Authorized / Centurion** — TPO, EPDM, PVC single-ply.
- **Johns Manville Peak Advantage** — commercial single-ply and mod-bit systems.

[Source: Soprema Canada; GAF Canada; IKO North America]

### 7.3 Why it matters for tender evaluation

- **Verify certification is current at both bid date and expected install date.** Certifications lapse annually if training or volume requirements are not met.
- **Request the manufacturer-issued certificate number and expiry**, then verify with the manufacturer directly (most maintain a contractor locator or will confirm by email).
- **If the manufacturer's extended warranty is part of the deliverable**, the contract should make the warranty's issuance a condition of final payment — not just "best efforts."

---

## 8. Public Procurement (BPS) Additional Requirements

When the owner is a **municipality, school board, hospital, university, college, LHIN/Ontario Health entity, or other Broader Public Sector (BPS) organization**, additional rules apply beyond the standard Ontario construction contracting framework.

### 8.1 BPS Procurement Directive compliance

The **BPS Procurement Directive** (issued under the *Broader Public Sector Accountability Act, 2010*, most recently updated Feb 2024) governs procurement by BPS organizations. Requirements include:

- Open, fair, and transparent competitive process.
- Published tender notice (typically on the Ontario Tenders Portal or a designated BPS portal).
- Mandatory competitive procurement thresholds: typically $100K+ for goods/services, $100K+ for construction (threshold set by the organization but cannot exceed Directive ceilings).
- Conflict-of-interest and supplier-code-of-ethics compliance.
- Documented evaluation methodology defined before bids are opened.
- Contract award disclosure.

[Source: Ontario.ca — BPS Procurement Directive (Feb 2024); Supply Ontario — BPS Procurement Directive]

### 8.2 AODA — accessible customer service & integrated standards

Under the **Accessibility for Ontarians with Disabilities Act, 2005 (AODA)** and the **Integrated Accessibility Standards Regulation (O. Reg. 191/11)**:

- BPS procurement must **incorporate accessibility design, criteria, and features** when acquiring goods, services, or facilities.
- If accessibility cannot be accommodated, the reason must be **recorded and retained** with the procurement decision.
- Contractors providing services on behalf of BPS organizations must have trained their staff on **accessible customer service**.

[Source: O. Reg. 191/11; Ontario.ca — BPS Procurement Directive]

### 8.3 French-language accommodation

Under the **French Language Services Act**, BPS organizations serving **designated areas** (25 designated regions across Ontario) must provide services in French. Procurement documents, signage for public-facing work, and emergency contact protocols may require French-language capability from the contractor in designated areas. Check the owner's status under the Act before assuming English-only is acceptable.

### 8.4 Ontario/Canadian content preferences

Ontario and Canadian content preferences must comply with Canada's trade obligations — the **Canadian Free Trade Agreement (CFTA)** and the **Canada–European Union Comprehensive Economic and Trade Agreement (CETA)** prohibit most explicit local-content preferences above defined thresholds. In practice, BPS construction procurement is largely open to any qualified Canadian bidder; explicit Ontario-only preferences are rare and generally limited to below-threshold procurements. The 2024 "Buy Ontario" procurement directive signals a policy shift but operates within trade-agreement constraints.

[Source: Ontario.ca — Buy Ontario Procurement Directive]

---

## 9. Practical Evaluation Checklist (Summary)

For each bidder, confirm:

**Registration & insurance**
- [ ] WSIB clearance current (verified via clearances.wsib.ca, not just PDF)
- [ ] CGL COI shows correct named insured, owner as additional insured, limits meet RFP
- [ ] Completed-operations coverage explicitly included, tail ≥ warranty period
- [ ] No disqualifying exclusions (hot work, height, CPL)
- [ ] Umbrella/excess if contract limit > primary CGL

**Workforce**
- [ ] Named foreman holds C of Q 449A (Roofer)
- [ ] All on-site workers have current WAH training (O. Reg. 297/13, valid 3 years)
- [ ] Fall-protection equipment annual inspections documented (O. Reg. 213/91)

**Safety record**
- [ ] WSIB rate at or near subclass average (not several risk bands above)
- [ ] No MOL orders, charges, or convictions in past 3 years
- [ ] COR™ certified (preferred for BPS / institutional)

**Financial capacity**
- [ ] Bid bond (10%) and agreement-to-bond (performance 50%, L&M 50%) on CCDC 2024 forms
- [ ] Bonding capacity ≥ 2× tender value (aggregate)
- [ ] 5+ years in business under the same legal entity
- [ ] 3+ references from similar-scope projects in past 3 years (confirmed non-affiliate)

**Hazmat (pre-1990 buildings)**
- [ ] Owner provided DSA (OHSA s. 30) with tender
- [ ] Bidder's asbestos-abatement plan classifies tasks by Type 1/2/3 (O. Reg. 278/05)
- [ ] CPL coverage in place if designated substances present

**Warranty / certifications**
- [ ] Manufacturer certification current for the specified system
- [ ] Certification expiry extends past install date
- [ ] CRCA / ORCA membership verified if claimed

**Red-flag screen**
- [ ] Named insured matches bidder legal entity (no shell)
- [ ] No pattern of litigation (CanLII search)
- [ ] Roofing work performed by bidder's own certified crews, not unnamed subs

---

## Sources

All URLs accessed 2026-04-15.

**WSIB**
- [Clearance Certificate in Construction — WSIB Operational Policy Manual](https://www.wsib.ca/en/operational-policy-manual/clearance-certificate-construction)
- [Clearances — WSIB](https://www.wsib.ca/en/businesses/premiums-and-payment/clearances)
- [Clearances FAQs — WSIB](https://www.wsib.ca/en/clearancefaqs)
- [Get a clearance certificate](https://clearances.wsib.ca/Clearances/eclearance/start?lang=en)
- [Expanded compulsory coverage in the construction industry — WSIB](https://www.wsib.ca/en/businesses/registration-and-coverage/expanded-compulsory-coverage-construction-industry)
- [Rate Framework: Construction — WSIB](https://www.wsib.ca/en/rate-framework-construction)
- [2024 premium rates — WSIB](https://www.wsib.ca/en/2024premiumrates)
- [Understanding your rate — WSIB](https://www.wsib.ca/en/businesses/premiums-and-payment/understanding-your-rate)
- [WSIB: 2024 premium rates — AWCBC](https://awcbc.org/about-us/our-members/news/wsib-2024-premium-rates)
- [Mandatory WSIB coverage in construction — IHSA](https://www.ihsa.ca/pdfs/businessowners/mandatory_coverage_in_construction.pdf)

**Ontario OHSA & regulations**
- [Guide to the Occupational Health and Safety Act — Part VIII: Enforcement](https://www.ontario.ca/document/guide-occupational-health-and-safety-act/part-viii-enforcement)
- [Guide to Designated Substances in the Workplace](https://www.ontario.ca/document/guide-designated-substances-workplace/overview-regulation)
- [Guide to the Regulation Respecting Asbestos on Construction Projects (O. Reg. 278/05)](https://www.ontario.ca/document/guide-regulation-respecting-asbestos-construction-projects-and-buildings-and-repair)
- [O. Reg. 278/05 — Designated Substance — Asbestos on Construction Projects (CanLII)](https://www.canlii.org/en/on/laws/regu/o-reg-278-05/latest/o-reg-278-05.html)
- [O. Reg. 213/91 — Construction Projects (CanLII)](https://www.canlii.org/en/on/laws/regu/o-reg-213-91/latest/o-reg-213-91.html)
- [O. Reg. 297/13 — Occupational Health and Safety Awareness and Training (CanLII)](https://www.canlii.org/en/on/laws/regu/o-reg-297-13/latest/o-reg-297-13.html)
- [Training for working at heights — Ontario.ca](https://www.ontario.ca/page/training-working-heights)
- [Provider Standard for Working at Heights Training — Ontario.ca](https://www.ontario.ca/page/provider-standard-working-heights-training)
- [Achieve compliance on construction sites — fall prevention — Ontario.ca](https://www.ontario.ca/page/achieve-compliance-construction-sites-fall-prevention)

**Skilled Trades Ontario**
- [Roofer trade page — Skilled Trades Ontario](https://www.skilledtradesontario.ca/trade-information/roofer/)
- [Roofer (449A) 2024 Trade Report](https://www.skilledtradesontario.ca/wp-content/uploads/2025/05/roofer-449A_2024_en_TradeReport.html)
- [Certificate of Qualification — Skilled Trades Ontario](https://www.skilledtradesontario.ca/certification/certificate-of-qualification/)
- [Apprenticeship Programs Quick Facts Chart (Aug 2024)](https://www.skilledtradesontario.ca/wp-content/uploads/2024/09/Apprenticeship-Programs-Chart-EN-09.06.24.pdf)

**IHSA**
- [COR™ Certification — IHSA](https://www.ihsa.ca/COR/What_is_COR.aspx)
- [COR™ Program Guidelines — IHSA](https://www.ihsa.ca/pdfs/cor/cor-program-guidelines.pdf)
- [Personal Fall Protection — IHSA Health & Safety Manual Ch. 19](https://www.ihsa.ca/rtf/health_safety_manual/pdfs/equipment/fall_protection.pdf)
- [Designated Substances W130 — IHSA](https://www.ihsa.ca/pdfs/products/id/w130.pdf)

**BPS Procurement**
- [BPS Procurement Directive (Feb 2024) — Ontario.ca PDF](https://www.ontario.ca/files/2024-02/tbs-bps-procurement-directive-en-2024-02-08.pdf)
- [BPS Procurement Directive — Supply Ontario](https://www.doingbusiness.mgs.gov.on.ca/mbs/psb/psb.nsf/Attachments/BPSProcDir-eng/$FILE/BPSProcDir-eng.html)
- [BPS Procurement Directive Implementation Guidebook](https://www.doingbusiness.mgs.gov.on.ca/mbs/psb/psb.nsf/Attachments/BPSProc_procurement_implementation-eng/$FILE/bps_procurement_implementation.html)
- [Buy Ontario Procurement Directive](https://www.ontario.ca/page/buy-ontario-procurement-directive)

**Surety & bonds**
- [Bonds for Tendering — Surety Association of Canada](https://suretycanada.com/SAC/SAC/Surety-Bonds/Bonds-for-Tendering.aspx)
- [Contract Surety Bonds in Ontario — FCA Insurance](https://fcainsurance.com/contract-surety-bonds/)

**CGL insurance**
- [Commercial General Liability Insurance (Ontario) — ThinkInsure](https://www.thinkinsure.ca/business-insurance/commercial-general-liability-insurance)
- [CGL in Ontario — BrokerForce Insurance](https://brokerforce.ca/blog/commercial-general-liability-cgl-insurance-in-ontario/)
- [Who Needs Commercial General Liability Insurance — Surnet](https://surnet.net/who-needs-commercial-general-liability-insurance/)

**CRCA / manufacturer programs**
- [Canadian Roofing Contractors Association — Under One Roof](https://roofingcanada.com/)
- [CRCA Membership](https://roofingcanada.com/membership/become-a-member/)
- [Why Choose a GAF Certified Roofer (Canada)](https://www.gaf.ca/en-ca/plan-design/homeowner-education/choose-gaf-roofer)
- [IKO ROOFPRO Program](https://www.iko.com/na/roofpro-program/)

**Legal/enforcement commentary**
- [Bill 119 — What You Need To Know (Hicks Morley, 2012)](https://hicksmorley.com/2012/03/07/bill-119-what-you-need-to-know/)
- [Bill 119 takes effect January 1, 2013 — Stringer LLP](https://www.stringerllp.com/2012/05/24/bill-119-takes-effect-january-1-2013/)
- [Owners of Construction Projects as Employers Under OHSA — Hicks Morley, 2023](https://hicksmorley.com/2023/11/14/owners-of-construction-projects-are-employers-under-ontarios-ohsa-more-on-a-recent-ruling-of-the-supreme-court-of-canada/)

---

**Document control.** This file is reference material. Update annually or whenever any of the following change: WSIB clearance cycle, WSIB Rate Framework parameters, O. Reg. 278/05 / 213/91 / 297/13 amendments, BPS Procurement Directive reissue, CCDC bond form editions, manufacturer certification program changes.
