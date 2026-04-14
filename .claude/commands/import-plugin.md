Import a skill, command, or script package from an external source into a new plugin in this repository.

## Arguments

`$ARGUMENTS` — source (GitHub URL or local path) plus optional flags:
- `--name <plugin-name>` — override the derived plugin name (kebab-case)
- `--version <version>` — initial version (default: `1.0.0`)

## Step 0 — Resolve Context

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
```

Parse `$ARGUMENTS`: extract `source`, `--name` (default: derive from source filename/directory in kebab-case), `--version` (default: `1.0.0`).

Set:
- `PLUGIN_NAME` — kebab-case name
- `PLUGIN_ROOT` = `${REPO_ROOT}/plugins/${PLUGIN_NAME}`

Abort with a clear message if `${PLUGIN_ROOT}` already exists.

## Step 1 — Fetch Source

If `source` is a GitHub URL: use WebFetch to read the command/skill `.md`, any `.py` scripts, `.json` schemas, and reference `.md` docs. Enumerate what was fetched (file names, line counts, types).

If `source` is a local path: read the file or directory with Read/Glob. Identify the same file types.

## Step 2 — Plan (show before writing)

Present a plan to the user:
- Plugin name, version, source
- Files to be created
- Whether the SKILL.md requires subagent dispatch — apply the trigger checklist from `cowork_lessons_learned.md`
- Scripts that need `cd "${SCRIPTS_DIR}"` before execution (sibling imports)
- Any hardcoded paths in scripts that need replacing with `Path(__file__).parent / "filename"`

Wait for user confirmation before proceeding.

## Step 3 — Create Plugin

Use `plugins/mcda-lease-comparison/` as the reference for all structure and formatting:
- Directory layout, `plugin.json`, `SKILL.md`, `README.md`, `CHANGELOG.md`

Read `cowork_lessons_learned.md` and apply **all four lessons** to the new SKILL.md:
- Lesson 1: subagent dispatch if the pipeline is context-heavy
- Lesson 2: distinct delimiters at each nesting level (`---` outer, `===` inner)
- Lesson 3: validate the intermediate artifact before running downstream steps
- Lesson 4: embed only operational lookup tables (~150 lines) in the subagent prompt; keep strategy, communication language, and interpretation narrative in the primary SKILL.md

Copy scripts to `${PLUGIN_ROOT}/skills/${PLUGIN_NAME}/scripts/` without renaming — preserve import chains.

## Step 4 — Update Metadata

**marketplace.json** (three changes — all three are required):
1. Add the new plugin entry under `"plugins"`
2. Bump `metadata.version` by one patch increment (e.g. `0.5.0` → `0.6.0`)
3. Extend `metadata.description` to include the new plugin

**Repo README.md** (three changes — all three are required):
1. Increment the plugins count badge (e.g. `plugins-4` → `plugins-5`)
2. Add a version badge for the new plugin
3. Add a `### \`${PLUGIN_NAME}\` — v${VERSION}` section with description, trigger phrases, and usage examples

## Step 5 — Validate

```bash
python3 -c "
import json, os, sys
root = '$(git rev-parse --show-toplevel)'
errors = []
plugin = '${PLUGIN_NAME}'
if not os.path.exists(f'{root}/plugins/{plugin}/.claude-plugin/plugin.json'):
    errors.append('Missing plugin.json')
if not os.path.exists(f'{root}/plugins/{plugin}/skills/{plugin}/SKILL.md'):
    errors.append('Missing SKILL.md')
m = json.load(open(f'{root}/.claude-plugin/marketplace.json'))
if plugin not in [p[\"name\"] for p in m[\"plugins\"]]:
    errors.append('Not in marketplace.json')
if errors:
    [print(f'ERROR: {e}') for e in errors]; sys.exit(1)
print(f'OK — {len(m[\"plugins\"])} plugins in marketplace, version {m[\"metadata\"][\"version\"]}')
"
```

## Step 6 — Report

```
IMPORT_RESULT
plugin: ${PLUGIN_NAME}
version: ${VERSION}
source: ${source}
files_created: [list]
marketplace_version: [bumped version]
subagent_dispatch: yes/no
lessons_applied: [list]
warnings: [any issues]
```
