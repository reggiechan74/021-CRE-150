# Exercise 1 — "The Desktop" (30 minutes)

## Part A.0 — Set Up Your CRE-150 Project (5 minutes)

The foundational step. You are creating a persistent workspace that remembers you.

**Step 1 — Create the folder** (if not already done during containerization briefing)
- Create `CRE-150-Workshop` on your desktop

**Step 2 — Elevate to a Cowork Project**
- In Cowork, click **Projects** → **New Project from existing folder**
- Select `CRE-150-Workshop`
- Paste into Project Instructions:
  > *This is my CRE-150 workshop workspace. I am learning Cowork by doing real CRE tasks. Help me practice Cowork's capabilities using commercial real estate scenarios. Always ask before taking destructive actions on my files. Never send emails or submit forms on my behalf without explicit approval.*

**Step 3 — Create your brain.md**
- Copy `BRAIN-TEMPLATE.md` (in this folder) into your `CRE-150-Workshop` folder
- Rename to `brain.md`
- Fill in the seven short fields yourself (role, firm, portfolio, team, clients, working preferences, voice notes)
- Start a new chat inside your Project and paste:
  > *Interview me to expand each field in brain.md. Ask me follow-up questions one at a time so I can give you substantive answers. When a section feels complete, move to the next. Save the expanded file when we finish.*
- Claude iterates through your brain.md with targeted questions
- Output: a rich persona document saved inside your Project

**Success criteria:** Project created with instructions, brain.md skeleton filled in and expanded via Claude interview, file saved inside the Project folder

**Why this matters:** Everything you build today — the workspace map below, the lease review in Exercise 4, the leasing memo in Exercise 5, your custom plugin in Exercise 7 — inherits context from this single document.

---

## Part A — File System Access (10 minutes)

- Navigate to a folder you're comfortable experimenting with:
  - `~/Downloads`, OR
  - `~/Documents`, OR
  - Any subfolder within these that you don't mind reorganizing
- Start a new Cowork task scoped to that folder (inside your Project)
- Ask Claude to:
  - Rename files to a consistent naming convention
  - Sort files into logical subfolders
  - Identify and flag duplicate files
  - Flag any files in wrong subfolders
- **Review Claude's proposed changes before accepting**
- Ask Claude to generate a folder manifest summarizing every file
- Ask Claude to generate a **workspace map** — a top-level markdown file describing the folder structure and purpose of each subfolder

**Success criteria:** Organized folder structure, consistent naming, duplicate report, folder manifest document, workspace map

---

## Part B — Computer Use: Claude Controls Your Screen (~6 minutes)

*Requires Pro or Max plan. Facilitator-led demo.*

- Facilitator demonstrates on a single screen
- Participants watch and narrate what Claude is doing
- Demo task: Claude uses Computer Use mode to open the workshop folder in Finder/Explorer, locate the folder manifest from Part A, and open it in a text editor
- Claude requests permission before accessing each application

**Key takeaway:** Computer Use operates by screenshotting your desktop and interpreting what it sees. Slower than direct file access. Single-app tasks are much more reliable than multi-app workflows. This is how Claude reaches legacy CRE tools that have no API or connector.

---

## Part C — Dispatch: Remote Control From Your Phone (~9 minutes)

*Requires Pro or Max plan, macOS only*

- In Cowork sidebar, select **Dispatch**
- Scan the QR code with the Claude mobile app
- Walk away from your laptop
- From your phone, ask Claude to create a summary document of the organized deal folder from Part A and note which files were flagged as duplicates
- Return to your laptop and open the document Claude created

**Participants without Pro/Max or macOS:** Pair with someone who has the requirements. One drives, one watches.

---

## Summary: Three Interaction Modes

| Mode | What Claude Touches | Speed | Reliability | Plan |
|------|-------------------|-------|-------------|------|
| File System | Your files and folders directly | Fast | High | All paid plans |
| Computer Use | Your screen, mouse, keyboard | Slow | Moderate (single-app reliable) | Pro / Max |
| Dispatch | Your desktop from your phone | Varies | Moderate (retrieval strong) | Pro / Max (macOS) |

**What your Project + brain.md unlocks:** Persistent memory across every chat in Exercises 2–7. The workspace map from Part A becomes your navigation spine. Your brain.md evolves over the day as Exercise 2 connectors feed it real evidence.
