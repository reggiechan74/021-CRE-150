# MLS Extraction — Field Reference (34 Fields)

**Standard**: All extractions produce exactly these 34 fields. Missing values use type-appropriate defaults (0, false, "").

---

## Column Order (by decision importance)

| # | Field | Type | Header | Format |
|---|-------|------|--------|--------|
| 1 | `is_subject` | boolean | Subject Property | YES / NO |
| 2 | `address` | string | Address | Left |
| 3 | `unit` | string | Unit | Left |
| 4 | `available_sf` | integer | Available SF | `#,##0` |
| 5 | `net_asking_rent` | float | Net Rent ($/SF) | `$#,##0.00` |
| 6 | `tmi` | float | TMI ($/SF) | `$#,##0.00` |
| 7 | `gross_rent` | float | Gross Rent ($/SF) | `$#,##0.00` |
| 8 | `clear_height_ft` | float | Clear Height (ft) | `0.0` |
| 9 | `building_age_years` | integer | Building Age (yrs) | `0.0` |
| 10 | `class` | integer → string | Class | A / B / C |
| 11 | `parking_ratio` | float | Parking Ratio | `0.0` |
| 12 | `pct_office_space` | float | % Office | `0.0%` |
| 13 | `shipping_doors_tl` | integer | Ship Doors (TL) | `0` |
| 14 | `shipping_doors_di` | integer | Ship Doors (DI) | `0` |
| 15 | `power_amps` | integer | Power (amps) | `#,##0` |
| 16 | `bay_depth_ft` | float | Bay Depth (ft) | `0.0` |
| 17 | `lot_size_acres` | float | Lot Size (acres) | `0.0` |
| 18 | `hvac_coverage` | integer → string | HVAC | Y / Partial / N |
| 19 | `sprinkler_type` | integer → string | Sprinkler | ESFR / Standard / None |
| 20 | `rail_access` | boolean | Rail Access | YES / NO |
| 21 | `crane` | boolean | Crane | YES / NO |
| 22 | `occupancy_status` | integer → string | Occupancy | Vacant / Occupied |
| 23 | `trailer_parking` | boolean | Trailer Parking | YES / NO |
| 24 | `secure_shipping` | boolean | Secure Shipping | YES / NO |
| 25 | `excess_land` | boolean | Excess Land | YES / NO |
| 26 | `grade_level_doors` | integer | Grade Level Doors | `0` |
| 27 | `zoning` | string | Zoning | Left |
| 28 | `availability_date` | string | Availability Date | Left |
| 29 | `days_on_market` | integer | Days on Market | `#,##0` |
| 30 | `mls_number` | string | MLS# | Left |
| 31 | `broker_name` | string | Broker | Left |
| 32 | `client_remarks` | string | Remarks | Left (max 500 chars) |
| 33 | `reported_market` | string | Market | Left |
| 34 | `source_pdf` | string | Source PDF | Left |

---

## Parsing Rules

### Bay Depth
- Input: `"Bay Size: 55 x 52"` → extract first number → `55.0`

### Lot Size
- Input: `"543,892 Sq Ft"` → divide by 43,560 → `12.48`
- Input: `"12.5 acres"` → use directly → `12.5`

### HVAC Coverage (`hvac_coverage`)
- `"Yes"`, `"Y"`, `"100%"` → `1`
- `"Partial"`, `"Part"`, `"50%"` → `2`
- `"No"`, `"N"`, `"0%"` → `3`

### Sprinkler Type (`sprinkler_type`)
- `"ESFR"` anywhere including Client Remarks → `1`
- `"Standard"`, `"Conventional"` → `2`
- `"None"`, `"N/A"` → `3`

### Occupancy Status
- `"Vacant"`, `"Available"` → `1`
- `"Occupied"`, `"Tenant in Place"` → `2`

### Class
- `"A"` → `1`; `"B"` → `2`; `"C"` → `3`
- Excel displays as `A`, `B`, `C` (formatter converts back)

### Office Percentage
- Input: `"97% Warehouse, 3% Office"` → `0.03`
- Input: `"5% Office"` → `0.05`

### Gross Rent (derived)
- `gross_rent = net_asking_rent + tmi`

### Building Age (derived)
- `building_age_years = current_year - year_built`

---

## Subject Property Detection (priority order)

1. Keyword `"Subject"` in `client_remarks`
2. `--subject="partial address"` fuzzy match against `address` (case-insensitive)
3. Default: first property in list

Exactly one property must have `is_subject: true`.

---

## Output File Naming

**JSON**: `YYYY-MM-DD_HHMMSS_mls_extraction_<market>.json`
**Excel**: `YYYY-MM-DD_HHMMSS_mls_extraction_<market>.xlsx`

Timestamp in Eastern Time. Market name: lowercase, underscores, alphanumeric only.
Example: `2025-11-06_183047_mls_extraction_mississauga.xlsx`
