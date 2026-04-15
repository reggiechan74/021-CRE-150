---
description: Explain a tenant charge or a specific GL line from an allocated CAM manifest
argument-hint: "<allocated_manifest.json> <tenant-id-or-line-id>"
---

# /cam-explain

1. Load the allocated manifest.
2. If the target matches a `tenant_id`, use the `cam-explain` skill's tenant drill-in mode.
3. If the target matches a `line_id`, use the GL-line drill-in mode.
4. Prefer the manifest's stored `math_trace`, `exclusions_applied`, `base_year_adjustment`, `cap_adjustment`, and `citations`.

If the target cannot be found, say so directly and list the available tenant IDs or line IDs closest to the request.
