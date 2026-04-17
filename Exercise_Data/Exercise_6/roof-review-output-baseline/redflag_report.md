# Roof Replacement Tender — Red Flag Report

**Project:** 2550 Argentia Road, Mississauga, ON
**Owner:** Tenebrus Capital
**RFP:** TC-ROOF-2026-001
**Report date:** 2026-04-17T02:26:45.556388+00:00

---

## Executive Summary

- Bids received: 5
- Compliant after mandatory gates: 3
- Critical red flags: 15
- High-severity red flags: 26
- Medium / low: 22 / 5

---

## Stage 1 — Mandatory Gate Results

### Heritage Construction Group

| Gate | Result | Evidence |
|---|:---:|---|
| Wsib Clearance | ✅ pass | Bid §INSURANCE COVERAGE cites WSIB Account #7890123-45; attachments list 'WSIB Clearance Certificate' and 'WSIB Experience Rating Letter (0.81)'. RFP §5.1.1. |
| Cgl Insurance | ⚠️ clarify | Bid §INSURANCE COVERAGE: CGL $5,000,000 per occurrence — meets RFP §5.1.2 minimum. Bid does NOT explicitly state owner named as additional insured nor the completed-operations tail (RFP requires 2 yrs). COI attached per attachments list but not quoted. |
| Bid Bond | ✅ pass | RFP §9.2 requires 50% performance + 50% L&M bonds (no bid-bond % stated in RFP). Bid declares bonding capacity up to $5M per project — comfortably above $578k project value. Consent of surety not explicitly attached. |
| Working At Heights | ✅ pass | Bid §SAFETY PROGRAM: 'Fall protection training for all workers (updated annually)' and COR certification. RFP §5.1 / fixture 04 §3 (O. Reg. 297/13). |
| Addenda Acknowledgment | ⚠️ clarify | Bid does not contain a Form of Tender section explicitly acknowledging addenda. No addenda numbers cited. RFP mandatory per §5.1. |
| Non Collusion Declaration | ⚠️ clarify | No non-collusion declaration found in the bid body or the attachments list. RFP mandatory. |
| Site Visit | ✅ pass | Cover letter: 'We attended the mandatory site visit on March 25, 2026'. RFP §6.4 / §8.1. |
| Minimum Years In Business | ✅ pass | Cover letter: 'Founded in 2012' — 14 years in business as of 2026. Closing remarks: '14 years in business'. RFP §5.1.3 minimum 10 years. |
| Minimum Similar Projects | ✅ pass | Four references provided (Amazon 185k sqft 2024; Magnotta 92k sqft 2023; Prologis 145k sqft 2025; Apotex 78k sqft 2024). All are commercial roof replacements within last 5 years. RFP §5.1.4 minimum 3. |

**Stage 1 status:** COMPLIANT — advances to rated scoring

### Lakeside Roofing Inc.

| Gate | Result | Evidence |
|---|:---:|---|
| Wsib Clearance | ✅ pass | COI section + Attachments list: 'WSIB Account #1234567-89'; 'WSIB Clearance Certificate attached'. Online re-verification at clearances.wsib.ca will be added as a standard award condition by the recommendation memo step. |
| Cgl Insurance | ⚠️ clarify | Insurance section: 'Commercial General Liability: $5,000,000 per occurrence' — meets RFP §5.1.2 ($5M minimum). However, bid does not confirm (a) Tenebrus Capital is named as Additional Insured, (b) 2-year completed-operations tail, or (c) that 'Lakeside Roofing Inc.' is the named insured on the COI. RFP requires all three (rfp.mandatory_requirements). |
| Bonding | ❌ fail | RFP §9.2 requires 50% performance and 50% L&M bonds; while RFP does not set a bid bond percent, no bid bond, consent of surety, or declared bonding capacity appears in the submission. Attachments list contains no surety documents. |
| Working At Heights Training | ✅ pass | Safety Program section: 'Fall protection training for all workers.' Interpreted as confirmation of O. Reg. 297/13 WAH training per fixture 04 §3. |
| Addenda Acknowledgment | ⚠️ clarify | No Form of Tender or addenda acknowledgment section appears in the markdown submission. RFP requires explicit acknowledgment (rfp.mandatory_requirements.addenda_acknowledgment_required = true). |
| Non Collusion Declaration | ⚠️ clarify | No signed non-collusion declaration is reproduced in the bid markdown. Cover letter is signed by Tony Marchetti, President, but RFP requires a separate non-collusion declaration (rfp.mandatory_requirements.non_collusion_declaration_required = true). |
| Minimum Years In Business | ✅ pass | Cover letter: 'Lakeside Roofing has been serving the Greater Toronto Area for 12 years.' Exceeds RFP §5.1.3 10-year minimum. |
| Similar Project References | ⚠️ clarify | Three references provided (Maple Logistics 62k sqft 2024; Westpark Industrial 71k sqft 2023; Torque Distribution 55k sqft 2025) — all commercial low-slope and within last 5 yrs, meeting count = 3 per RFP §5.1.4. However, project values are not stated, so the comparable test (0.5x-2x subject value, roof-qualification-check Gate 8) cannot be confirmed. |
| Site Visit | ✅ pass | Cover letter: 'We attended the mandatory site visit on March 25, 2026.' Satisfies RFP §6.4 / §8.1. |

**Stage 1 status:** NON-COMPLIANT — excluded

### Metro Building Solutions Inc.

| Gate | Result | Evidence |
|---|:---:|---|
| Wsib Clearance | ⚠️ clarify | Attachments list 'WSIB Clearance Certificate' and 'WSIB Experience Rating Letter (1.12)'; WSIB Account #3456789-01 cited. No clearance date or good-standing text in bid body. |
| Cgl Insurance | ⚠️ clarify | CGL $5,000,000 per occurrence meets RFP §5.1.2 minimum. Cover letter does not state owner named as additional insured nor completed-operations tail years; COI attached per exhibit list but not quoted. |
| Bid Bond | ✅ pass | RFP §9.2 does not require a bid bond (bid_bond_percent = null; only 50% performance and 50% L&M bonds required). Bid contains no bid bond but none was required. |
| Working At Heights | ❌ fail | Safety Program section lists 'Written safety procedures' and 'Fall protection equipment provided' but does not confirm all on-site workers hold current O. Reg. 297/13 Working-at-Heights training. RFP §5.1 requires confirmation. |
| Addenda Acknowledgment | ⚠️ clarify | No addenda acknowledgment statement in the bid. Cover letter cites RFP number only. |
| Non Collusion | ⚠️ clarify | No non-collusion declaration text visible in bid; not listed in attachments. |
| Site Visit | ✅ pass | Cover letter: 'We attended the site visit on March 25, 2026.' RFP site_meeting_mandatory=true. |
| Years In Business | ✅ pass | 'operating in the Greater Toronto Area since 2010' (cover letter). 2026 - 2010 = 16 years, exceeds RFP §5.1.3 minimum of 10. |
| Similar Projects | ⚠️ clarify | Three references provided (Smallwood 2024 48k sqft, Valley View 2023 52k sqft, Eastgate 2025 67k sqft) — count meets RFP §5.1.4 minimum of 3. All within 5-year recency and commercial low-slope class. However, project values not disclosed — comparable test (0.5×-2× subject value) cannot be verified from bid alone. |

**Stage 1 status:** NON-COMPLIANT — excluded

### Pinnacle Roofing Corp.

| Gate | Result | Evidence |
|---|:---:|---|
| Wsib Clearance | ✅ pass | Attachments list includes 'WSIB Clearance Certificate' and 'WSIB Experience Rating Letter (0.89)'; §Insurance cites WSIB Account #5678901-23. No explicit clearance date stated in bid body — gate passed with standard award condition to re-verify on clearances.wsib.ca before contract signing (per roof-qualification-check SKILL.md §1). |
| Cgl Insurance | ⚠️ clarify | Bid §Insurance states 'Commercial General Liability: $5,000,000 per occurrence' meeting RFP §5.1.2 $5M minimum. Attachments include Certificate of Insurance. However bid does NOT confirm (a) owner named as additional insured, or (b) 2-year completed-operations tail — both mandatory per RFP §5.1.2. |
| Bonding | ✅ pass | RFP mandatories show no bid_bond_percent required (rfp.mandatory_requirements.bid_bond_percent=null; confirmed in extraction_notes: 'No bid bond percentage stated in §9.2'). Performance + L&M bonds at 50% are post-award obligations. Bid does not declare bonding capacity, but that is not a mandatory gate per this RFP. |
| Working At Heights Training | ✅ pass | §Safety Program: 'Fall protection training for all workers (updated every 2 years)'. RFP §5.1 working_at_heights_training_required=true. |
| Addenda Acknowledgment | ⚠️ clarify | Bid does not explicitly list addenda acknowledged. Cover letter states 'carefully reviewed all RFP documents' but no Form of Tender addenda list is provided. RFP §5.1 addenda_acknowledgment_required=true. |
| Non Collusion Declaration | ⚠️ clarify | Bid is signed by Robert K. Thompson, President, but no separate non-collusion declaration is attached or referenced. RFP §5.1 non_collusion_declaration_required=true. |
| Site Visit | ✅ pass | Cover letter: 'We attended the mandatory site visit on March 25, 2026'. RFP §6.4/§8.1 site_visit_required=true. |
| Minimum Years In Business | ✅ pass | Cover letter: 'Established in 2008' → 18 years at time of bid. RFP §5.1.3 requires minimum 10 years. |
| Similar Project References | ✅ pass | Three references provided (Canadian Tire Distribution Centre Concord 95,000 sqft 2024; Loblaws Head Office Brampton 78,000 sqft 2023; Tim Hortons Supply Chain Oakville 62,000 sqft 2025). All three are commercial (Part 3 class), all roof replacements on occupied buildings, all within last 5 years. Project values not stated but scale (62-95k sqft) is within 0.5-2x of subject 85k sqft. Count of comparable ≥ 3 per RFP §5.1.4. |

**Stage 1 status:** COMPLIANT — advances to rated scoring

### Summit Contracting Ltd.

| Gate | Result | Evidence |
|---|:---:|---|
| Wsib Clearance | ⚠️ clarify | WSIB Clearance Certificate listed in attachments (bid Attachments section); date of issue not cited in cover letter; 'in good standing' language not quoted. RFP §5.1.1 / mandatory_requirements.wsib_clearance_required. |
| Cgl Insurance | ⚠️ clarify | CGL $10,000,000 per occurrence (exceeds RFP §5.1.2 minimum $5M). Certificate of Insurance listed in attachments. Owner-named-as-additional-insured and completed-operations tail years NOT confirmed in cover letter text. |
| Bonding | ⚠️ clarify | RFP mandatory_requirements specifies performance_bond_percent=50 and labour_material_bond_percent=50 (§9.2); bid_bond_percent is null (not required). Summit bid does not mention performance/L&M bonds or surety consent in cover letter or attachments list. |
| Working At Heights | ✅ pass | Safety Program section: 'Fall protection training for all workers (updated annually).' COR certified; CRSP-certified safety officer on-site. Fixture 04 §3 / RFP mandatory_requirements.working_at_heights_training_required. |
| Addenda Acknowledgment | ⚠️ clarify | Cover letter does not list acknowledgment of any RFP addenda. No Form of Tender with addenda section included in the bid text. RFP mandatory_requirements.addenda_acknowledgment_required = true. |
| Non Collusion Declaration | ⚠️ clarify | Cover letter signed by Michael Chen, P.Eng., VP Sales & Engineering. No explicit non-collusion declaration quoted or listed in attachments. |
| Minimum Years In Business | ✅ pass | Cover letter: 'For over 25 years, we have been serving the GTA.' RFP §5.1.3 / mandatory_requirements.minimum_years_in_business = 10. |
| Similar Project References | ✅ pass | Four commercial references provided, all occupied/similar scope, completed 2022-2025: Maple Leaf Foods (125k sf, 2023), Shoppers DC (210k sf, 2022), Magnotta Winery (68k sf, 2024), Pfizer Canada (95k sf, 2025). RFP §5.1.4 / mandatory_requirements.minimum_similar_projects = 3. |
| Site Visit | ✅ pass | Cover letter: 'We attended the mandatory site visit on March 25, 2026.' RFP §6.4/§8.1 mandatory site visit. |

**Stage 1 status:** COMPLIANT — advances to rated scoring

---

## Stage 2 — Qualitative Red Flags

### Heritage Construction Group

**[CRITICAL] Warranty — RFP requires total_system_ndl warranty; bid offers '20-year NDL warranty on TPO membrane' — appears to be a membrane-scope NDL, not a total-system NDL covering the full assembly (insulation, flashings, labour). A specific manufacturer system-warranty program is not named for the base bid.**
- Citation: RFP §3.1 / §9.6 warranty_type_required = total_system_ndl; fixture 02 §1 & §4.5
- Evidence: Bid §WARRANTY (BASE BID): 'Manufacturer Warranty: 20-year NDL warranty on TPO membrane'. No named Platinum/Red Shield/Sopra-Garantie Mammouth program attached for base bid.
- Recommended action: clarify

**[CRITICAL] Substitutions — VE Option 5 removes cover board from a TPO-over-polyiso assembly. Removing the cover board over polyiso voids most manufacturer system warranties and creates a long-term performance defect (board-joint telegraphing, membrane puncture). Contractor's blanket claim that 'mechanically attached does not require cover board per Carlisle and Firestone' is not supported by current manufacturer guidelines for system-warranted assemblies.**
- Citation: fixture 02 §4 cover board requirement; CRCA best practice
- Evidence: Bid VE Option 5: 'Remove cover board (not required with mechanically attached assembly per manufacturer)'.
- Recommended action: reject

**[HIGH] Qualifications — CGL coverage: owner-as-additional-insured endorsement and 2-year completed-operations tail not explicitly confirmed in bid narrative.**
- Citation: RFP §5.1.2; fixture 04 §2
- Evidence: Bid §INSURANCE COVERAGE lists CGL $5M but is silent on additional-insured endorsement and completed-ops years.
- Recommended action: clarify

**[HIGH] Qualifications — Addenda acknowledgment and non-collusion declaration not evidenced in the submitted bid text.**
- Citation: RFP §5.1; CCDC 23 guidance (fixture 03)
- Evidence: Neither item appears in the bid narrative nor in the attachments list.
- Recommended action: clarify

**[HIGH] Warranty — Workmanship warranty is 2 years — meets RFP minimum but below market median of 5 years for a complex occupied pharma-warehouse project with 47 penetrations.**
- Citation: fixture 02 §3; RFP §9.6 minimum 2 yrs
- Evidence: Bid §WARRANTY: 'Workmanship Warranty: 2 years on installation'.
- Recommended action: negotiate

**[HIGH] Materials — Specific membrane manufacturer for the base bid is not named. Contractor lists three certifications (Carlisle, Firestone, GAF) but does not commit to a single product data line for the 60 mil TPO.**
- Citation: fixture 02 §4 mis-matched components voids system warranty
- Evidence: Bid §MANUFACTURER CERTIFICATIONS lists three; base bid section does not name the manufacturer to be installed.
- Recommended action: clarify

**[HIGH] Safety — Wind-uplift design basis (CSA A123.21 or FM 1-29) not stated anywhere in the bid. Single-ply commercial roof, 28 ft, with 47 penetrations requires an explicit uplift design reference.**
- Citation: fixture 01 §1.2; CSA A123.21
- Evidence: Bid narrative discusses mechanically-attached vs adhered trade-off under VE Option 1 but never cites a wind-uplift design standard.
- Recommended action: clarify

**[HIGH] Safety — Fall-protection approach is stated generically (COR, WAH training, safety coordinator) but no site-specific plan naming anchor points, parapet/perimeter detail, or CSA Z91 anchor compliance is provided.**
- Citation: fixture 01 §3; CSA Z91
- Evidence: Bid §SAFETY PROGRAM describes program-level commitments only.
- Recommended action: clarify

**[MEDIUM] Qualifications — Reference project values not stated; comparability by 0.5×-2× subject-value test cannot be confirmed.**
- Citation: roof-qualification-check Gate 8; fixture 04 §1
- Evidence: Bid §REFERENCES lists four projects with sqft but omits contract value.
- Recommended action: clarify

**[MEDIUM] Substitutions — VE Option 1 (mechanically attached) proposed as 'ACCEPTABLE' but equivalence justification is thin — site-specific wind uplift design is not provided, and Ontario TPO wind-event losses correlate with mech-attached systems.**
- Citation: fixture 02 §1; fixture 01 §1.2
- Evidence: Bid VE Option 1: 'wind uplift risk is moderate. Mechanically attached systems are widely used in similar applications.'
- Recommended action: clarify

**[MEDIUM] Scope — Bid excludes 'work outside standard hours (7 AM - 6 PM weekdays)' — but also commits to 72-hr weekend HVAC shutdowns. Ambiguity about premium for any after-hours or weekend roofing labour that the phasing plan may require.**
- Citation: RFP §11.1 occupied-site phasing; RFP §1.2
- Evidence: Bid §EXCLUSIONS item 6 vs §PHASING PLAN weekend protection + §CLARIFICATIONS item 5.
- Recommended action: clarify

**[MEDIUM] Scope — Crew size not stated and mobilization-days-after-award not stated; 90-day duration on 85,000 sqft occupied building with three phases depends on crew resourcing that is not quantified.**
- Citation: RFP §4 schedule; roof-qualification-check schedule sub-factor
- Evidence: Bid §PROJECT TEAM lists PM/Supervisor/Safety/4 installers but does not specify total crew deployed.
- Recommended action: clarify

**[LOW] Scope — Bid explicitly excludes replacement of damaged roof drains or leaders; RFP scope included 'tapered insulation or added drains' to resolve ponding. Potential scope gap if drain addition becomes the preferred ponding-correction path.**
- Citation: RFP §3 scope included_items
- Evidence: Bid §EXCLUSIONS item 3 vs RFP included_items 'Tapered insulation or added drains'.
- Recommended action: clarify

### Lakeside Roofing Inc.

**[CRITICAL] Materials — 45 mil TPO proposed where RFP specifies 60 mil minimum — below commercial single-ply industry minimum.**
- Citation: RFP §3.1 '60 mil minimum'; fixture 02 §1 (60 mil is commercial TPO minimum)
- Evidence: Key Specifications: 'Membrane: 45 mil TPO, mechanically attached'; Price Breakdown: 'TPO membrane (45 mil) $145,000'
- Recommended action: reject

**[CRITICAL] Materials — No cover board included over polyiso insulation. Missing cover board is a critical defect for commercial TPO over polyiso and voids most manufacturer system warranties.**
- Citation: Fixture 02 §4 (missing cover board = critical red flag); RFP included_items '1/4 inch gypsum or HD polyiso cover board'
- Evidence: Price Breakdown has no cover board line; Key Specifications list only membrane, insulation, attachment; contractor does not mention cover board anywhere.
- Recommended action: reject

**[CRITICAL] Warranty — 15-year material-only warranty offered vs RFP-required 20-year total-system NDL. Shortfall on both duration (15<20) and tier (material_only vs total_system_ndl).**
- Citation: RFP §3.1, §9.6 (20-year minimum, total-system NDL); fixture 02 §1 and §4.5 warranty taxonomy
- Evidence: Warranty section: 'Manufacturer Warranty: 15-year limited warranty on TPO membrane'; Attachments list: 'Sample 15-Year Warranty Documentation'.
- Recommended action: reject

**[CRITICAL] Scope — Mechanically attached system proposed where RFP specifies fully-adhered attachment. Change in attachment method materially alters wind-uplift performance and voids the specified system.**
- Citation: RFP §3.1 'Fully adhered system preferred' (manifest membrane_system_specified.attachment_method = 'fully_adhered')
- Evidence: Key Specifications: 'Attachment: Mechanically attached system'; Additional Notes: 'We use efficient mechanically attached systems that reduce installation time and cost.'
- Recommended action: reject

**[CRITICAL] Scope — Ponding correction (tapered insulation or added drains) deleted from base bid and offered only as an upgrade; contractor disputes RFP ponding finding on self-assessment.**
- Citation: RFP included_items 'Tapered insulation or added drains to resolve ponding'
- Evidence: Exclusion #10: 'Tapered insulation for ponding correction - available as upgrade'; Additional Notes: 'our inspection did not confirm significant ponding... proceeding with standard installation'.
- Recommended action: reject

**[CRITICAL] Safety — Temporary weather protection for incomplete phases explicitly excluded on an occupied 85,000 sqft pharma-warehouse with phased tear-off. Creates water-ingress hazard to occupants and products.**
- Citation: RFP §3.1 phasing 'watertight at EOD'; fixture 01 §3 (site safety on occupied buildings)
- Evidence: Exclusion #12: 'Temporary weather protection for incomplete phases'.
- Recommended action: reject

**[HIGH] Safety — No site-specific fall protection / anchor plan provided; only a generic 'fall protection training' statement. Occupied commercial roof requires CSA Z91 anchor plan and parapet strategy.**
- Citation: Fixture 01 §3; O. Reg. 297/13; CSA Z91
- Evidence: Safety Program section lists training and weekly meetings only; no site safety plan attached (Attachments list).
- Recommended action: clarify

**[HIGH] Materials — Wind uplift design basis not stated. Commercial low-slope TPO with mechanical attachment on a 28-year-old deck requires documented CSA A123.21 or FM 1-29 design.**
- Citation: Fixture 01 §1.2; CSA A123.21
- Evidence: No wind uplift design reference anywhere in the bid; product data sheets listed but no design calcs.
- Recommended action: clarify

**[HIGH] Scope — Single-layer R-30 polyiso proposed vs RFP-specified two staggered layers. Single-layer stacks create thermal bridging at butt joints and may not satisfy SB-10 effective R-value at seams.**
- Citation: Fixture 01 §1.3 (SB-10 effective R-value); RFP included_items 'R-30 polyiso in two staggered layers'
- Evidence: Key Specifications: 'Insulation: Polyisocyanurate, R-30 (single layer to meet code minimum)'; Additional Notes: 'Single-layer insulation meets code requirements while minimizing material costs.'
- Recommended action: reject

**[HIGH] Scope — After-hours HVAC coordination and temperature monitoring excluded on an occupied pharma-warehouse that requires 72-hour HVAC shutdown coordination per RFP.**
- Citation: RFP included_items 'HVAC temporary protection, 72-hr shutdown coordination'
- Evidence: Exclusions #13 'Temperature monitoring of warehouse during construction' and #14 'After-hours HVAC coordination'.
- Recommended action: clarify

**[HIGH] Warranty — No manufacturer named and no certified installer program declared. 20-yr NDL system warranties require certified installer status at the named tier (e.g., Soprema PAQ+S, Firestone Red Shield Platinum, GAF Master Elite).**
- Citation: Fixture 02 §3 certified installer programs
- Evidence: Materials section names no manufacturer; attachments list does not include a manufacturer certification letter.
- Recommended action: clarify

**[HIGH] Qualifications — No bid bond, consent of surety, or declared bonding capacity. RFP §9.2 requires 50% performance and 50% L&M bonds; bid should include surety consent.**
- Citation: RFP §9.2; fixture 04 §5 (bonding capacity)
- Evidence: Attachments list contains no surety documents; no bonding capacity stated anywhere.
- Recommended action: clarify

**[MEDIUM] Qualifications — COI does not confirm Tenebrus Capital named as Additional Insured or 2-year completed-operations tail; named insured entity on COI not verified against bidder legal name.**
- Citation: RFP mandatory_requirements.owner_named_additional_insured / completed_operations_years; fixture 04 §2 and §5
- Evidence: Insurance section lists $5M CGL only; no AI endorsement or completed-ops language reproduced in submission.
- Recommended action: clarify

**[MEDIUM] Qualifications — No subcontracting disclosure. RFP projects of this scope typically require declaration of whether roofing crew is in-house or sub'd, and naming of key subs. Undisclosed sub-trades on the actual roofing crew is a fixture 04 §5 shell-company signal.**
- Citation: Fixture 04 §5
- Evidence: No subcontractor list in the bid.
- Recommended action: clarify

**[MEDIUM] Qualifications — Reference project values not provided; comparable-reference test (0.5x-2x subject value, last 5 yrs, same building class) cannot be fully evaluated.**
- Citation: roof-qualification-check Gate 8
- Evidence: References section lists square footage and year but not contract value.
- Recommended action: clarify

**[MEDIUM] Qualifications — Non-collusion declaration and addenda acknowledgment not reproduced in submission. RFP requires both as mandatory.**
- Citation: RFP mandatory_requirements.non_collusion_declaration_required / addenda_acknowledgment_required; fixture 03
- Evidence: Markdown submission contains cover letter signed by president but no separate non-collusion form or addenda acknowledgment page.
- Recommended action: clarify

### Metro Building Solutions Inc.

**[CRITICAL] Scope — Base bid excludes cover board — directly contradicts RFP included scope (§3.1 cover board required) and voids TPO manufacturer warranty over polyiso assemblies.**
- Citation: RFP §3.1 / fixture 02 §4 — cover board required over polyiso for single-ply system warranty
- Evidence: Cover letter Exclusion #4: 'Cover board - Not included in base bid. Optional upgrade at $38,000.'
- Recommended action: reject

**[CRITICAL] Substitutions — Mechanically attached TPO proposed in lieu of RFP-specified fully-adhered system. No manufacturer approval or wind-uplift calculation provided; equivalence justification is unsupported assertion.**
- Citation: RFP §3.1 attachment_method=fully_adhered / fixture 02 §1
- Evidence: Key Specifications: 'Mechanically attached system.' Assumption #15: 'Mechanically attached system acceptable (equivalent to fully adhered for this application).'
- Recommended action: reject

**[CRITICAL] Scope — Tapered insulation / ponding resolution excluded; contractor dismisses ponding as 'superficial' — direct contradiction of RFP included_items requiring ponding resolution.**
- Citation: RFP §3.1 included_items 'Tapered insulation or added drains to resolve ponding'
- Evidence: Exclusion #5 and Additional Notes: 'Ponding water is common on roofs of this age and does not necessarily indicate failure.'
- Recommended action: reject

**[CRITICAL] Warranty — Warranty is 20-year manufacturer 'limited' on membrane only — material_only tier, not the total_system_ndl required. Workmanship warranty only 1 year vs RFP §9.6 minimum 2 years. No manufacturer-certified-installer status declared.**
- Citation: RFP warranty_requirements (20 yr total_system_ndl, 2 yr workmanship, manufacturer certification required) / fixture 02 §1 warranty taxonomy
- Evidence: Warranty section: 'Manufacturer Warranty: 20-year limited warranty on TPO membrane. Workmanship Warranty: 1 year on installation.'
- Recommended action: reject

**[CRITICAL] Safety — Working-at-Heights training (O. Reg. 297/13) not explicitly confirmed; only generic 'Fall protection equipment provided.' Fails RFP mandatory gate.**
- Citation: RFP §5.1 / O. Reg. 297/13 / fixture 04 §3
- Evidence: Safety Program section — no WAH training statement.
- Recommended action: clarify

**[CRITICAL] Materials — Assumption #5 ('Building will be vacated or operations can continue normally during work') directly contradicts RFP project.occupied_during_work=true and §11.1 phased occupied pharma warehouse requirement. No phasing plan submitted.**
- Citation: RFP §1.2 / §11.1 / scope_of_work work_description (max 15,000 sqft exposed)
- Evidence: Clarifications & Assumptions #5 and #12
- Recommended action: reject

**[HIGH] Scope — Skylight count discrepancy: RFP specifies 12 skylights; bidder 'counted 4 during site visit' and prices work only for 4. Any replacement beyond 4 billed at $4,800/skylight as extra.**
- Citation: RFP scope / flashings at 47 penetrations
- Evidence: Exclusion #8
- Recommended action: clarify

**[HIGH] Scope — 25+ listed exclusions and open-ended cost adjusters (material escalation, waste-fee escalation, temperature monitoring, weekend weather protection) transfer price risk to owner and undermine bid comparability.**
- Citation: fixture 03 §5 — low-ball base-bid pattern
- Evidence: Cover letter 'IMPORTANT EXCLUSIONS' list (25 items) + final NOTE TO BIDDER warning at bid foot.
- Recommended action: negotiate

**[HIGH] Qualifications — WSIB Experience Rating 1.12 is above industry average (1.00 baseline) — financial/claims-history signal per fixture 04 §5. Warrants review of 3-year claims history before award.**
- Citation: fixture 04 §5 — WSIB experience rating signal
- Evidence: Safety Program section: 'WSIB Experience Rating: 1.12'
- Recommended action: clarify

**[HIGH] Qualifications — No manufacturer certification (GAF Master Elite, Soprema PAQ+S, Firestone Red Shield, Sika Sarnafil, etc.) declared; TPO system manufacturer itself not named in bid body. RFP manufacturer_certification_required=true.**
- Citation: RFP warranty_requirements.manufacturer_certification_required / fixture 02 §3
- Evidence: No certification program cited anywhere in bid; TPO manufacturer omitted from Key Specifications.
- Recommended action: reject

**[HIGH] Qualifications — Reference project values not disclosed — comparability (0.5×-2× of $468k subject value) cannot be verified. All three references are commercial low-slope within 5 years (positive signal), but Smallwood at 48k sqft and Valley View at 52k sqft are materially smaller than the 85k sqft subject roof.**
- Citation: fixture 03 — reference comparability / Gate 8 definition
- Evidence: References section lists name, location, sqft, contact but no project value.
- Recommended action: clarify

**[HIGH] Safety — No fall-protection plan, anchor-point strategy, weather-protection plan, tear-off staging plan, or site-safety plan attached. Occupied pharma warehouse with 47 penetrations demands a specific plan.**
- Citation: fixture 01 §3 / CSA Z91 / OBC occupied-building precautions
- Evidence: Technical approach sections absent; cover letter contains only generic statements.
- Recommended action: reject

**[HIGH] Materials — Wind-uplift design basis (CSA A123.21 or FM 1-29) not stated — required for commercial low-slope, especially when attachment method is being substituted to mechanically fastened.**
- Citation: fixture 01 §1.2 — commercial low-slope wind-uplift design
- Evidence: Key Specifications omits wind-uplift figures; no wind_uplift_coverage_mph claimed in warranty.
- Recommended action: clarify

**[MEDIUM] Scope — Front-loaded payment schedule (20% mobilization + 30% progress + 30% substantial + 10% holdback) concentrates owner risk. Construction Act holdback respected, but 20% mobilization is above GTA commercial norm (~10%).**
- Citation: Construction Act / fixture 03 §6 payment norms
- Evidence: Payment Schedule section and note 'We require larger upfront payment due to material procurement costs.'
- Recommended action: negotiate

**[MEDIUM] Warranty — Bid does not identify TPO manufacturer — impossible to confirm warranty eligibility or manufacturer acceptable-list fit.**
- Citation: fixture 02 §4 — named-manufacturer requirement
- Evidence: Key Specifications: '60 mil TPO' (no manufacturer).
- Recommended action: clarify

### Pinnacle Roofing Corp.

**[CRITICAL] Warranty — Warranty type claimed is 20-year NDL but the RFP requires total_system_ndl. Bid does not attach a named system-warranty program (e.g., Carlisle Syntec Golden Seal/Sure-Weld Total System, Firestone Red Shield Platinum, Johns Manville Peak Advantage System NDL). 'NDL' alone covers materials only without the labour + full assembly coverage the owner specified.**
- Citation: RFP §3.1/§9.6 warranty_type_required=total_system_ndl; fixture 02 §1 and §4.5
- Evidence: Cover letter §Warranty: '20-year NDL (No Dollar Limit) warranty on TPO membrane'; Attachments: '20-Year NDL Warranty Sample Documentation' (membrane-scope language only, not system)
- Recommended action: clarify

**[HIGH] Qualifications — COI confirmation gap: bid does not state owner is named additional insured or confirm 2-year completed-operations tail**
- Citation: RFP §5.1.2; fixture 04 §2
- Evidence: §Insurance: 'Commercial General Liability: $5,000,000 per occurrence' — no mention of additional-insured endorsement or completed-ops years
- Recommended action: clarify

**[HIGH] Materials — Membrane manufacturer not specified in bid. Bidder lists three manufacturer certifications (Carlisle, Firestone, Johns Manville) but does not commit to which manufacturer's system will be installed. Manufacturer choice determines warranty program, wind-uplift rating, component compatibility, and installer tier requirement.**
- Citation: fixture 02 §3 and §4
- Evidence: §Materials System / Manufacturer Certifications list multiple brands with no commitment. No named product line on product data sheets reference.
- Recommended action: clarify

**[HIGH] Materials — Wind uplift design basis not stated. Commercial low-slope retrofit should state CSA A123.21 or FM 1-29 design basis for fully-adhered TPO on a 28-year-old deck (steel + wood sections).**
- Citation: fixture 01 §1.2 (OBC Part 3 wind uplift); CSA A123.21
- Evidence: §Key Specifications lists 'Fully adhered' attachment but no uplift-test basis. Solar reflectance and thickness given; uplift rating omitted.
- Recommended action: clarify

**[HIGH] Safety — Fall protection plan is generic. No named anchor points, no parapet-specific tie-off vs guardrail strategy on a 85,000 sqft occupied-building roof with 47 penetrations.**
- Citation: fixture 01 §3; CSA Z91; O. Reg. 213/91 + O. Reg. 297/13
- Evidence: §Safety Program: 'Fall protection training for all workers... Weekly safety meetings'. No site-specific plan describing anchor layout, rescue plan, or perimeter controls.
- Recommended action: clarify

**[MEDIUM] Qualifications — Addenda acknowledgment not explicitly listed in bid**
- Citation: RFP §5.1; CCDC 23 guidance (fixture 03)
- Evidence: No Form of Tender addenda table in submission
- Recommended action: clarify

**[MEDIUM] Qualifications — Non-collusion declaration not attached or referenced**
- Citation: RFP §5.1 non_collusion_declaration_required=true
- Evidence: Cover letter signed by President but no standalone declaration form evident
- Recommended action: clarify

**[MEDIUM] Qualifications — Reference project dollar values not disclosed, preventing full 0.5x-2x comparability check**
- Citation: fixture 03 tender evaluation; roof-qualification-check Gate 8
- Evidence: References list square footage and contact but no contract value
- Recommended action: clarify

**[MEDIUM] Scope — Exclusion: 'Replacement of damaged roof drains or leaders' — RFP §scope references 'added drains to resolve ponding' as part of included work. Bid covers tapered insulation for ponding but excludes drain replacement, creating a scope-gap risk if drains are found damaged during tear-off.**
- Citation: RFP §3 scope_of_work included_items
- Evidence: §Exclusions item 3: 'Replacement of damaged roof drains or leaders (minor adjustments included)'
- Recommended action: negotiate

**[MEDIUM] Scope — Working-hours exclusion (7 AM-6 PM weekdays only). RFP occupied pharma-warehouse with 72-hr HVAC shutdown coordination may require weekend work; Pinnacle excludes out-of-hours work and assumes weekend HVAC-shutdown scheduling at no cost — contradictory assumption that could yield change orders.**
- Citation: RFP §1.2/§11 occupied-site requirements
- Evidence: §Exclusions item 6 vs §Clarifications item 5
- Recommended action: clarify

**[MEDIUM] Scope — Permits excluded. RFP does not explicitly say bidder must carry permits, but pricing transparency expects inclusion or a stated carried amount. Pinnacle puts the $4,500-$6,000 estimate on the owner.**
- Citation: fixture 03 tender evaluation
- Evidence: §Exclusions item 9: 'Building permits (estimated $4,500-$6,000)'
- Recommended action: clarify

**[MEDIUM] Scope — Hazmat handling scope ambiguous — 'Minor ACM handling included; major abatement would be extra' without defining the threshold. Building is post-1980 so ACM is unlikely, but owner should fix the boundary.**
- Citation: O. Reg. 278/05; fixture 01 §4
- Evidence: §Hazardous Materials Approach and §Exclusions item 7
- Recommended action: clarify

**[LOW] Qualifications — Skilled Trades C of Q holder count not disclosed for roofing crew**
- Citation: fixture 04 §4
- Evidence: §Project Team names PM and Site Supervisor; 'Lead Installers: 3 certified roofing technicians' without C of Q specifics
- Recommended action: clarify

**[LOW] Materials — Flashing material spec 'Aluminum' differs from some manufacturer system-warranty requirements that call for galvanized steel at specific details. Depends on final manufacturer selection.**
- Citation: fixture 02 §4
- Evidence: §Key Specifications 'Flashing Material: Aluminum'
- Recommended action: clarify

### Summit Contracting Ltd.

**[HIGH] Qualifications — Performance and L&M bonds (50% each, RFP §9.2) not addressed in bid; no surety consent or bonding capacity declared**
- Citation: RFP §9.2 / rfp.mandatory_requirements.performance_bond_percent; fixture 04 §5 (bonding capacity as financial-capacity signal)
- Evidence: Bid attachments list and cover letter make no reference to performance bond, L&M bond, or surety consent. CGL/WSIB/COR are addressed; bonding is silent.
- Recommended action: clarify

**[HIGH] Qualifications — Addenda acknowledgment absent; non-collusion declaration absent from bid documentation**
- Citation: RFP mandatory_requirements (addenda_acknowledgment_required, non_collusion_declaration_required); CCDC 23 §5 (fixture 03)
- Evidence: No Form of Tender text quoted; cover letter does not list addenda acknowledged or a signed non-collusion declaration.
- Recommended action: clarify

**[HIGH] Safety — Contractor proposes to self-perform 'minor ACM' abatement under existing certification without specifying Type 1/2/3 designation**
- Citation: O. Reg. 278/05 (Asbestos on Construction Projects); fixture 01 §4; RFP §2.3
- Evidence: Hazardous Materials Approach §2: 'If ACM confirmed: We hold appropriate licensing for limited abatement. Full abatement would be extra, but minor ACM can be handled under our existing certification.' The specific Type (1/2/3) and licensed supervisor credentials are not cited.
- Recommended action: clarify

**[MEDIUM] Qualifications — CGL completed-operations years and owner-named-additional-insured not textually confirmed**
- Citation: RFP §5.1.2 / mandatory_requirements.cgl_minimum_cad + completed_operations_years; fixture 04 §2
- Evidence: Cover letter cites $10M CGL limit but does not quote completed-ops tail length or owner additional-insured endorsement. COI is attached but not rendered in the bid text.
- Recommended action: clarify

**[MEDIUM] Qualifications — WSIB clearance date and 'in good standing' language not quoted; WSIB Experience Rating of 0.72 is favorable (below industry average)**
- Citation: Fixture 04 §1.3 (90-day validity window) and §1.4 (online verifier is authoritative)
- Evidence: Cover letter Attachments list shows 'WSIB Clearance Certificate' and 'WSIB Experience Rating Letter (0.72)' but validity date and good-standing text not reproduced in cover letter.
- Recommended action: clarify

**[MEDIUM] Safety — Fall-protection plan references annual training and CRSP safety officer but does not identify site-specific anchor points, CSA Z91-compliant tie-off locations, or parapet strategy**
- Citation: CSA Z91 (fall protection); fixture 01 §3
- Evidence: Cover letter Safety Program lists generic compliance statements (COR, annual training, tailgate meetings) without site-specific fall-arrest engineering for a 47-penetration, multi-level roof.
- Recommended action: clarify

**[MEDIUM] Warranty — Wind-uplift coverage stated as '130 mph' but design basis (CSA A123.21 or FM 1-29) not identified**
- Citation: Fixture 01 §1.2 (wind uplift design basis required on commercial low-slope); fixture 02 §4
- Evidence: Warranty section: 'Wind Warranty: Up to 130 mph wind speed coverage.' No reference to CSA A123.21 pull-test basis or FM 1-29 classification.
- Recommended action: clarify

**[MEDIUM] Materials — Membrane manufacturer for the proposed 80-mil TPO system not explicitly named in the cover letter**
- Citation: Fixture 02 §1 (system-level warranty is manufacturer-specific); RFP §3.1
- Evidence: Manufacturer Certifications lists Carlisle Syntec, Firestone, GAF, but the cover letter does not tie the 80-mil TPO product data sheet to a specific manufacturer/system line. Attachments include 'Product Data Sheets (80 mil TPO membrane)' but the manufacturer is not named in the narrative.
- Recommended action: clarify

**[LOW] Warranty — Contractor-offered '10-year ponding warranty' is not a standard manufacturer warranty product and may overlap/conflict with the manufacturer NDL exclusions for ponding**
- Citation: Fixture 02 §1 (ponding voids most manufacturer warranties); fixture 02 §4.5
- Evidence: Warranty section lists '10-year warranty against ponding water recurrence' as if separate from the 30-yr NDL. Contractor-provided coverage survives only as long as contractor survives; may be marketing gloss on workmanship warranty.
- Recommended action: clarify

**[LOW] Scope — Base bid includes a $15,000 'contingency allowance for unknown conditions' embedded in price**
- Citation: CCDC 2 (contingency handling); fixture 03 §4
- Evidence: Price Breakdown line: 'Contingency allowance for unknown conditions $15,000.' Typical practice is to carry contingency as a separate stated allowance, not inside the lump sum, so unspent contingency credits back to owner.
- Recommended action: negotiate

---

## Cross-Bid Patterns

- **Price spread 28.37%** — exceeds 15%. Review whether scope is equivalent across bids or one is a low-bid outlier.

## Severity Definitions

| Severity | Meaning | Default owner action |
|---|---|---|
| Critical | Non-compliant, voids warranty, or safety risk | Reject or cure before award |
| High | Material deviation from RFP or industry standard | Negotiate or reject |
| Medium | Ambiguity or moderate risk | Request written clarification |
| Low | Minor note | Accept, note for contract admin |

_Red flags identified by `roof-technical-review` and `roof-qualification-check` against `fixtures/domain_knowledge/`._
