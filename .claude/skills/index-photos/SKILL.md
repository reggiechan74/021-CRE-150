---
name: index-photos
description: Create a markdown index of property photos with AI-generated descriptions. Use when you have a folder of site photos that need cataloging.
argument-hint: "[path/to/photos/folder]"
allowed-tools: Read, Write, Bash(ls*), Bash(find*), Bash(wc*), Bash(date*), Glob, Task, TaskCreate, TaskUpdate, TaskList
---

# Property Photo Indexer

Generate a markdown index file that catalogs property photos with factual, appraisal-focused descriptions for each image.

## Workflow

### Step 0: Start Timer

Start the elapsed time tracker:
```bash
source /workspaces/appraisal-automation/.claude/utils/timing.sh && start_timer "index-photos"
```

### Step 1: Scan Photo Folder

List all image and video files in the provided folder:
```bash
ls -1 "$ARGUMENTS"/*.jpg "$ARGUMENTS"/*.jpeg "$ARGUMENTS"/*.png "$ARGUMENTS"/*.JPG "$ARGUMENTS"/*.JPEG "$ARGUMENTS"/*.PNG 2>/dev/null | head -200
```

List video files:
```bash
ls -1 "$ARGUMENTS"/*.mov "$ARGUMENTS"/*.mp4 "$ARGUMENTS"/*.MOV "$ARGUMENTS"/*.MP4 "$ARGUMENTS"/*.avi "$ARGUMENTS"/*.AVI 2>/dev/null
```

### Step 2: Create Individual Tasks for Every File

**CRITICAL: Create one task per file.** If there are 100 photos and 2 videos, create 102 tasks (plus 1 for generating the index).

For each **photo file**, create a task:
```
TaskCreate:
  subject: "Describe: [filename.jpg]"
  description: "Read and describe photo: [full path to file]"
  activeForm: "Describing [filename.jpg]"
```

For each **video file**, create a task:
```
TaskCreate:
  subject: "Review: [filename.mov]"
  description: "Review video file: [full path to file]"
  activeForm: "Reviewing [filename.mov]"
```

Create a final task for generating the index:
```
TaskCreate:
  subject: "Generate photo index file"
  description: "Compile all descriptions into final markdown index"
  activeForm: "Writing index file"
```

### Step 3: Process Each Photo

For each photo task:
1. **Set task to `in_progress`**
2. Use the **Read** tool to view the image
3. Write a **factual, appraisal-focused 2-4 sentence description** (see guidelines below)
4. Store the description
5. **Set task to `completed`**

---

## Description Guidelines: Writing Appraisal-Focused Descriptions

**Your goal is to document property characteristics relevant to valuation.** Focus on building condition, materials, site improvements, functional utility, and any observable deficiencies or deferred maintenance.

### What to Describe (Appraisal-Relevant Details)

**Colors & Materials:**
- Not "painted walls" → "cream-colored painted concrete block walls with an orange accent stripe at waist height"
- Not "metal roof" → "corrugated galvanized steel roof with visible rust staining near the gutters"
- Not "flooring" → "grey sealed concrete floor showing oil stains and wear patterns from forklift traffic"

**Equipment & Brands (read labels!):**
- Not "press machine" → "Danly 250-ton mechanical stamping press with yellow safety guarding"
- Not "CNC machine" → "Takumi V22A vertical machining center with 20-position tool carousel"
- Not "electrical panel" → "Square D 400-amp main breaker panel with 30HP compressor disconnect"

**Dimensions & Quantities (estimate):**
- Not "high ceilings" → "approximately 22-foot clear height to the exposed bar joist structure"
- Not "several parking spaces" → "approximately 15 striped parking stalls on aged asphalt"
- Not "some shelving" → "four-tier pallet racking spanning roughly 60 feet along the east wall"

**Condition & Age:**
- Not "in good condition" → "recently painted with no visible damage or deferred maintenance"
- Not "worn floor" → "concrete floor with extensive surface scaling, oil penetration, and crack repairs"
- Not "old equipment" → "vintage 1980s-era press showing heavy patina but appearing operational"

**Spatial Relationships:**
- Not "near the door" → "positioned immediately left of the overhead door along the north wall"
- Not "in the corner" → "tucked into the northeast corner behind the mezzanine stairs"

**Deferred Maintenance & Deficiencies:**
- "Asphalt showing extensive alligator cracking and ponding water indicating drainage issues"
- "Roof flashing with visible rust and deterioration at parapet connections"
- "Concrete floor with spalling, oil contamination, and unrepaired crack damage"

**Functional Utility:**
- "Grade-level overhead door suitable for truck access"
- "Insufficient parking relative to building size - only 8 spaces for 25,000 SF"
- "Column spacing of approximately 40 feet allows flexible warehouse layout"

### What NOT to Describe (Avoid Artistic Language)

**DO NOT include:**
- Weather/sky descriptions ("dramatic grey winter sky", "overcast conditions")
- Reflections in puddles or glass ("mirror reflection of the building facade")
- Photographic composition ("the composition shows", "at the edge of frame")
- Atmospheric/poetic language ("dramatic", "imposing", "stretching into the distance")
- Seasonal aesthetics ("dormant grass", "bare winter trees")

**Instead, focus on:** What would an appraiser note during a site inspection? Condition, materials, dimensions, access, deficiencies, improvements.

### Condition Rating Scale (Use Consistently)

| Rating | Definition |
|--------|------------|
| **Good** | No visible deficiencies, well-maintained, no immediate repairs needed |
| **Average** | Normal wear for age, minor maintenance items only |
| **Fair** | Visible deficiencies, moderate repairs needed within 1-3 years |
| **Poor** | Significant deficiencies, major repair or replacement required |

### Handling Repetitive Photos

When multiple photos show the same feature or condition:
- **First/Key photo:** Provide full detailed description with all relevant observations
- **Subsequent similar photos:** Reference the key photo but STILL include unique physical details visible in this specific image

**Example - Key Photo (full detail):**
> "**KEY PHOTO - Rear service yard condition.** Asphalt in **Poor** condition - extensive alligator cracking covering 60%+ of surface, multiple patches, and large areas of standing water indicating base failure and drainage deficiency. **Significant deferred maintenance:** Full pavement replacement required, estimated $50,000-$75,000. Approximately 12-15 employee vehicles parked. White box truck at right indicates active shipping/receiving."

**Example - Subsequent photo (reference + unique details):**
> "Additional rear yard view - asphalt condition consistent with Photo 12. This angle shows extent of deterioration across full yard width. Standing water pooled in multiple low spots. Phragmites along railway easement at left. Adjacent industrial buildings visible beyond perimeter."

**NOT this (too stripped down):**
> ~~"Rear yard - same as Photo 12."~~

### Flagging Key Appraisal Issues

Explicitly flag these when observed:
- **Deferred Maintenance:** Estimate magnitude (Minor <$10K / Moderate $10-50K / Significant >$50K)
- **Functional Obsolescence:** Note outdated features vs. modern standards (e.g., "grade-level doors vs. modern dock-height (44-48 inches) - functional obsolescence for distribution")
- **Environmental Concerns:** Flag indicators like phragmites (wetland), staining (contamination), storage tanks, asbestos-suspect materials
- **Code/Safety Issues:** Note visible concerns (blocked exits, missing railings, etc.)

### Identifying Key Photos

Mark photos as **KEY PHOTO** when they best document:
- A significant deferred maintenance item (e.g., best view of deteriorated asphalt)
- A functional obsolescence issue (e.g., clearest view of grade-level vs dock-height doors)
- An environmental concern (e.g., phragmites indicating wetland)
- A major building system (e.g., electrical service, HVAC equipment)

Key photos get full detailed descriptions. Subsequent photos showing the same issue should reference the key photo number while adding any unique details visible in that specific image.

### Structure of a Good Description

1. **Lead with location/subject:** What is this a photo OF and WHERE on the property?
2. **Describe physical characteristics:** Materials, dimensions, condition, age indicators
3. **Note deficiencies or issues:** Deferred maintenance, damage, code concerns
4. **Identify improvements:** Equipment, fixtures, upgrades visible

### Finding the Right Balance

**Target length:** 2-4 sentences, approximately 40-60 words per photo.

**Include:**
- Specific materials and colors (grey CMU, corrugated metal, rubber bumpers)
- Dimensions and quantities (28 feet to parapet, 12-foot doors, 6 propane tanks)
- Equipment makes/models when visible (Danly press, Square D panel, Triple M Metal dumpster)
- Condition ratings with brief supporting evidence
- Cross-references to key photos for repeated conditions

**Avoid:**
- Weather, sky, or atmospheric descriptions
- Photographic composition commentary
- Redundant full descriptions of already-documented conditions
- Poetic or artistic language

**The test:** Could an appraiser who didn't visit the site understand the property's physical characteristics, condition, and any deficiencies from these descriptions alone?

### Example Descriptions (GOOD vs BAD vs TOO SPARSE)

**BAD (too vague):** "Interior manufacturing area with equipment visible."

**TOO SPARSE:** "Production floor with presses. Concrete floor. CMU walls **Fair** condition."

**GOOD:** "Main production floor approximately 8,000 SF with 20-foot clear height to exposed bar joist structure. Three mechanical stamping presses (Danly) with yellow safety guarding arranged in row. Concrete floor shows oil staining and wear patterns from forklift traffic - consistent with heavy industrial use. Painted CMU walls in **Fair** condition with minor scuffing."

---

**BAD (too vague):** "Electrical room with panels."

**GOOD:** "Electrical room with 400-amp Square D main service panel. Multiple generations of infrastructure visible with added sub-panels and bank of eight knife-blade disconnects with red handles. Hand-written labels identify circuits: '30HP Compressor', 'Can Machine', 'Air Compressor'. Adequate capacity for current industrial use. Room approximately 10x12 feet."

---

**BAD (too vague):** "Break room with tables."

**GOOD:** "Employee break room approximately 400 SF with white ceramic tile floor and 2x4 fluorescent drop ceiling. Four rectangular laminate tables with black plastic stacking chairs - seating for approximately 16 workers. Stainless steel commercial refrigerator and dual microwaves along back wall. Walls and ceiling in **Good** condition. Adequate amenity space for building size."

---

**BAD (too artistic):** "Front elevation viewed from the parking lot on an overcast winter day with dramatic sky reflecting in puddles creating a mirror image of the building."

**GOOD:** "Front elevation - single-storey CMU construction with painted light beige finish in **Good** condition. Main entrance with glass door and one 12-foot overhead door at right. Building signage 'TORONTO GUARD METALS' in dark green letters above entrance. Yellow gas meter and riser visible at corner. Asphalt parking area in **Average** condition with some cracking near entrance."

---

**BAD (too artistic):** "Railway corridor stretching dramatically into the distance under grey winter skies, with tall phragmites creating a natural buffer and the building's imposing form looming at left."

**GOOD:** "Railway spur curving along rear property boundary - active track on crushed granite ballast with wooden ties. Subject building visible at right with white/grey painted CMU exterior in **Fair** condition. Rail easement (EB387062) registered on title provides potential rail access. **Environmental note:** Dense phragmites reeds (6-8 feet tall) on both sides of corridor indicate potential wetland/TRCA regulated area."

---

**BAD (too artistic):** "Large puddle occupying the foreground reflects the grey winter sky, creating a mirror of the building facade. The composition shows the transition from active service area to undeveloped easement."

**GOOD:** "Southeast corner of rear yard - building corner with one overhead door, red scrap dumpster below, and yellow propane storage cage visible. Transition from paved service yard to unpaved easement strip at right. Tall phragmites reeds (7-8 feet) mark rail corridor boundary - **environmental note per Photo 3**. Standing water in settled asphalt confirms drainage issues (Photo 12)."

---

### For Blurry or Poor Quality Photos

Still describe what you CAN see, then note the quality issue:
- "Appears to show interior manufacturing equipment, but severe motion blur renders details indiscernible. A yellow object (possibly a press or crane) is faintly visible at center frame. Photo not usable for documentation purposes."

### Step 4: Process Each Video

For each video task:
1. **Set task to `in_progress`**
2. Spawn a **subagent** using the Task tool with `subagent_type: "general-purpose"`:
   ```
   Task tool parameters:
     subagent_type: "general-purpose"
     description: "Review video [filename]"
     prompt: |
       Review this property video file and provide a 3-5 sentence appraisal-focused description:

       Video path: [full path to video]

       Use the Read tool to view the video. Describe:
       - What areas of the property are shown (specific rooms, spaces, features)
       - Building/site conditions observed (materials, maintenance, deficiencies)
       - Key improvements visible (equipment, fixtures, upgrades)
       - Approximate dimensions or areas if determinable

       Focus on facts relevant to property valuation. Avoid artistic or atmospheric language.
       Return ONLY the description text, nothing else.
   ```
3. Store the description from subagent
4. **Set task to `completed`**

**Note:** Launch video subagents in parallel when possible to improve performance.

### Step 5: Generate Index File

1. **Set "Generate photo index file" task to `in_progress`**
2. Create a markdown file with the photo index using the template below

**Output Location:** `/workspaces/appraisal-automation/Output/`
**Filename Format:** `[TIMESTAMP]_Photo_Index_[FolderName].md`
**Timestamp:** `TZ='America/New_York' date '+%Y-%m-%d_%H%M%S_EST'`

3. **Set task to `completed`**

## Output Template

```markdown
# Photo Index: [Property/Folder Name]
**Generated:** [Date and Time]
**Total Photos:** [N] images
**Source Folder:** [Path]

---

## Photo Inventory

| # | Filename | Description |
|---|----------|-------------|
| 1 | [filename1.jpg] | [2-4 sentence appraisal-focused description] |
| 2 | [filename2.jpg] | [2-4 sentence appraisal-focused description] |
| 3 | [filename3.jpg] | [2-4 sentence appraisal-focused description] |
...

---

## Video Inventory

| # | Filename | Description |
|---|----------|-------------|
| 1 | [video1.mov] | [3-5 sentence appraisal-focused description] |

---

## Photo Categories

### Exterior Views
- [List filenames showing building exterior]

### Interior Views
- [List filenames showing interior spaces]

### Site/Parking
- [List filenames showing parking, landscaping, site access]

### Loading/Shipping
- [List filenames showing loading docks, shipping areas]

### Details/Other
- [List filenames showing signage, equipment, details]

---

*Index generated by Claude Code Photo Indexer*
```

### Step 6: End Timer and Append Elapsed Time

After writing the index file, stop the timer and append elapsed time:
```bash
source /workspaces/appraisal-automation/.claude/utils/timing.sh && end_timer "index-photos"
```

Then append the `$ELAPSED_TIME_TEXT` to the end of the generated markdown file.

## Technical Notes

1. **Batch Processing:** Process photos in batches of 10-15 at a time to manage context, but each photo still gets its own task.

2. **File Types:** Support common image formats: `.jpg`, `.jpeg`, `.png` (and uppercase variants).

3. **Naming Patterns:** Photos are often timestamped (e.g., `2020-01-28 15.00.01.jpg`). Extract dates if useful for sorting.

4. **Duplicates:** Note if photos appear to be duplicates or very similar angles.

5. **Quality Issues:** Still describe what's visible, then note the quality issue.

6. **Read Labels:** Always try to read any visible text - equipment brands, warning signs, room numbers, company names, capacity ratings, etc.
