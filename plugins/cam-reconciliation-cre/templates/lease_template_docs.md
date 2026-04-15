# Lease Template

Provide one object per tenant in `leases.json` or YAML converted to JSON before ingestion.

Required fields:
- `tenant_id`
- `tenant_name`
- `unit_label`
- `rsf`
- `pool` (`office` or `retail`)
- `pro_rata_of_pool`
- `lease_type`

Optional lease structures:
- `annual_prebilled`
- `base_year`
- `cap`
- `excluded_categories`
- `specific_exclusions`
- `clause_refs`

Use `specific_exclusions` when an exclusion applies only to a specific raw GL category or invoice pattern. Use `excluded_categories` when the lease excludes an entire normalized category such as `utilities` or `repairs_maintenance`.

For `specific_exclusions`, set `treatment` to:
- `exclude_share` to remove only that tenant's pooled share and reallocate it across the remaining eligible tenants.
- `direct_bill_to_matching_tenant` to bypass pooled CAM entirely and bill the matched line 100% to the tenant outside the shared pool.
