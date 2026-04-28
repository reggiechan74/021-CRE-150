# Roof Replacement Tender — Red Flag Report

**Project:** 2550 Argentia Road, Mississauga, Ontario
**Owner:** Tenebrus Capital
**RFP:** TC-ROOF-2026-001
**Report date:** 2026-04-28T04:37:06.363560+00:00

---

## Executive Summary

- Bids received: 5
- Fully compliant: 0
- Conditional (scored, pending pre-contract clarifications): 3
- Non-compliant (excluded from ranking): 2
- Critical red flags: 20
- High-severity red flags: 20
- Medium / low: 27 / 20

---

## Stage 1 — Mandatory Gate Results

### Heritage Construction Group

| Gate | Result | Evidence |
|---|:---:|---|
| Wsib Clearance | ✅ pass | WSIB Clearance Certificate listed in ATTACHMENTS; INSURANCE COVERAGE section: 'Workers Compensation: WSIB Account #7890123-45'; SAFETY PROGRAM: 'WSIB Experience Rating: 0.81' (below 1.0 = better than industry average). Bid manifest: wsib_clearance_attached=true, wsib_in_good_standing=true. |
| Cgl Insurance | ✅ pass | INSURANCE COVERAGE section: 'Commercial General Liability: $5,000,000 per occurrence'; matches RFP §5.1.2 minimum (mandatory_requirements.cgl_minimum_cad = $5,000,000). Certificate of Insurance listed in ATTACHMENTS. |
| Additional Insured | ⚠️ clarify | INSURANCE COVERAGE section lists CGL, Auto, Pollution and WSIB but does NOT explicitly state Tenebrus Capital is named as additional insured on the COI. Bid manifest qualifications.owner_named_as_additional_insured = null. |
| Completed Ops | ⚠️ clarify | INSURANCE COVERAGE section does not state a completed-operations tail. Bid manifest qualifications.cgl_completed_operations_years = null. |
| Working At Heights | ✅ pass | SAFETY PROGRAM section: 'Fall protection training for all workers (updated annually)'; PROJECT TEAM names Marcus Johnson as CRSP-certified Safety Coordinator; technical_approach.fall_protection_plan: 'Annual fall protection training for all workers; COR-certified safety program'. Bid manifest qualifications.working_at_heights_training_confirmed = true. |
| Performance Bond | ⚠️ clarify | WHY HERITAGE CONSTRUCTION GROUP §5: 'Bonding capacity up to $5 million per project' — capacity declared but no consent of surety for the 50% performance bond required by RFP §9.2 was attached to this bid submission. |
| Labour Material Bond | ⚠️ clarify | Same as performance_bond — $5M bonding capacity declared but consent of surety for the 50% L&M bond required by RFP §9.2 was not attached. |
| Bid Bond | ⚠️ clarify | RFP submission_requirements does not list a bid bond and mandatory_requirements has no bid_bond_percent — therefore bid_bond is NOT APPLICABLE per scripts/gate_applicability.py and the strongest result is needs_clarification, never fail. Bid attachments list COI, WSIB cert, COR, product data sheets, warranty samples, reference letters, manufacturer certifications, VE summary, safety program, phasing plan, Apotex case study — no bid bond. |
| Site Visit | ✅ pass | COVER LETTER: 'We attended the mandatory site visit on March 25, 2026, and conducted a detailed analysis of the existing conditions.' RFP §6.4 / §8.1 require mandatory attendance. |
| Minimum Years In Business | ✅ pass | COVER LETTER: 'Founded in 2012'; WHY HERITAGE §5: '14 years in business'. Bid manifest qualifications.years_in_business = 14. RFP §5.1.3 requires minimum 10 years. |
| Similar Project References | ✅ pass | Four references provided, all commercial/industrial low-slope roof replacements completed 2023-2025: Amazon Fulfillment YHM1 Hamilton (185,000 sf, 2024), Magnotta Winery Niagara-on-the-Lake (92,000 sf, 2023), Prologis Park 407 Vaughan (145,000 sf, 2025), Apotex Pharmaceuticals Toronto (78,000 sf, 2024). RFP §5.1.4 requires minimum 3 references from similar projects (50,000+ sq ft) within past 5 years. |
| Scope Compliance | ✅ pass | Base bid §KEY SPECIFICATIONS confirms 60 mil TPO fully-adhered, R-30 two-layer staggered insulation, 1/4" gypsum cover board, white 80% solar reflectance — matches RFP §3.1/§3.2. VE Options 1-5 are alternates; the base bid itself is RFP-compliant. |
| Membrane Thickness | ✅ pass | 60 mil TPO base bid (KEY SPECIFICATIONS table) meets RFP §3.1 minimum 60 mil. Fixture 02 §1.3 floor for commercial. |
| Cover Board | ✅ pass | 1/4" gypsum cover board explicitly listed in base bid PRICE BREAKDOWN ($28,000 line item) and KEY SPECIFICATIONS table. RFP §3.2 requires 1/4" gypsum or HD polyiso. |
| Insulation Upgrade | ✅ pass | R-30 two-layer staggered polyiso (PRICE BREAKDOWN: $115,000) meets RFP §3.2 'R-30 as per Ontario Building Code 2024' and SB-10 Zone 5 minimum ~R-30ci (fixture 01 §1.3). |
| Warranty Type | ✅ pass | Bid §WARRANTY (BASE BID) offers '20-year NDL warranty on TPO membrane'. RFP §3.1/§9.6 specify '20-year manufacturer warranty' without explicitly defining type; rfp.json applied total_system_ndl as inferred default. Heritage's NDL claim is at or near the inferred default but lacks a named manufacturer system program — flagged as warranty red flag rather than gate fail since clarification (manufacturer/system commitment) can cure without re-bid. |
| Warranty Duration | ✅ pass | 20-year manufacturer warranty (base) and 2-year workmanship — meets RFP §9.6 minimums (20 yr / 2 yr). |
| Completion Date | ✅ pass | Substantial completion July 30, 2026; final completion August 12, 2026. Within RFP-implicit 2026 construction season; no specific RFP completion deadline cited in rfp.json. |
| Fire Rating | ✅ pass | Base bid TPO with cover board + polyiso assembly is a standard CAN/ULC-S107 Class A configuration for major manufacturers. RFP does not specify a class beyond OBC default; no deficiency identified. |
| Wind Uplift | ✅ pass | Bid does not numerically state CSA A123.21 / FM 1-29 uplift rating — but proposed assembly (60 mil TPO fully-adhered over HD cover board over polyiso) is a standard rated assembly. Missing design basis treated as red flag (per skill rubric: 'design basis not stated' is a red flag, not a fail). |

**Stage 1 status:** COMPLIANT — advances to rated scoring

### Lakeside Roofing Inc.

| Gate | Result | Evidence |
|---|:---:|---|
| Wsib Clearance | ⚠️ clarify | INSURANCE COVERAGE + ATTACHMENTS — WSIB Account #1234567-89 with Clearance Certificate attached and Experience Rating 0.98 (good standing). Manifest qualifications.wsib_clearance_date is null — cert date not transcribed. |
| Cgl Insurance | ✅ pass | INSURANCE COVERAGE — 'Commercial General Liability: $5,000,000 per occurrence' meets RFP §5.1.2 minimum_cgl_cad of 5,000,000. |
| Additional Insured | ⚠️ clarify | Cover letter does not state owner is named as additional insured; manifest qualifications.owner_named_as_additional_insured is null pending COI inspection. |
| Completed Ops | ⚠️ clarify | Bid states only the $5M per-occurrence limit (cover letter INSURANCE COVERAGE). Completed-operations tail period is not disclosed; manifest qualifications.cgl_completed_operations_years is null. |
| Performance Bond | ⚠️ clarify | RFP §9.2 requires performance bond 50% of contract value at award. Bid does not address bonding capacity or consent of surety; manifest qualifications.bonding_capacity_cad is null. |
| Labour Material Bond | ⚠️ clarify | RFP §9.2 requires L&M bond 50% of contract value. Bid is silent on L&M bonding. |
| Bid Bond | ⚠️ clarify | Bid does not include a bid bond (qualifications.bid_bond_attached=false). RFP submission_requirements (§6.2) lists 13 items; no bid bond is named. mandatory_requirements has no bid_bond_percent field. |
| Working At Heights | ✅ pass | SAFETY PROGRAM — 'Fall protection training for all workers'; manifest qualifications.working_at_heights_training_confirmed=true. |
| Site Visit | ✅ pass | COVER LETTER — 'We attended the mandatory site visit on March 25, 2026.' Satisfies RFP §6.4 / §8.1 mandatory site meeting. |
| Minimum Years In Business | ✅ pass | COVER LETTER — '12 years' serving GTA; manifest qualifications.years_in_business=12. RFP §5.1.3 requires minimum 10. |
| Similar Project References | ⚠️ clarify | Three industrial roof replacement references provided: Maple Logistics 62,000 sf (2024), Westpark 71,000 sf (2023), Torque Distribution 55,000 sf (2025). All same building class (industrial commercial), all within 5 years, all >50,000 sf, all within 0.5x-2x of subject 85,000 sf footprint. |
| Membrane Thickness | ❌ fail | Bid KEY SPECIFICATIONS: 'Membrane: 45 mil TPO, mechanically attached'. RFP §3.1 specifies 'Minimum 60 mil', but RFP §4 mandatory_requirements does not invoke membrane_thickness as a formal mandatory gate — Tenebrus Capital populated only wsib_clearance_required, cgl_minimum_cad, performance_bond_percent, labour_material_bond_percent, site_visit_required, minimum_years_in_business, and minimum_similar_projects. Per scripts/reconcile_gates.py applicability rule, the underlying technical concern is captured as a critical red flag (45 mil sub-spec for Class A commercial retrofit per fixture 02 §1.3). RFP §3.1 specifies but does not invoke as mandatory gate — captured as critical red flag instead. |
| Cover Board | ❌ fail | Bid materials_system.cover_board_included = false; cover board not mentioned in KEY SPECIFICATIONS or PRICE BREAKDOWN. RFP §3.2 / scope_of_work.included_items requires 'cover board (1/4 inch gypsum or HD polyiso)', but RFP §4 mandatory_requirements does not invoke cover_board as a formal mandatory gate. Per scripts/reconcile_gates.py applicability rule, the underlying technical concern is captured as a critical red flag (missing cover board over polyiso voids most NDL warranties per fixture 02 §4 Red Flag #3). RFP §3.2 specifies but does not invoke as mandatory gate — captured as critical red flag instead. |
| Warranty Type | ❌ fail | Bid WARRANTY: '15-year limited warranty on TPO membrane' (material_only per extraction). RFP warranty_requirements.warranty_type_required = 'total_system_ndl' (an INFERRED default from fixture 02 §1, not a literal RFP statement); RFP §4 mandatory_requirements does not invoke warranty_type as a formal mandatory gate. Per scripts/reconcile_gates.py applicability rule, the underlying technical concern is captured as a critical red flag (material-only is substantively weaker than NDL Total System per fixture 02 §4 Red Flag #5). RFP §3.1/§9.6 specifies but does not invoke as mandatory gate — captured as critical red flag instead. |
| Warranty Duration | ❌ fail | Bid WARRANTY offers 15-year manufacturer warranty. RFP §3.1/§9.6 and warranty_requirements.minimum_manufacturer_years = 20, but RFP §4 mandatory_requirements does not invoke warranty_duration as a formal mandatory gate. Per scripts/reconcile_gates.py applicability rule, the underlying technical concern (offered duration 5 years below RFP minimum) is captured as a critical red flag. RFP §3.1/§9.6 specifies but does not invoke as mandatory gate — captured as critical red flag instead. |
| Scope Compliance | ❌ fail | Bid EXCLUSIONS list contradicts multiple RFP-required base-scope items: (a) excludes 'Temporary weather protection for incomplete phases' vs RFP requirement that 'each phase watertight at end of each work day'; (b) excludes 'Tapered insulation for ponding correction' vs RFP requirement to 'resolve existing ponding via tapered insulation or additional drains'; (c) bidder rebuts ponding existence; (d) excludes 'Replacement of damaged roof drains or leaders' vs RFP requirement to 'replace damaged drain bowls/leaders'; (e) single-layer R-30 vs RFP §3.2 'two-layer staggered'; (f) no wind uplift design basis stated. RFP §4 mandatory_requirements does not invoke scope_compliance as a formal mandatory gate. Per scripts/reconcile_gates.py applicability rule, these are captured as critical red flags. RFP §3.1/§3.2/§5.1.6 specifies as scope/warranty requirement (rfp_scope tier). |

**Stage 1 status:** NON-COMPLIANT — excluded

### Metro Building Solutions Inc.

| Gate | Result | Evidence |
|---|:---:|---|
| Wsib Clearance | ⚠️ clarify | ATTACHMENTS lists 'WSIB Clearance Certificate' and INSURANCE COVERAGE section cites WSIB Account #3456789-01; however bid manifest qualifications.wsib_clearance_date is null and qualifications.wsib_in_good_standing is null — no clearance date or 'in good standing' wording extracted from the certificate. |
| Cgl Insurance | ✅ pass | INSURANCE COVERAGE section: 'Commercial General Liability: $5,000,000 per occurrence' equals RFP §5.1.2 / mandatory_requirements.cgl_minimum_cad of $5,000,000. |
| Additional Insured | ⚠️ clarify | Bid declares CGL limit but is silent on whether Tenebrus Capital is named as additional insured on the COI; qualifications.owner_named_as_additional_insured is null in the manifest. |
| Completed Ops | ⚠️ clarify | qualifications.cgl_completed_operations_years is null in the manifest; INSURANCE COVERAGE section names a CGL limit but does not state the completed-operations tail. |
| Performance Bond | ⚠️ clarify | Bid is silent on bonding capacity and consent of surety. RFP §9.2 requires a 50% performance bond on this OBC Part 3 project. |
| Labour Material Bond | ⚠️ clarify | Bid is silent on L&M bond; RFP §9.2 requires a 50% L&M bond on this OBC Part 3 project. |
| Bid Bond | ⚠️ clarify | qualifications.bid_bond_attached is false. RFP mandatory_requirements does not set bid_bond_percent and submission_requirements (§6.2) does not list a bid bond. |
| Working At Heights | ⚠️ clarify | SAFETY PROGRAM section states 'Fall protection equipment provided' but the bid does not confirm O. Reg. 297/13 Working-at-Heights training currency for on-site workers; qualifications.working_at_heights_training_confirmed is null. |
| Site Visit | ✅ pass | Cover Letter: 'We attended the site visit on March 25, 2026.' RFP §6.4 / §8.1 makes the site meeting mandatory. |
| Minimum Years In Business | ✅ pass | Cover Letter: 'operating in the Greater Toronto Area since 2010' — 16 years as of 2026; qualifications.years_in_business = 16. RFP §5.1.3 requires minimum 10 years. |
| Similar Project References | ⚠️ clarify | Three references provided (REFERENCES section): Smallwood Industrial Park 48,000 sf (2024), Valley View Warehouse 52,000 sf (2023), Eastgate Commerce Centre 67,000 sf (2025). RFP §5.1.4 requires 3 references for similar projects 50,000+ sq ft completed within 5 years. |
| Addenda Acknowledgment | ⚠️ clarify | Bid does not acknowledge or list any RFP addenda; cover letter and bid body silent on addenda. |
| Non Collusion Declaration | ⚠️ clarify | No non-collusion declaration is referenced in the cover letter, bid body, or ATTACHMENTS list. |
| Cover Board | ❌ fail | Bid IMPORTANT EXCLUSIONS item #4 explicitly excludes cover board from base bid (offered as $38,000 add-on); RFP §3.2 specifies '1/4 inch gypsum or HD polyiso' cover board over polyiso under TPO and fixture 02 §1.3 makes cover board mandatory under TPO for NDL-warranty validity. However, RFP §3.2/§5.1.6/§9.6 specifies as scope/warranty requirement (rfp_scope tier). RFP mandatory_requirements does not list cover_board, and submission_requirements does not enumerate it verbatim. Per scripts/reconcile_gates.py applicability rule, demoted to needs_clarification; underlying technical concern preserved in red_flags[] as critical. |
| Scope Compliance | ❌ fail | Base bid omits multiple RFP-required scope items without offering equivalents (cover board, tapered insulation for ponding, drain bowl/leader replacement, HVAC curb work, skylight reconciliation, permits) and contains 25 declared exclusions plus 15 clarifications/assumptions that materially diverge from the RFP scope. However, RFP §3.2/§5.1.6/§9.6 specifies as scope/warranty requirement (rfp_scope tier). RFP mandatory_requirements does not list scope_compliance and submission_requirements does not enumerate a verbatim 'full scope compliance' clause. Per scripts/reconcile_gates.py applicability rule, demoted to needs_clarification; the cumulative scope-divergence concern is preserved in red_flags[] as critical. |
| Warranty Duration | ❌ fail | Bid WARRANTY section: 'Workmanship Warranty: 1 year on installation' is below RFP §9.6 stated minimum of 2 years; the 3-year upgrade is offered only as a $8,500 priced add-on. However, RFP §3.2/§5.1.6/§9.6 specifies as scope/warranty requirement (rfp_scope tier). RFP mandatory_requirements does not list warranty_duration (only wsib_clearance_required, cgl_minimum_cad, performance_bond_percent, labour_material_bond_percent, site_visit_required, minimum_years_in_business, minimum_similar_projects), and submission_requirements does not enumerate a verbatim '2-year workmanship warranty' line item. Per scripts/reconcile_gates.py applicability rule, demoted to needs_clarification; underlying deficiency preserved in red_flags[] as critical. |

**Stage 1 status:** NON-COMPLIANT — excluded

### Pinnacle Roofing Corp.

| Gate | Result | Evidence |
|---|:---:|---|
| Wsib Clearance | ⚠️ clarify | WSIB Clearance Certificate listed in ATTACHMENTS; account #5678901-23 cited in INSURANCE COVERAGE; bidder claims good standing and provides Experience Rating 0.89. However, certificate issue/expiry date is NOT transcribed in the cover-letter narrative — validity window cannot be confirmed from the bid text alone. |
| Cgl Insurance | ✅ pass | INSURANCE COVERAGE section: 'Commercial General Liability: $5,000,000 per occurrence' — meets RFP §5.1.2 / mandatory_requirements.cgl_minimum_cad of $5,000,000. |
| Additional Insured | ⚠️ clarify | INSURANCE COVERAGE section silent on whether Tenebrus Capital is named as additional insured. COI is attached but contents not transcribed in bid narrative. |
| Completed Ops | ⚠️ clarify | INSURANCE COVERAGE section declares CGL $5M per occurrence but does not state completed-operations tail length. |
| Performance Bond | ⚠️ clarify | RFP §9.2 requires 50% performance bond on this OBC Part 3 project. Pinnacle bid is silent on bonding capacity, surety, or consent of surety. ATTACHMENTS list and INSURANCE COVERAGE section make no reference to bonds. |
| Labour Material Bond | ⚠️ clarify | RFP §9.2 requires 50% L&M payment bond. Pinnacle bid does not address L&M bonding or surety. |
| Bid Bond | ⚠️ clarify | RFP submission_requirements list 13 items; bid bond is NOT among them, and rfp.mandatory_requirements has no bid_bond_percent field. Pinnacle did not attach a bid bond. |
| Working At Heights | ✅ pass | SAFETY PROGRAM section: 'Fall protection training for all workers (updated every 2 years)'. Bid asserts a written safety manual, weekly safety meetings, and incident reporting. WSIB Experience Rating 0.89 (below industry average) corroborates an active safety culture. |
| Site Visit | ✅ pass | Cover Letter para 2: 'We attended the mandatory site visit on March 25, 2026.' submission_metadata.site_visit_attended = true; site_visit_date = 2026-03-25. |
| Minimum Years In Business | ✅ pass | Cover Letter: 'Established in 2008' — 18 years to 2026. Exceeds RFP §5.1.3 minimum of 10 years commercial roofing experience. |
| Similar Project References | ✅ pass | Three references, all comparable on the three-part test: (1) Canadian Tire Distribution Centre, Concord ON (2024, 95,000 sf, occupied distribution); (2) Loblaws Head Office, Brampton ON (2023, 78,000 sf, continuous-ops office); (3) Tim Hortons Supply Chain, Oakville ON (2025, 62,000 sf, cold-storage). All commercial OBC Part 3 class, all >50,000 sf threshold per RFP §5.1.4, all completed within last 3 years. Named contacts with phone numbers provided. |
| Addenda Acknowledgment | ⚠️ clarify | Bid does not reference any addenda acknowledgment. RFP did not explicitly require an addenda acknowledgment in mandatory_requirements (no addenda_acknowledgment_required field) and the submission_requirements list does not enumerate it. |
| Non Collusion Declaration | ⚠️ clarify | No non-collusion declaration is attached or referenced in the bid. |
| Scope Compliance | ✅ pass | KEY SPECIFICATIONS table confirms 60 mil TPO fully adhered, R-30 two-layer polyiso, 1/4" gypsum cover board, 82% solar reflectance — matches RFP §3.1/§3.2. Phased plan caps exposure at 10,000 sf (RFP §2.1 ceiling: 15,000 sf). |
| Membrane Thickness | ✅ pass | PRICE BREAKDOWN line 'TPO membrane (60 mil)' and KEY SPECIFICATIONS row confirm 60 mil — meets RFP §3.1 minimum. |
| Cover Board | ✅ pass | PRICE BREAKDOWN line 'Cover board (gypsum) $32,000' and KEY SPECIFICATIONS row '1/4" gypsum board' — meets RFP §3.2 (1/4" gypsum or HD polyiso) and fixture 02 §1.3 cover-board requirement under TPO. |
| Insulation Upgrade | ✅ pass | KEY SPECIFICATIONS row 'Insulation R-Value R-30; Two-layer, staggered joints' meets RFP §3.2 / OBC SB-10 Zone 5 floor (~R-30ci continuous per fixture 01 §1.3). |
| Warranty Type | ? clarify | WARRANTY section states '20-year NDL'; ATTACHMENTS list cites only '20-Year NDL Warranty Sample Documentation' (a sample, not a system letter), and bid does not name a single manufacturer for the supplied TPO. Per fixture 02 §1.3 and §3, total_system_ndl requires named certified installer for the supplied system, pre-install review, and manufacturer inspection — none evidenced. Recorded as a clarify rather than fail because the bidder does hold Carlisle/Firestone/JM certifications and could likely produce a true system NDL once the manufacturer is selected. |
| Warranty Duration | ✅ pass | WARRANTY section: '20-year NDL' meets RFP §3.1/§9.6 minimum 20 years. |
| Completion Date | ✅ pass | PROJECT SCHEDULE: Substantial Completion 2026-07-20; Final 2026-08-05 — within typical Ontario roofing season for a May 1 start; RFP does not state a fixed deadline. |
| Mobilization Date | ? clarify | PROJECT SCHEDULE gives a Start Date of 2026-05-01 but does not state mobilization-days-after-award; needs clarification but RFP does not impose a latest-mobilization requirement, so this is not a fail. |
| Fire Rating | ? clarify | Bid does not state a CAN/ULC-S107 listing for the proposed assembly (membrane, cover board, polyiso, deck). RFP is silent on a specific class but OBC 3.1.15.2 requires listed assembly. Treat as clarify; not a rebid trigger. |
| Wind Uplift | ? clarify | WARRANTY section field 'wind_uplift_coverage_mph' is null; bid does not cite a CSA A123.21 listing or FM 1-29/1-90 design basis. Per skill rules, missing wind-uplift design basis is a red flag, not a gate fail. |

**Stage 1 status:** COMPLIANT — advances to rated scoring

### Summit Contracting Ltd.

| Gate | Result | Evidence |
|---|:---:|---|
| Wsib Clearance | ⚠️ clarify | Bid ATTACHMENTS list 'WSIB Clearance Certificate' and INSURANCE COVERAGE section gives WSIB Account #9876543-21; SAFETY PROGRAM cites WSIB Experience Rating 0.72 (favourable). However, the certificate's issue/clearance date is not stated in the bid body, so the validity window cannot be confirmed from the manifest text alone (fixture 04 §1.3 — clearance certificates have a defined validity window). |
| Cgl Insurance | ✅ pass | INSURANCE COVERAGE — 'Commercial General Liability: $10,000,000 per occurrence'. RFP §5.1.2 requires minimum $5M; Summit at $10M is 2x the floor. |
| Additional Insured | ⚠️ clarify | Bid declares CGL limit of $10M and lists 'Certificate of Insurance ($10M liability)' as an attachment, but the bid body does not state whether Tenebrus Capital is named as additional insured on the COI. |
| Completed Ops | ⚠️ clarify | Bid does not state the completed-operations coverage period for the $10M CGL policy. Critical for the post-install warranty period per fixture 04 §2. |
| Performance Bond | ⚠️ clarify | RFP §9.2 requires performance bond at 50% of contract value (mandatory_requirements.performance_bond_percent = 50). Summit's bid does not include a consent of surety or agreement-to-bond letter, and no surety is named in the cover letter or attachments list. |
| Labour Material Bond | ⚠️ clarify | RFP §9.2 requires labour and material payment bond at 50% of contract value. No surety document or agreement-to-bond letter is included in the bid. |
| Working At Heights | ✅ pass | SAFETY PROGRAM section: 'Fall protection training for all workers (updated annually)'; COR certified; CRSP-certified Safety Officer (Patricia Lee); zero lost-time incidents in past 7 years; WSIB Experience Rating 0.72. |
| Site Visit | ✅ pass | Cover Letter: 'We attended the mandatory site visit on March 25, 2026, and our team conducted a thorough assessment of the existing conditions.' RFP §6.4 / §8.1 require attendance at mandatory pre-bid site meeting. |
| Minimum Years In Business | ✅ pass | Cover Letter: 'For over 25 years, we have been serving the GTA' — qualifications.years_in_business = 25. RFP §5.1.3 requires minimum 10 years commercial roofing experience. |
| Similar Project References | ✅ pass | Bid §REFERENCES lists 4 projects; 3 are comparable per skill definition (commercial Part 3, completed ≤5 yrs, scale aligned with 85,000 sq ft subject): (1) Maple Leaf Food, 125,000 sq ft, 2023 — occupied phasing; (2) Shoppers Drug Mart Distribution Centre, 210,000 sq ft, 2022 — pharmaceutical cold-storage; (4) Pfizer Canada Mississauga, 95,000 sq ft, 2025 — pharmaceutical with strict temperature controls, described as similar scope. RFP §5.1.4 requires minimum 3 references (50,000+ sq ft) within past 5 years. |
| Bid Bond | ⚠️ clarify | Bid does not include a bid bond. RFP §6.2 (submission_requirements) does not list a bid bond and rfp.mandatory_requirements.bid_bond_percent is not set; the only bonding requirements specified are performance and L&M bonds at §9.2. |
| Scope Compliance | ✅ pass | Cover Letter §INCLUDED IN OUR BID PRICE and §KEY SPECIFICATIONS — bid claims full RFP compliance with no declared exclusions; tapered insulation, cover board, 47-penetration flashing scope, hazmat testing, drain replacement (4) all included. |
| Membrane Thickness | ✅ pass | §KEY SPECIFICATIONS — 80 mil TPO proposed vs RFP minimum 60 mil. Voluntary upgrade noted in §VALUE ENGINEERING OBSERVATIONS. |
| Cover Board | ✅ pass | §KEY SPECIFICATIONS row 'Cover Board: High-density polyiso'; §PRICE BREAKDOWN line 'Cover board (high-density polyiso) $48,000'. Meets fixture 02 §4 requirement for HD polyiso/DensDeck under TPO over polyiso. |
| Insulation Upgrade | ✅ pass | §KEY SPECIFICATIONS — R-38 two-layer staggered polyiso vs RFP minimum R-30. Meets/exceeds SB-10 Zone 5 ~R-30ci continuous threshold (fixture 01 §1.3). |
| Warranty Type | ✅ pass | §WARRANTY — '30-year NDL (No Dollar Limit) warranty on TPO membrane'. Meets RFP-required total_system_ndl tier in form, although the named manufacturer program backing the NDL is not identified (see warranty red flag). |
| Warranty Duration | ✅ pass | §WARRANTY — 30-year manufacturer warranty exceeds RFP 20-year minimum by 10 years; workmanship 5 years exceeds RFP 2-year minimum. |
| Completion Date | ✅ pass | §PROJECT SCHEDULE — Substantial Completion July 25, 2026; Final Completion Aug 10, 2026. RFP does not specify a hard substantial-completion deadline; bid is consistent with the May-Aug 2026 occupied-building work window. |
| Fire Rating | ? unclear | Bid does not state CAN/ULC-S107 class or listing number for the proposed assembly. RFP does not specify a class either. Treated as documentation gap, not a gate fail (see materials red flag). |
| Wind Uplift | ? unclear | §WARRANTY cites '130 mph wind speed coverage' as a warranty term; bid does not state CSA A123.21 dynamic uplift listing, FM 1-29 design pressures, or zone-by-zone fastening/adhesion design. Per skill guidance, 'design basis not stated' is a high red flag, not a wind_uplift gate fail. |

**Stage 1 status:** COMPLIANT — advances to rated scoring

---

## Stage 2 — Qualitative Red Flags

### Heritage Construction Group

**[CRITICAL] Substitutions — VE Option 5 (Combined Optimal Package) proposes removing the cover board when paired with mechanically attached 80 mil TPO. Removing the cover board on commercial single-ply over polyiso voids most NDL warranty programs and is a top-tier red flag in fixture 02 §4 #3. Although Heritage cites 'Carlisle and Firestone' permitting this with mechanically attached, neither manufacturer's published Sure-Weld or UltraPly TPO 80 mil 30-year NDL warranty program waives the cover board requirement on polyiso — this would require explicit written manufacturer approval. As an alternate the option is informational, but if the owner selects VE 5 it becomes a critical scope risk.**
- Citation: fixture 02 §4 #3 (missing cover board = top-tier red flag); fixture 02 §1.3 (cover board mandatory under TPO); RFP §3.2 (cover board required)
- Evidence: Bid §VE OPTION 5: 'Additional Savings: Remove cover board (not required with mechanically attached assembly per manufacturer) = -$8,000... No cover board (acceptable with this assembly per manufacturer) ... 30-year NDL warranty.' Bid §CLARIFICATIONS #7: 'Cover board: Included in base bid; can be removed if VE Option 5 is selected (mechanically attached system does not require cover board per Carlisle and Firestone).'
- Recommended action: reject

**[HIGH] Warranty — Manufacturer not committed in base bid: contractor holds Carlisle/Firestone/GAF certifications but does not name which system will be installed, so the specific NDL warranty program (Carlisle Golden Seal, Firestone Red Shield, GAF Diamond Pledge) cannot be verified before contract execution.**
- Citation: fixture 02 §3 (Manufacturer Certified Contractor Programs); fixture 02 §4 #1 (mismatched system components red flag)
- Evidence: Heritage bid §KEY SPECIFICATIONS lists '60 mil TPO' generically; §MANUFACTURER CERTIFICATIONS lists three certifications without committing to one. Base manifest extraction_notes #2: 'Manufacturer not explicitly named in base bid... Owner follow-up needed to confirm which TPO system (and therefore which named NDL warranty) will actually be installed before contract execution.'
- Recommended action: clarify

**[HIGH] Warranty — Workmanship warranty 2 years is at the RFP floor and below the 5-year market median for reputable Ontario commercial contractors per fixture 02 §4 #6. Combined with bid's own claim of 14 years in business and stable bonding, a longer workmanship term would be expected.**
- Citation: fixture 02 §4 #6 (workmanship warranty market median 5 years); RFP §9.6 (minimum 2 years)
- Evidence: Bid §WARRANTY (BASE BID): 'Workmanship Warranty: 2 years on installation.'
- Recommended action: negotiate

**[HIGH] Materials — Wind uplift design basis not stated. RFP is silent on numeric uplift requirements but bid does not cite CSA A123.21 listing or FM 1-60/1-90 rating for the proposed 60 mil fully-adhered TPO over R-30 polyiso assembly. For a 28-year-old industrial roof with parapets at 28 ft height in Mississauga, factored uplift pressures should be calculated per NBC Part 4.**
- Citation: fixture 01 §1.2 (CSA A123.21 / FM 1-29); fixture 02 §4 #4 (no wind uplift design basis red flag)
- Evidence: Heritage bid references 'wind uplift risk is moderate' for VE Option 1 (mechanically attached) but provides no calculation, no zone breakdown (field/perimeter/corner), and no listed assembly number anywhere. Base manifest extraction_notes #5: 'Wind uplift coverage mph: Not stated in bid... Owner follow-up needed.'
- Recommended action: clarify

**[HIGH] Safety — Fall protection plan is generic WAH compliance language (annual training, COR cert, dedicated coordinator) but lacks site-specific elements required by O. Reg. 213/91 §26.1: named anchor points, lifeline/lanyard inventory, rescue plan, and approach for parapet/perimeter work on the 47 penetrations and three roof levels. No NOP filing commitment cited (project >$50k triggers per O. Reg. 213/91 §6).**
- Citation: O. Reg. 213/91 §26.1 (fall protection plan and rescue plan); O. Reg. 213/91 §6 (Notice of Project); fixture 01 §3.2-3.3
- Evidence: Bid §SAFETY PROGRAM: 'Fall protection training for all workers (updated annually); Daily tailgate safety meetings; Dedicated safety coordinator for projects over 75,000 sq ft.' No site-specific fall protection plan, no anchor layout, no rescue plan visible. Heritage manifest field technical_approach.fall_protection_plan is similarly generic.
- Recommended action: clarify

**[MEDIUM] Qualifications — Owner-named-as-additional-insured not explicitly stated on Heritage's INSURANCE COVERAGE section. Standard COI endorsement clarifiable pre-contract but must be confirmed before award.**
- Citation: —
- Evidence: —
- Recommended action: Require revised Certificate of Insurance naming Tenebrus Capital as additional insured on the CGL policy prior to contract execution.

**[MEDIUM] Qualifications — CGL completed-operations tail duration not stated in bid. Critical for the 2-year workmanship warranty period and any latent-defect exposure post-substantial-completion.**
- Citation: —
- Evidence: —
- Recommended action: Require COI endorsement evidencing a completed-operations tail of at least 2 years (matching workmanship warranty) — preferably extending to the 20-year manufacturer warranty term where commercially available.

**[MEDIUM] Qualifications — Performance bond and Labour & Material payment bond consent-of-surety letters not attached to bid submission. RFP §9.2 mandates 50% performance and 50% L&M bonds. Heritage declared $5M bonding capacity (well above project value) but no surety consent letter attached.**
- Citation: —
- Evidence: —
- Recommended action: On award notification, require consent of surety letters from a Canadian-licensed surety naming both bonds at the required 50% before contract signing. Failure to produce at that stage would be a fail.

**[MEDIUM] Warranty — RFP-required warranty type 'total_system_ndl' (per inferred default in rfp.json provenance) versus Heritage's bid-stated 'ndl' — the difference is whether the warranty is a manufacturer-specific named system program (e.g., Carlisle Total System, Firestone Red Shield Platinum) with PAQ+S/Authorized Applicator inspection prerequisites. Heritage's attached 'Sample 20-Year and 30-Year NDL Warranty Sample Documentation' is sample-only and not committed to a specific system. Cure available via clarification.**
- Citation: fixture 02 §1.3 (Carlisle 30-year Golden Seal prerequisites: Authorized Applicator, mid-job inspection); RFP §3.1 / §9.6 / §5.1.6 (manufacturer certification required)
- Evidence: Bid §ATTACHMENTS lists 'Sample 20-Year and 30-Year NDL Warranty Sample Documentation' but no executed warranty form or manufacturer pre-job notice. Base manifest warranty_offered.warranty_type='ndl' (not 'total_system_ndl'); extraction_notes #3: 'Not classified as total_system_ndl since no certified-installer/system-warranty-program prerequisites are documented in this submission.'
- Recommended action: clarify

**[MEDIUM] Scope — Manufacturer pre-installation notice and mid-job technical inspection not budgeted or scheduled. Carlisle/Firestone/GAF top-tier (25-30 year) NDL warranties universally require pre-job notice + mid-job manufacturer rep inspection + final inspection (fixture 02 §4 #7). Without these line items, the 20-year NDL claim may be marketing-only.**
- Citation: fixture 02 §4 #7 (no pre-installation or mid-job manufacturer inspection for long warranties)
- Evidence: Bid §PRICE BREAKDOWN does not include a manufacturer technical-rep inspection line item. §QUALITY CONTROL is bi-weekly progress reports by Heritage staff only.
- Recommended action: clarify

**[MEDIUM] Scope — Bid excludes 'Replacement of damaged roof drains or leaders' but RFP §2.1 §included_items requires 'replace damaged drain bowls/leaders'. This appears to be a direct exclusion of a required scope item — not just a cap on quantities.**
- Citation: RFP §2.1.5 (drainage scope); fixture 02 §5 (drain reconditioning vs replacement)
- Evidence: Bid §EXCLUSIONS #3: 'Replacement of damaged roof drains or leaders.' Compare to RFP scope_of_work.included_items: 'replace damaged drain bowls/leaders'.
- Recommended action: negotiate

**[MEDIUM] Scope — Bid excludes 'Skylight replacement or major repairs' but RFP §2.1 included_items references '4 skylights' as part of the 47 penetrations requiring new flashings. Heritage covers flashings but is silent on skylight curb integration / re-flashing approach where existing skylights remain.**
- Citation: RFP §2.1 (47 penetrations including 4 skylights); fixture 02 §5 (skylight reglazing)
- Evidence: Bid §EXCLUSIONS #4: 'Skylight replacement or major repairs'; bid §INCLUDED IN BASE BID PRICE #6: 'All flashings and penetrations (47 counted during site visit)' — internal ambiguity.
- Recommended action: clarify

**[LOW] Qualifications — Skilled Trades Ontario Certificate of Qualification (C of Q) status of the four lead installers not declared. Bid describes them as 'certified roofing technicians' with avg 10 years experience, but Ontario C of Q is the regulated trade credential under O. Reg. 458/22 / Skilled Trades Ontario.**
- Citation: —
- Evidence: —
- Recommended action: Owner to request written confirmation that at minimum the foreman (Dave Kowalczyk) and a majority of the lead installers hold a current Ontario C of Q in roofing or a related compulsory trade. Affects qualifications sub-score, not a gate.

**[LOW] Qualifications — Subcontracting status not explicitly declared. Bid implies self-perform (named PM, supervisor, safety coordinator, 4 lead installers) but does not state whether any portion of the roofing crew is subcontracted. Shell-company / unnamed-sub risk per fixture 04 §5.**
- Citation: —
- Evidence: —
- Recommended action: Owner to require written declaration of any subcontracted scope (especially the actual roofing crew) and named subcontractors with their own WSIB/CGL/WAH evidence before contract execution.

**[LOW] Qualifications — WSIB clearance certificate date not transcribed in bid body (certificate is listed as attached). Standard award condition is online re-verification at clearances.wsib.ca within 30 days of contract signing — added automatically by the memo skill.**
- Citation: —
- Evidence: —
- Recommended action: Verify WSIB validity online before contract signing; no action required at evaluation stage.

**[LOW] Qualifications — CRCA (Canadian Roofing Contractors Association) membership not declared. Affects industry-membership sub-factor of qualifications_certifications scoring (0 of 15 awarded).**
- Citation: —
- Evidence: —
- Recommended action: Informational; not curable for this bid.

**[LOW] Qualifications — Reference project values (CAD) not stated for any of the four references. All four references pass the size/recency/scope comparable test on the available data, so this is not a gate fail; it does affect verifiability sub-factor of experience_references (8 of 15 awarded instead of 15 of 15).**
- Citation: —
- Evidence: —
- Recommended action: If owner wishes to validate the $0.5x-2x project-value comparable test rigorously, request approximate contract values from Heritage for the Apotex and Magnotta references in particular.

**[LOW] Qualifications — Bid bond not attached. RFP is silent on bid bonds (no bid_bond_percent in mandatory_requirements; no 'bid bond' in submission_requirements) so this is NOT a gate fail per applicability rules. Listed as a red flag because most Ontario private-commercial CCDC 2 procurements treat a 10% bid bond as best practice.**
- Citation: —
- Evidence: —
- Recommended action: Optional: if owner wishes to harden the bid against withdrawal during the 60-day validity window, request a 10% bid bond from the apparent low bidder pre-award.

**[LOW] Scope — VE Option 1 narrative claims fully-adhered specification but RFP §3.1 explicitly allows mechanically attached as an acceptable alternative. The 'value engineering' framing therefore overstates the savings as a deviation from RFP. Not a substitution flag, just a slight mischaracterization.**
- Citation: RFP §3.1 (Fully adhered system preferred; mechanically attached acceptable)
- Evidence: Bid §VE OPTION 1: presented as alternative to base bid fully-adhered system; RFP allows both attachment methods.
- Recommended action: accept-with-condition

### Lakeside Roofing Inc.

**[CRITICAL] Materials — 45 mil TPO membrane proposed where RFP §3.1 specified minimum 60 mil. Sub-specification thickness for a Class A commercial retrofit; voids the RFP spec and would not unlock 20-year+ warranty from any reputable manufacturer. NOTE: Underlying gate (membrane_thickness) demoted to needs_clarification because RFP §4 did not invoke it as a formal mandatory gate; severity preserved here per fixture 02 §4.**
- Citation: fixture 02 §1.3 (TPO thickness: '45 mil: Residential or light commercial. Not acceptable for Class A commercial retrofit'); RFP §3.1; fixture 02 §6 Quick Evaluation Matrix (Fail = <60 mil)
- Evidence: Bid KEY SPECIFICATIONS: 'Membrane: 45 mil TPO, mechanically attached'; PRICE BREAKDOWN line item 'TPO membrane (45 mil) $145,000'
- Recommended action: reject

**[CRITICAL] Materials — No cover board over polyiso insulation. Cover board (HD polyiso or DensDeck) is mandatory under single-ply TPO to protect membrane from foot traffic punctures, provide a smooth substrate, and unlock manufacturer system warranties. NOTE: Underlying gate (cover_board) demoted to needs_clarification because RFP §4 did not invoke it as a formal mandatory gate; severity preserved here per fixture 02 §4.**
- Citation: fixture 02 §4 Red Flag #3 ('Missing cover board... Polyiso alone under TPO/PVC/EPDM is best-practice-deficient... Most manufacturer 25-year+ warranties require it'); RFP §3.2 included_items ('cover board (1/4 inch gypsum or HD polyiso)')
- Evidence: Bid KEY SPECIFICATIONS lists only Membrane, Insulation, and Attachment — cover board absent; PRICE BREAKDOWN has no cover board line item; bid manifest materials_system.cover_board_included = false
- Recommended action: reject

**[CRITICAL] Warranty — Warranty type is material_only (15-yr limited) where RFP requires total_system_ndl with 20-year minimum. Material-only excludes labour to repair and excludes installation defects — owner is left exposed to workmanship and accessory failures. NOTE: Underlying gate (warranty_type) demoted to needs_clarification because RFP §4 did not invoke it as a formal mandatory gate; severity preserved here per fixture 02 §4.**
- Citation: fixture 02 §4 Red Flag #5 ('25-year warranty without the type... Material-only, labor-and-material, or NDL Total System — these are radically different products priced similarly by weaker bidders'); RFP warranty_requirements (warranty_type_required = total_system_ndl, minimum 20 years)
- Evidence: Bid WARRANTY section: '15-year limited warranty on TPO membrane' and 'Sample 15-Year Warranty Documentation attached' (no NDL/total-system language)
- Recommended action: reject

**[CRITICAL] Warranty — Warranty duration of 15 years is 5 years below RFP minimum of 20 years. Below RFP §3.1/§9.6 requirement of 'Minimum 20-year manufacturer warranty on membrane.' NOTE: Underlying gate (warranty_duration) demoted to needs_clarification because RFP §4 did not invoke it as a formal mandatory gate; severity preserved here per fixture 02 §4.**
- Citation: RFP §3.1 / §9.6 ('Minimum 20-year manufacturer warranty on membrane'); RFP warranty_requirements.minimum_manufacturer_years = 20; fixture 02 §4 Red Flag #5
- Evidence: Bid WARRANTY section: '15-year limited warranty on TPO membrane'; Sample 15-Year Warranty Documentation attached; warranty_offered.manufacturer_years = 15
- Recommended action: reject

**[CRITICAL] Warranty — Manufacturer of TPO membrane is not named in the bid. Without a named manufacturer the owner cannot validate (a) which warranty product is being offered, (b) whether the contractor is certified at the claimed tier, or (c) system component compatibility. No GAF Master Elite, Carlisle Authorized Applicator, Sika Sarnafil, Firestone Red Shield, or Johns Manville Peak Advantage program named.**
- Citation: fixture 02 §3 (Manufacturer Certified Contractor Programs — 'Non-certified installers cannot sell the top-tier warranties — regardless of installation quality'); RFP §5.1.6 (Manufacturer Authorization required)
- Evidence: ATTACHMENTS list: 'Product Data Sheets (45 mil TPO membrane)' — manufacturer not identified anywhere in bid; warranty_offered.manufacturer_certified_installer = false
- Recommended action: reject

**[CRITICAL] Scope — Bidder excludes 'Temporary weather protection for incomplete phases' (exclusion #12), explicitly contradicting the RFP requirement that 'each phase watertight at end of each work day.' For an occupied pharmaceutical warehouse with cold-storage tenants, this exclusion creates direct exposure to interior water damage. NOTE: Underlying gate (scope_compliance) demoted to needs_clarification because RFP §4 did not invoke it as a formal mandatory gate; severity preserved here per fixture 02 §4.**
- Citation: RFP scope_of_work.included_items ('Phased construction with no more than 15,000 sq ft exposed at any one time; each phase watertight at end of each work day')
- Evidence: Bid EXCLUSIONS AND CLARIFICATIONS item #12: 'Temporary weather protection for incomplete phases'
- Recommended action: reject

**[CRITICAL] Scope — Bidder rebuts the RFP's documented ponding condition ('our inspection did not confirm significant ponding') and excludes tapered insulation and damaged drain replacement from base bid. This is a substitution of bidder judgment for the owner's stated scope and would leave the existing drainage defect unresolved. Combined with the absence of weather protection, the un-corrected drainage condition creates a system that cannot deliver the 20+ year service life the RFP envisions.**
- Citation: fixture 01 §1.4 (Drainage — 'industry minimum 2% positive slope to drains'; 'Red flag: Dead-flat roof with no tapered insulation'); RFP scope_of_work.included_items (drainage correction including tapered insulation or additional drains; 'replace damaged drain bowls/leaders')
- Evidence: Bid ADDITIONAL NOTES: 'Regarding the ponding issues noted in the RFP: our inspection did not confirm significant ponding. We recommend proceeding with standard installation and addressing any drainage issues if they persist after completion'; EXCLUSIONS items #3 (drains/leaders) and #10 (tapered insulation)
- Recommended action: reject

**[CRITICAL] Materials — Insulation is single-layer R-30. RFP §3.2 requires 'two-layer staggered with cover board.' Single-layer rigid insulation on a commercial roof creates joint leakage and thermal bridging per fixture 02 §4 Red Flag #1 / fixture 01 §1.3. Combined with the absent cover board and 45 mil membrane, the assembly will not deliver the assumed thermal performance or warranty eligibility.**
- Citation: fixture 01 §1.3 ('Two layers of insulation with staggered joints is standard practice to maintain continuity'; Red flag: 'Single layer of rigid insulation on a commercial roof'); RFP scope_of_work.included_items
- Evidence: Bid KEY SPECIFICATIONS: 'Insulation: Polyisocyanurate, R-30 (single layer to meet code minimum)'; ADDITIONAL NOTES: 'Single-layer insulation meets code requirements while minimizing material costs'
- Recommended action: reject

**[CRITICAL] Scope — No wind uplift design basis stated. RFP project is a 28-year-old industrial warehouse with parapeted perimeter; a CSA A123.21 (or FM 1-29) calculation by zone is required. Mechanically-attached TPO with no zoning calculation is at high risk of perimeter/corner billowing — a safety hazard for occupants and adjacent properties.**
- Citation: fixture 01 §1.2 ('Tender must demonstrate: Wind load calculation for the specific project... Named CSA A123.21 listing... Fastening schedule showing field, perimeter, and corner patterns'); fixture 02 §4 Red Flag #4
- Evidence: Bid contains no wind uplift calculation, no CSA A123.21 listing, no FM rating, no fastening schedule by zone. warranty_offered.wind_uplift_coverage_mph = null.
- Recommended action: clarify

**[HIGH] Qualifications — No manufacturer-certified installer status claimed and no manufacturer named for the proposed 45-mil TPO. Without manufacturer certification, the bidder cannot deliver a manufacturer-issued NDL or even a typical 20-yr extended warranty (fixture 04 §4). This compounds the warranty-tier deficiency owned by technical-review and limits owner recourse.**
- Citation: —
- Evidence: KEY SPECIFICATIONS / WARRANTY / ATTACHMENTS — '15-year limited warranty', no manufacturer named, certification_program=null, manufacturer_certified_installer=false.
- Recommended action: —

**[HIGH] Safety — No site-specific fall protection plan. Bid offers a generic 'Fall protection training for all workers' statement. For an 85,000 sq ft low-slope industrial roof, O. Reg. 213/91 Part III requires named anchor points, lifelines, rescue plan, and zone-by-zone control approach. Required rescue plan is absent.**
- Citation: fixture 01 §3.3 ('Tender must demonstrate: Site-specific fall protection plan identifying which method is used in which zone; anchor specifications; harness/lanyard/SRL inventory; rescue plan (mandatory per §26.1)'); O. Reg. 213/91 §26.1
- Evidence: Bid SAFETY PROGRAM section lists training/meetings/incident reporting only. technical_approach.site_safety_plan_attached = false. No anchor layout, no rescue plan stated.
- Recommended action: clarify

**[HIGH] Scope — No waste disposal / environmental plan. RFP is replacing 85,000 sq ft of existing built-up gravel roof — a significant tonnage of demolition debris. No facility named, no diversion commitment, no dumpster placement plan.**
- Citation: fixture 01 §4.1 ('Tender must demonstrate: Named waste disposal / recycling facility; diversion rate target; bin type'); RFP scope_of_work.included_items ('Complete removal and legal disposal')
- Evidence: Bid technical_approach.waste_disposal_plan = null; PRICE BREAKDOWN has 'Roof removal and disposal $85,000' lump-sum but no facility, weights, or diversion target
- Recommended action: clarify

**[HIGH] Warranty — No manufacturer certification at claimed warranty tier. RFP §5.1.6 explicitly requires 'Proof of manufacturer certification for proposed roofing system.' Without certification the manufacturer will not issue any extended warranty regardless of contractor installation quality.**
- Citation: fixture 02 §3 (all manufacturer programs); RFP §5.1.6 (manufacturer authorization required)
- Evidence: Bid warranty_offered.manufacturer_certified_installer = false; certification_program = null. No GAF Master Elite / Carlisle Authorized Applicator / Sika Sarnafil / Soprema PAQ+S / Firestone Red Shield / JM Peak Advantage cited.
- Recommended action: reject

**[MEDIUM] Qualifications — Crew size, mobilization-from-award lead time, named foreman, and any Skilled Trades Certificate of Qualification (Roofer 449A) crew composition are all unstated. For an occupied 85,000 sf pharma cold-storage warehouse this is a meaningful gap in the bidder's resourcing story.**
- Citation: —
- Evidence: Schedule section omits crew_size and mobilization_days; qualifications.certificate_of_qualification_roofers_count=null.
- Recommended action: —

**[MEDIUM] Qualifications — Owner-named-as-additional-insured and CGL completed-operations tail period are not confirmed in the cover letter. Both are commercial baseline (fixture 04 §2) and must be cured before contract.**
- Citation: —
- Evidence: qualifications.owner_named_as_additional_insured=null; cgl_completed_operations_years=null.
- Recommended action: —

**[MEDIUM] Qualifications — Reference values not disclosed — only square footage and owner contacts. The Gate 8 comparable test relies on 0.5x-2x value match; without budget figures the comparability is inferred from size only. Owner should obtain original contract values from each reference to validate.**
- Citation: —
- Evidence: REFERENCES section — three projects cited with sqft and contact only; manifest references_provided[].value_cad=null.
- Recommended action: —

**[MEDIUM] Scope — Mechanically attached TPO proposed where RFP §3.1 stated 'Fully adhered system preferred; mechanically attached acceptable.' Acceptable per RFP letter, but combined with no wind uplift design and no cover board, the mechanically-attached choice compounds wind/uplift risk on perimeter and corner zones.**
- Citation: fixture 02 §1.3 (TPO attachment methods — MF 'billows in high wind if not designed for uplift'); RFP §3.1
- Evidence: Bid KEY SPECIFICATIONS: 'Attachment: Mechanically attached system'; ADDITIONAL NOTES: 'We use efficient mechanically attached systems that reduce installation time and cost'
- Recommended action: clarify

**[MEDIUM] Scope — After-hours HVAC coordination and HVAC curb modifications excluded. RFP requires 72-hour minimum coordination notice for shutdowns and lists HVAC protection during construction in base scope. Excluding curb work and after-hours coordination on an occupied pharmaceutical warehouse with cold-storage tenants creates change-order exposure.**
- Citation: RFP scope_of_work.included_items ('HVAC protection during construction with 72-hour minimum coordination notice for shutdowns')
- Evidence: Bid EXCLUSIONS items #5 ('HVAC curb modifications or replacements'), #6 ('Work required outside standard working hours'), #14 ('After-hours HVAC coordination')
- Recommended action: negotiate

**[LOW] Qualifications — Subcontracting posture not declared. Bid does not affirm self-perform or name any subcontractor. Per fixture 04 §5, undisclosed subcontracting of the actual roofing crew is a financial-distress and quality-control signal.**
- Citation: —
- Evidence: qualifications.subcontracting_declared=false but no affirmative self-perform statement; subcontractors_named=[].
- Recommended action: —

**[LOW] Qualifications — CRCA membership and any Skilled Trades industry membership are not stated. Not disqualifying, but limits the qualifications_certifications sub-score and signals the bidder is not invested in industry-association reputational scrutiny.**
- Citation: —
- Evidence: qualifications.crca_member=null; no industry association named in cover letter.
- Recommended action: —

**[LOW] Qualifications — WSIB clearance certificate date not transcribed; only the account number and good-standing experience rating are visible. Validity window cannot be confirmed from the manifest alone — re-verify online at clearances.wsib.ca before contract (handled as a standard award condition).**
- Citation: —
- Evidence: qualifications.wsib_clearance_date=null.
- Recommended action: —

### Metro Building Solutions Inc.

**[CRITICAL] Materials — No cover board in base bid for TPO over polyiso. Cover board is explicitly required by RFP §3.2 (1/4" gypsum or HD polyiso) and is mandatory under TPO per fixture 02 §1.3 to protect polyiso facer and provide NDL-warranty-compliant substrate. Bidder's clarification 'Cover board not required for this building type' is contrary to industry practice and to the RFP. Captured here as a critical red flag because RFP did not invoke cover_board as a formal mandatory gate (rfp.mandatory_requirements does not list it and submission_requirements does not enumerate it verbatim) - per fixture 02 §4 this remains a critical disqualifier-level concern even though the gate has been demoted to needs_clarification.**
- Citation: fixture 02 §1.3 (TPO insulation stack: 'Cover board is mandatory under TPO'); fixture 02 §4 #3 (missing cover board red flag); fixture 02 §6 (Quick Evaluation Matrix: no cover board = Fail); RFP §3.2
- Evidence: IMPORTANT EXCLUSIONS item #4: 'Cover board - Not included in base bid. Optional upgrade at $38,000.' CLARIFICATIONS #13: 'Cover board not required for this building type.' Add-on price $38,000 (OPTIONAL ADD-ONS).
- Recommended action: reject

**[CRITICAL] Warranty — Workmanship warranty of 1 year is below RFP §9.6 minimum of 2 years. The 3-year upgrade is priced separately at $8,500. Per fixture 02 §4 #6, a workmanship warranty below market median is a defined red flag; 1 yr is well below the 5-yr Ontario market median. Captured as critical red flag rather than gate fail because RFP did not invoke warranty_duration as a formal mandatory gate (rfp.mandatory_requirements does not list it; §9.6 narrative text is not enumerated verbatim in rfp.submission_requirements). Per fixture 02 §4 the underlying deficiency remains critical.**
- Citation: RFP §9.6 ('Minimum 2-year workmanship warranty from contractor'); fixture 02 §4 #6 ('typical 5 years')
- Evidence: WARRANTY section: 'Workmanship Warranty: 1 year on installation.' OPTIONAL ADD-ONS: '3-year workmanship warranty upgrade - $8,500.'
- Recommended action: reject

**[CRITICAL] Warranty — Warranty type is unclear ('20-year limited warranty on TPO membrane') and bidder names no manufacturer and no certified-installer designation. RFP-inferred default per fixture 02 §1 is total_system_ndl. Without manufacturer + certified installer + cover board + mid-job inspection, any 20-yr NDL warranty cannot issue per fixture 02 §3 and §4 #1, #5, #7. Critical because (a) warranty type cannot be confirmed, (b) no manufacturer is named, and (c) no certified-installer credentials are attached - any one is critical per fixture 02 §4.**
- Citation: fixture 02 §3 (manufacturer certified contractor programs); fixture 02 §4 #5 ('25-year warranty without the type'); fixture 02 §4 #7 (no pre-install/mid-job manufacturer inspection); RFP §3.1 / §5.1.6
- Evidence: WARRANTY section: '20-year limited warranty on TPO membrane' (no NDL/material/labour qualifier, no manufacturer name). KEY SPECIFICATIONS lists '60 mil TPO, mechanically attached' with no brand. ATTACHMENTS lists 'Sample Warranty Documentation' but no manufacturer authorization letter and no Master Elite / Red Shield / Authorized Applicator certificate.
- Recommended action: reject

**[CRITICAL] Scope — Bidder declares 25 exclusions in base bid covering cover board, tapered insulation, permits, hazmat handling, material price escalation, and other scope items the RFP requires. The cumulative effect is that the $468K base bid is not directly comparable to fully-compliant bids and the bidder explicitly refuses to include several RFP-required items in base scope (cover board excluded; tapered insulation for ponding 'address only if leaks occur'; permits not included; hazmat on cost-plus-15%). Per fixture 02 §4, cumulative declared-exclusions of this magnitude on RFP-required scope is critical. Captured as red flag (not gate fail) because RFP did not invoke scope_compliance as a formal mandatory gate.**
- Citation: RFP §2.1 (included items); RFP §2.1.7 (positive drainage / resolve ponding via tapered insulation); fixture 02 §4 (scope-divergence pattern)
- Evidence: IMPORTANT EXCLUSIONS - PLEASE READ CAREFULLY section enumerates 25 items. Notable items: #4 cover board excluded; #5 tapered insulation excluded ('We recommend addressing only if leaks occur'); #11 hazardous materials cost-plus-15%; #15 permits not included; #19 material price escalation if start delayed past 60 days. CLARIFICATIONS #13, #14, #15 reinforce these substitutions.
- Recommended action: reject

**[CRITICAL] Scope — Bidder excludes tapered insulation for ponding correction and proposes 'address only if leaks occur.' This contradicts RFP §2.1.7 which requires positive drainage and resolution of existing ponding via tapered insulation or additional drains. Standing water on a 28-year-old roof is the proximate cause of premature membrane failure and will void most manufacturer NDL warranties (fixture 02 §1.3 / §4).**
- Citation: RFP §2.1.7 ('Positive drainage to all roof drains; ... resolve existing ponding via tapered insulation or additional drains'); fixture 01 §1.4 ('No tapered insulation' = red flag)
- Evidence: IMPORTANT EXCLUSIONS item #5: 'Tapered insulation for ponding - Not included. ... We recommend addressing only if leaks occur.' CLARIFICATIONS #14: 'Ponding does not require correction unless causing active leaks.'
- Recommended action: reject

**[CRITICAL] Substitutions — Bidder substitutes mechanically attached for the RFP-preferred fully-adhered system without a wind uplift calculation or named CSA A123.21 / FM 1-60+ assembly listing. RFP §3.1 states fully adhered preferred but accepts MF; however, MF systems require explicit wind-uplift design (zone-specific fastening pattern). Bid does not provide this.**
- Citation: RFP §3.1 (membrane attachment_method: fully_adhered); fixture 01 §1.2 (CSA A123.21 wind uplift listing required); fixture 02 §4 #4 ('No wind uplift design basis')
- Evidence: KEY SPECIFICATIONS: '60 mil TPO, mechanically attached.' CLARIFICATIONS #15: 'Mechanically attached system acceptable (equivalent to fully adhered for this application).' No CSA A123.21 listing, no fastener pattern, no zone-specific calculation provided.
- Recommended action: reject

**[CRITICAL] Scope — Front-loaded payment schedule: 20% upon contract signing for 'mobilization and materials' exceeds typical 10% mobilization and Construction Act norms. Combined with the 25 declared exclusions, this front-loading shifts financial risk to the owner if scope disputes arise mid-project. Per fixture 02 §4 critical-flag pattern, front-loaded payments combined with high-exclusion scopes are a defined risk pattern.**
- Citation: Construction Act (Ontario) - holdback provisions; fixture 02 §4 (cumulative bid-pattern risk indicators)
- Evidence: PAYMENT SCHEDULE section: '20% upon contract signing (mobilization and materials); 30% progress payment (monthly); 30% upon substantial completion; 10% holdback (released as per Construction Act).' Bidder note: 'We require larger upfront payment due to material procurement costs.'
- Recommended action: negotiate

**[HIGH] Qualifications — WSIB experience rating of 1.12 is above the 1.00 industry baseline, indicating worse-than-average claims history. Per fixture 04 §5, an elevated rating is a financial-distress / safety-performance signal that warrants owner due diligence before award on a 90-day occupied-building project.**
- Citation: —
- Evidence: SAFETY PROGRAM section: 'WSIB Experience Rating: 1.12'; manifest qualifications.wsib_experience_rating = 1.12.
- Recommended action: —

**[HIGH] Qualifications — No manufacturer certified-installer status declared. The bid claims a 20-year manufacturer warranty on the TPO membrane but does not name the manufacturer (Carlisle, GAF, Firestone, Versico, Sika, Johns Manville) and does not declare certified-installer credentials (e.g., Carlisle Authorized, GAF Master Select, Firestone Red Shield, Sika Sarnafil). Per fixture 02 §3, manufacturer warranties at this tier are typically only issued to certified installers; the warranty as offered may be unenforceable. Owner must verify before award.**
- Citation: —
- Evidence: WARRANTY section ('20-year limited warranty on TPO membrane'); KEY SPECIFICATIONS / BID SUMMARY (no manufacturer named); no certification listed in ATTACHMENTS.
- Recommended action: —

**[HIGH] Scope — Skylight count discrepancy: bidder counted 4 skylights at site visit; bid claims 'RFP states 12 skylights.' RFP scope_of_work.included_items actually itemizes '4 skylights' within the 47-penetration count. Either way, the bidder's interpretation of scope is unreconciled with the RFP and the discrepancy must be resolved before award.**
- Citation: RFP §2.1.5 (47 penetrations including 4 skylights)
- Evidence: IMPORTANT EXCLUSIONS item #8: 'Skylight work - ... 12 skylights on roof per RFP - we counted 4 during site visit.' RFP scope_of_work.included_items: '47 penetrations (12 HVAC, 8 plumbing vents, 6 electrical conduits, 4 skylights, ...)'.
- Recommended action: clarify

**[HIGH] Safety — Safety program is generic - 'Fall protection equipment provided' and 'Written safety procedures' - with no site-specific fall protection plan, no named anchor points, no parapet/perimeter strategy, and no rescue plan. Per fixture 01 §3.3 (O. Reg. 213/91 §26.1), a rescue plan is mandatory for any fall-arrest system; absence is a critical regulatory gap. Marked high (not critical) because deficiency may be cured by submission of a site-specific plan; no evidence the contractor cannot produce one.**
- Citation: O. Reg. 213/91 §26.1 (fall arrest > 3m, rescue plan mandatory); fixture 01 §3.3
- Evidence: SAFETY PROGRAM section: 'Written safety procedures; Fall protection equipment provided; WSIB Experience Rating 1.12.' technical_approach.fall_protection_plan: 'Fall protection equipment provided (Safety Program section)' - no anchor points, no rescue plan.
- Recommended action: clarify

**[HIGH] Materials — Manufacturer not named for any product (membrane, insulation, flashings, adhesives, fasteners). Per fixture 02 §4 #1 (mismatched system components voids most system warranties), the bid hides which brand family will be used and whether components are compatible. Required for any manufacturer system warranty to issue.**
- Citation: fixture 02 §4 #1 (mismatched system components); RFP §6.2.4 (product data sheets required)
- Evidence: materials_system.manufacturer: null. KEY SPECIFICATIONS: '60 mil TPO, mechanically attached.' BID PRICE BREAKDOWN line 'TPO membrane (60 mil) - $152,000' with no brand. ATTACHMENTS list shows 'Product Data Sheets (60 mil TPO membrane)' - but the manifest does not record which brand.
- Recommended action: clarify

**[HIGH] Scope — Wind uplift design basis is not stated. For a 85,000 sq ft Mississauga industrial roof under OBC Part 3, the bid must state the design wind uplift pressure per zone and a CSA A123.21 (or FM 1-60+) listed assembly. Absence is a fixture 02 §4 #4 'No wind uplift design basis' red flag.**
- Citation: fixture 01 §1.2 (CSA A123.21); fixture 02 §4 #4; NBC Part 4 wind loads
- Evidence: warranty_offered.wind_uplift_coverage_mph: null. No mention of CSA A123.21, FM 1-60/1-90, ASCE 7, or zone-specific fastening pattern anywhere in the bid.
- Recommended action: clarify

**[HIGH] Scope — Bidder excludes hazardous-material handling on a cost-plus-15% basis (Exclusion #11) without acknowledgement of OHSA s.30 Designated Substance Report duty (building constructed 1998 - post-1980 trigger does not apply, but RFP §2.3 flagged ACM/lead possibility during 1998 transition period). No DSA / DSR receipt acknowledgement, no Type 1/2/3 classification framework offered.**
- Citation: fixture 01 §4.2 (O. Reg. 278/05; OHSA §30 DSR duty); RFP §2.3
- Evidence: IMPORTANT EXCLUSIONS item #11: 'Hazardous materials - If any hazardous materials discovered during removal (asbestos, lead flashing, etc.): actual cost plus 15%.' CLARIFICATIONS #1, #4: 'Existing roof can be removed without special hazardous material handling'; 'All existing flashings are non-hazardous materials' - assumption not supported by survey.
- Recommended action: clarify

**[MEDIUM] Qualifications — Reference verifiability is incomplete: all three references include named contact, scope size, and completion year, but no contract value is provided on any. The RFP comparability test (50,000+ sq ft within 5 years) is met on size for two of three references; Smallwood Industrial Park (48,000 sf, 2024) is marginally below the RFP's 50,000 sf threshold.**
- Citation: —
- Evidence: REFERENCES section; manifest qualifications.references_provided[].value_cad all null.
- Recommended action: —

**[MEDIUM] Qualifications — No Skilled Trades Ontario Certificate of Qualification (313A roofer C of Q) crew count declared. For an 85,000 sf occupied OBC Part 3 commercial roof replacement, the absence of a stated C of Q crew count limits the owner's ability to assess installation quality and compliance with Skilled Trades Act requirements (fixture 04 §4).**
- Citation: —
- Evidence: Bid is silent on C of Q roofer count; manifest qualifications.certificate_of_qualification_roofers_count is null.
- Recommended action: —

**[MEDIUM] Qualifications — Crew size and mobilization-days-after-award are not declared. The bid commits to a 90-day duration but does not state crew composition or named foreman, limiting owner ability to assess production capacity and supervision continuity for an occupied-building project.**
- Citation: —
- Evidence: PROJECT SCHEDULE section; manifest schedule.crew_size and schedule.mobilization_days_after_award both null.
- Recommended action: —

**[MEDIUM] Materials — Insulation R-30 is stated and matches RFP §3.2 / OBC SB-10 Zone 5 prescriptive minimum, but the layer count, joint stagger, and vapour barrier product/perm rating are not specified. Fixture 01 §1.3 requires two-layer staggered installation and a vapour barrier on the warm side; bid silent on both.**
- Citation: fixture 01 §1.3; OBC Part 5 §5.5.1 (vapour barrier)
- Evidence: materials_system.insulation_spec: 'Polyisocyanurate, R-30.' No mention of layer count, stagger, or vapour barrier in narrative or attachments list.
- Recommended action: clarify

**[LOW] Qualifications — Working-at-Heights training under O. Reg. 297/13 is not affirmatively confirmed. Bid mentions 'Fall protection equipment provided' but does not state that on-site workers hold current WAH training certificates (3-year validity per fixture 04 §3).**
- Citation: —
- Evidence: SAFETY PROGRAM section; manifest qualifications.working_at_heights_training_confirmed is null.
- Recommended action: —

**[LOW] Qualifications — No CRCA (Canadian Roofing Contractors Association) or regional roofing-association membership declared. Industry membership is a minor positive indicator of professional standards (fixture 04 §4) and is absent from the bid.**
- Citation: —
- Evidence: Bid silent; manifest qualifications.crca_member is null.
- Recommended action: —

### Pinnacle Roofing Corp.

**[CRITICAL] Warranty — 20-year NDL warranty claimed but no specific manufacturer system named and only a 'sample' warranty document is attached. Without a named system, the contractor cannot produce a binding total-system NDL letter at award; the RFP requires total_system_ndl per the manifest's RFP-deficiency-resolved default.**
- Citation: fixture 02 §1.3 (TPO warranty prerequisites — Authorized Applicator, named system, pre-install review, mid-job inspection); fixture 02 §4 item 5 ('25-year warranty without the type' family).
- Evidence: WARRANTY section: '20-year NDL (No Dollar Limit) warranty on TPO membrane'; ATTACHMENTS: '20-Year NDL Warranty Sample Documentation'; MANUFACTURER CERTIFICATIONS lists three brands without specifying the supplied system.
- Recommended action: clarify

**[CRITICAL] Materials — TPO manufacturer not named. Bidder lists certifications with three different manufacturers (Carlisle Syntec, Firestone, Johns Manville) but does not specify which manufacturer's TPO membrane, adhesive, fasteners, cover board attachment system, or termination accessories will be used. Mismatched system components void most NDL system warranties (fixture 02 §4 item 1).**
- Citation: fixture 02 §4 item 1 (mismatched system components void warranty); fixture 02 §1.3 (TPO warranty tiers tied to specific manufacturer programs).
- Evidence: MANUFACTURER CERTIFICATIONS section lists Carlisle/Firestone/JM; PRICE BREAKDOWN line 'TPO membrane (60 mil)' does not name the brand or product line; product data sheets attached but extraction does not confirm a single manufacturer.
- Recommended action: clarify

**[HIGH] Scope — Wind uplift design basis not stated. Bid contains no CSA A123.21 listing, no FM 1-29/1-60/1-90 rating, and no project-specific calculated uplift pressure for field/perimeter/corner zones. RFP §3.1 implicitly relies on OBC compliance; OBC adopts NBC Part 4 with CSA A123.21.**
- Citation: OBC NBC Part 4 / CSA A123.21-20 (fixture 01 §1.2); fixture 02 §4 item 4 ('No wind uplift design basis').
- Evidence: WARRANTY section field wind_uplift_coverage_mph is null; KEY SPECIFICATIONS table does not state uplift rating; PHASING PLAN SUMMARY does not include a fastening schedule with corner/perimeter densification.
- Recommended action: clarify

**[HIGH] Safety — Fall protection plan is generic. Bid cites WAH training renewal cycle, written manual, and weekly safety meetings, but does not name anchor points, specific fall-arrest equipment, rescue plan, or a control-zone/guardrail layout for the parapet and roof-edge zones during built-up tear-off. O. Reg. 213/91 §26.1 mandates a rescue plan for any fall-arrest system; §26.3(6) requires a 2 m control-zone barrier on built-up roof work.**
- Citation: O. Reg. 213/91 §§26.1 and 26.3(6) (fixture 01 §3.3 and §3.4); CSA Z91 (fixture 01 §1.6) for any permanent anchors used.
- Evidence: SAFETY PROGRAM section: 'Fall protection training for all workers (updated every 2 years); written safety manual; weekly safety meetings; incident reporting and investigation' — no site-specific plan, no anchor inventory, no rescue plan referenced.
- Recommended action: clarify

**[HIGH] Warranty — No manufacturer pre-install review or mid-job technical inspection is included in scope. Top-tier NDL warranties (25-30 yr) and even most 20-yr total-system NDL letters require manufacturer technical-rep inspections that the contractor must arrange and absorb. Without scheduled inspections, the 20-yr NDL may not issue at completion.**
- Citation: fixture 02 §3 (manufacturer certified-contractor program prerequisites); fixture 02 §4 item 7 (no pre-install/mid-job inspection for long warranties).
- Evidence: PHASING PLAN SUMMARY and HAZARDOUS MATERIALS APPROACH sections do not mention manufacturer inspection visits; payment schedule shows no manufacturer-acceptance milestone before holdback release.
- Recommended action: clarify

**[MEDIUM] Qualifications — Bonding silent in submission. RFP §9.2 requires 50% performance bond and 50% L&M bond on this OBC Part 3 project, but Pinnacle's submission contains no consent of surety, no bonding capacity declaration, and no surety identified. Bond capacity below project value or inability to obtain consent of surety would prevent contract execution.**
- Citation: —
- Evidence: ATTACHMENTS list; INSURANCE COVERAGE section silent on bonding
- Recommended action: —

**[MEDIUM] Qualifications — Working-at-heights training described in non-regulatory terms. SAFETY PROGRAM cites 'Fall protection training for all workers (updated every 2 years)'. O. Reg. 297/13 mandates a CPO-approved working-at-heights training program with 3-year validity. The 2-year refresh and 'fall protection' label could indicate either (a) the bidder uses an internal program rebranded as fall protection while still meeting the regulatory requirement, or (b) workers are trained on harness use but lack the formal regulatory cert.**
- Citation: —
- Evidence: SAFETY PROGRAM section
- Recommended action: —

**[MEDIUM] Warranty — Workmanship warranty of 3 years is below the 5-year Ontario market median for reputable contractors. Bidder offers an alternate to extend to 5 years for $8,500 — should be evaluated against the price gap to the next bidder.**
- Citation: fixture 02 §4 item 6 (workmanship warranty band; 5-year market median).
- Evidence: WARRANTY section: 'Workmanship Warranty: 3 years on installation'; OPTIONAL ADD-ONS: 'Extended workmanship warranty to 5 years $8,500'.
- Recommended action: negotiate

**[MEDIUM] Scope — Hazardous materials approach assumes 'minimal ACM if any (building is 1998)' with testing during removal and major abatement excluded. RFP §2.3 acknowledges potential ACM and lead flashings during the 1998 transition period; the bidder's 'pause for testing' approach could trigger schedule and cost changes mid-tear-off. RFP excludes ACM abatement costs from the bid (owner-funded) — but bidder should at least price a contingency for stop-work / re-mobilization if ACM is encountered.**
- Citation: O. Reg. 278/05 (asbestos on construction projects) — fixture 01 §4.2; OHSA s.30 (DSR obligation).
- Evidence: EXCLUSIONS item 7 ('Hazardous material abatement beyond minor handling (testing included)'); HAZARDOUS MATERIALS APPROACH ('If hazardous materials are suspected, work will pause for testing'); CLARIFICATIONS item 3 ('We assume minimal ACM if any...').
- Recommended action: clarify

**[MEDIUM] Scope — No CAN/ULC-S107 fire classification listing cited for the proposed assembly. OBC 3.1.15.2 requires a listed assembly. While 60 mil TPO over polyiso + 1/4" gypsum cover board is a standard Class A configuration for major manufacturers, the specific listing number tied to the as-installed assembly is not stated.**
- Citation: OBC 3.1.15.2; CAN/ULC-S107 (fixture 01 §1.1).
- Evidence: KEY SPECIFICATIONS table lists components but no UL/ULC listing number; ATTACHMENTS reference product data sheets but no fire-classification listing is enumerated in the cover letter.
- Recommended action: clarify

**[MEDIUM] Scope — Skylight replacement and HVAC equipment modifications excluded. RFP §2.1 includes 4 skylights among the 47 penetrations to be flashed but does not require replacement. Re-flashing 28-year-old skylights without replacement is a known leak path (fixture 02 §5).**
- Citation: fixture 02 §5 (Common Scope Omissions — skylight replacement).
- Evidence: EXCLUSIONS items 4 and 5 ('Skylight replacement or major repairs', 'HVAC equipment modifications or replacements').
- Recommended action: clarify

**[LOW] Qualifications — Manufacturer ambiguity. Bid lists three manufacturer certifications (Carlisle Syntec, Firestone, Johns Manville) but does not name which manufacturer's TPO system will actually be supplied. The '20-Year NDL Warranty Sample Documentation' attachment is a sample, not a system-specific warranty letter. The named installer credential must match the supplied system for total-system NDL eligibility (fixture 04 §4); a Carlisle Certified Installer cannot install Johns Manville and obtain a JM NDL warranty.**
- Citation: —
- Evidence: MANUFACTURER CERTIFICATIONS section; ATTACHMENTS list
- Recommended action: —

**[LOW] Qualifications — Skilled Trades Ontario C of Q crew composition not disclosed. Project Team identifies Project Manager (Jennifer Morrison, 12 yrs), Site Supervisor (Tom Bakos, 18 yrs), and '3 certified roofing technicians (avg 8 yrs)'. 'Certified' here appears to refer to manufacturer certification, not Skilled Trades Ontario C of Q. The Roofer trade (no. 449A) is not compulsory in Ontario, so this is not a regulatory issue, but for an 85,000 sf Part 3 project a crew with C of Q holders is a quality-of-workmanship signal.**
- Citation: —
- Evidence: PROJECT TEAM section
- Recommended action: —

**[LOW] Qualifications — Reference contract values not disclosed. All three references provide named contact, scope size in sf, and completion year, but contract value is omitted. The comparable-project test requires project value within 0.5x to 2x the subject project's value; this dimension cannot be verified from the submission. Sizes (62K-95K sf) are comparable to the 85K subject, so the gate passes on size and recency, but a reference at materially different price-per-sqft could indicate a different scope depth.**
- Citation: —
- Evidence: REFERENCES section
- Recommended action: —

**[LOW] Qualifications — WSIB clearance certificate date not transcribed. Bid asserts WSIB account #5678901-23 in good standing with Experience Rating 0.89, but the issue/expiry date of the attached certificate is not visible in the bid narrative.**
- Citation: —
- Evidence: ATTACHMENTS list; INSURANCE COVERAGE section
- Recommended action: —

**[LOW] Qualifications — Owner-as-additional-insured and completed-operations tail unconfirmed. Bid declares CGL $5M per occurrence but does not specify whether Tenebrus Capital is named as additional insured nor the completed-operations tail length. Both are routine COI items.**
- Citation: —
- Evidence: INSURANCE COVERAGE section; COI attached but contents not transcribed
- Recommended action: —

**[LOW] Scope — No unit pricing for steel deck (per bf), wood deck (per bf), flashing (per lf), or insulation (per sqft per R-value). Allowances are flat-dollar ($12K steel, $8K wood, $18K tapered) with no rate for overruns. RFP §2.1.2 and §3.2 both contemplate unit pricing for extras.**
- Citation: fixture 02 §5 (unit-price allowances for deck replacement).
- Evidence: PRICE BREAKDOWN allowance lines are flat amounts; OPTIONAL ADD-ONS table omits per-bf or per-sqft rates for deck/insulation extras.
- Recommended action: clarify

### Summit Contracting Ltd.

**[CRITICAL] Warranty — 30-year NDL warranty claimed without identifying the supplying manufacturer or named system program. Bid lists Carlisle Syntec Master Installer, Firestone Premier Contractor, and GAF Master Elite certifications, but does not say which manufacturer's TPO and which warranty program (e.g., Sure-Weld 30-yr Golden Seal, EverGuard 30-yr, or Firestone equivalent) is being supplied. NDL validity depends on the actual manufacturer + installed system + certified-installer match — and 30-yr tiers require pre-installation drawing review, mid-job and final manufacturer inspection on the specific named system.**
- Citation: fixture 02 §1.3 (TPO warranty tiers: 30-yr Golden Seal requires 80 mil + Authorized Applicator + manufacturer inspection); fixture 02 §3 (manufacturer certified contractor programs); fixture 02 §4 item 1 (mismatched system components void warranty)
- Evidence: Sections 'WARRANTY' and 'MANUFACTURER CERTIFICATIONS'; Attachments list 'Product Data Sheets (80 mil TPO membrane)' and '30-Year NDL Warranty Sample Documentation' but the body of the bid never names the manufacturer of the system being installed.
- Recommended action: clarify

**[HIGH] Materials — Wind uplift design basis not stated. Bid cites '130 mph wind speed coverage' as a warranty term but does not provide a CSA A123.21 dynamic uplift listing for the as-proposed assembly, FM 1-29 design pressures for field/perimeter/corner zones, NBC Part 4 wind-load calculation, or fastening/adhesion schedule keyed to zone. A roof of this height and exposure (multi-level industrial) requires zone-by-zone uplift design.**
- Citation: fixture 01 §1.2 (CSA A123.21 wind uplift, FM 1-29 zones); fixture 02 §4 item 4 ('No wind uplift design basis')
- Evidence: §WARRANTY — '130 mph wind speed coverage' is the only wind reference; no q-value, no zone pressures, no listed assembly identifier appears in the bid body or attachments list.
- Recommended action: clarify

**[HIGH] Safety — Site-specific fall protection plan is generic. Bid confirms COR certification, CRSP-certified safety officer, annual fall protection training, and dedicated safety officer for >50,000 sf projects — but does not identify named anchor points, anchor type/load rating (≥22.2 kN per O. Reg. 213/91), harness/lanyard/SRL inventory, control-zone demarcation per §26.3(6) for built-up roof work, or a written rescue plan (which is mandatory under §26.1 for any fall-arrest system).**
- Citation: O. Reg. 213/91 §§26.1–26.9; fixture 01 §3.3 (fall arrest hierarchy and rescue plan requirement); fixture 01 §3.4 (guardrails/control zone)
- Evidence: §SAFETY PROGRAM — 'Fall protection training for all workers (updated annually). Dedicated safety officer on-site for projects over 50,000 sq ft.'; ATTACHMENTS lists 'Safety Program Manual (excerpt)' but no project-specific fall protection plan or rescue plan is described in the bid body.
- Recommended action: clarify

**[MEDIUM] Qualifications — Skilled Trades Ontario Certificate of Qualification (Roofer 449A) count for the assigned crew is not declared. Bid lists '4 certified roofing technicians (average 12 years experience)' but does not state how many hold the 449A C of Q. Per fixture 04 §4 the trade is voluntary in Ontario, but a Part 3 occupied pharmaceutical re-roof warrants explicit confirmation of 449A coverage on the working crew.**
- Citation: —
- Evidence: Bid §PROJECT TEAM and §PRICE BREAKDOWN ('Labour (certified installers, phasing premium)').
- Recommended action: —

**[MEDIUM] Qualifications — TPO membrane manufacturer for the proposed 30-year NDL warranty is not explicitly named. Bid claims three top-tier manufacturer certifications (GAF Master Elite, Carlisle Syntec Master Installer, Firestone Premier Contractor) but does not specify which manufacturer's TPO system is being supplied. NDL warranty validity depends on the actual manufacturer + system + certified-installer match per fixture 02 §1.**
- Citation: —
- Evidence: Bid §WARRANTY and §MANUFACTURER CERTIFICATIONS; ATTACHMENTS list shows '30-Year NDL Warranty Sample Documentation' (sample, not the named program).
- Recommended action: —

**[MEDIUM] Qualifications — Surety/bonding documentation for the §9.2 performance bond (50%) and labour & material bond (50%) is absent from the bid. No agreement-to-bond letter, consent of surety, or named surety is provided. Per skill calibration this is a needs_clarification at submission stage but must be cured before contract execution on this Construction Act / Part 3 project.**
- Citation: —
- Evidence: Bid ATTACHMENTS list does not include a surety letter or agreement to bond; no surety is named in the cover letter.
- Recommended action: —

**[MEDIUM] Scope — Hazardous-material boundary is ambiguous. Bid states 'minor ACM can be handled under our existing certification' but full abatement would be extra. The threshold between 'minor' and 'full' is not defined, and Type 1/2/3 classification per O. Reg. 278/05 is not stated. RFP §2.3 acknowledges potential ACM and lead from the 1998 transition period.**
- Citation: O. Reg. 278/05; fixture 01 §4.2 (ACM Type 1/2/3 classification, MLITSD notification for Type 3)
- Evidence: §HAZARDOUS MATERIALS APPROACH — 'If ACM confirmed: We hold appropriate licensing for limited abatement. Full abatement would be extra, but minor ACM can be handled under our existing certification.'
- Recommended action: clarify

**[MEDIUM] Materials — Fire classification listing not provided. Bid does not cite a CAN/ULC-S107 Class A/B/C listing for the as-proposed assembly (membrane + insulation + cover board + steel deck). RFP also does not require a specific class, but for an 85,000 sf OBC Part 3 industrial building this is a documentation gap that should be closed before contract.**
- Citation: fixture 01 §1.1 (CAN/ULC-S107 listing must match as-proposed assembly); OBC 3.1.15.2
- Evidence: Bid 'KEY SPECIFICATIONS' table and 'PRICE BREAKDOWN' do not mention a CAN/ULC-S107 listing or fire class; no UL/ULC listing number cited.
- Recommended action: clarify

**[LOW] Qualifications — CRCA (Canadian Roofing Contractors Association) membership is not declared. Not mandatory under the RFP but is a positive industry-membership signal for a complex commercial Part 3 re-roof.**
- Citation: —
- Evidence: Bid does not mention CRCA in the cover letter, project team, or attachments list.
- Recommended action: —

**[LOW] Materials — No CRCA technical bulletin or named C&D recycling/diversion facility for ~150 tons of BUR/gravel tear-off waste. RFP does not require diversion targets, but a named disposal facility and weight-tracking commitment is industry best practice and would protect the owner against unauthorized dumping liability.**
- Citation: fixture 01 §4.1 (asphalt shingle disposal best practice — named facility, diversion rate, weight tracking)
- Evidence: §INCLUDED IN OUR BID PRICE — 'Daily site cleanup and debris removal included.' No facility named in bid body or attachments list.
- Recommended action: accept-with-condition

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
