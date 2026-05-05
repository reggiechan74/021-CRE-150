# Teaching a CRE Domain Expert to Build a Lease Abstraction Skill

**Target Audience:** Lease administration professional with deep domain expertise but no agentic engineering background.

**Goal:** Take them from "I abstract leases manually" to "I built a skill that abstracts leases automatically."

---

## The One-Sentence Framing

> **Skill creation is fundamentally the encoding of domain knowledge into a form that an AI can execute.**

Everything else is implementation detail.

You are not teaching them to code. You are teaching them to **articulate their expertise so precisely that a very literal-minded junior could execute it without asking any questions.** The AI is that junior. The skill is the instruction manual.

---

## Where to Begin: Start With Their Workflow, Not the Technology

Don't start with:
- ❌ "Here's how agents work"
- ❌ "Let me explain context windows and tokens"
- ❌ "This is the technical architecture"

Start with:
- ✅ "Walk me through how you abstract a lease today"
- ✅ "What do you look for first? Second? Third?"
- ✅ "What mistakes do juniors make when they try to help you?"
- ✅ "What takes the most time? What's the most boring part?"

**Why:** They already have the domain knowledge. Your job is to help them see that **building a skill is documenting their expertise in a way an AI can execute it.**

---

## Phase 1: Map the Human Workflow (No Code Yet)

### Exercise 1: Think Aloud Protocol

Give them a lease and ask them to abstract it while narrating every decision:

```
"I'm looking at page 1... I need to find the parties. The header says
'Landlord: ABC Properties' but wait, there's an assignment clause on
page 47 that changed the landlord to XYZ Trust. I need to note both
and flag the assignment date..."
```

**Capture:**
- What sections do they read first?
- What do they skip on first pass?
- When do they re-read something?
- When do they say "hmm, that's odd"?
- When do they write something down vs. remember it?

### Exercise 2: The Checklist They Already Have

Most lease administrators have a mental or physical checklist:

```
□ Parties identified
□ Premises address confirmed
□ Commencement date found
□ Expiry date calculated
□ Base rent extracted
□ Escalation mechanism identified
□ Renewal options counted
□ Critical dates listed
...
```

**This is their Domain Data Dictionary in embryonic form.**

### Exercise 3: Edge Cases and "It Depends" Moments

Ask: *"What makes a lease hard to abstract?"*

They'll tell you:
- "When Schedule G contradicts the main body"
- "When there are multiple amendments"
- "When rent is 'market rate' with no formula"
- "When the commencement date is 'TBD' or tied to an event"

**These are your validation rules and status tags.**

---

## Phase 2: Translate Workflow to Skill Structure

### Concept 1: The Skill Is a Recipe

**Analogy:** A lease abstraction skill is like a recipe card.

| Recipe Component | Skill Equivalent |
|------------------|------------------|
| Ingredients list | Input documents (lease PDF, amendments) |
| Step-by-step instructions | Prompt telling the AI what to do |
| "Cook until golden brown" | Quality checks ("verify parties are correct") |
| Serving suggestions | Output format (Markdown table, JSON) |

**Teaching point:** You're not "coding" — you're writing down your recipe so someone else (the AI) can follow it.

### Concept 2: The Output Schema Is Your Abstract Template

**Show them:** A blank lease abstract template with 25 sections.

**Say:** *"This template has 258 boxes to fill in. Every lease, same boxes. The skill's job is to fill every box, or write 'Not Found' if the lease doesn't have that term."*

**This is the Domain Data Dictionary — but don't call it that yet.** Call it "the template."

### Concept 3: Status Tags Are Quality Flags

**Analogy:** Think of a traffic light system.

| Status | Meaning | Traffic Light |
|--------|---------|---------------|
| `FACT` | I found this exact term in the lease | 🟢 Green — go, it's verified |
| `INFERENCE` | I had to interpret/derive this | 🟡 Yellow — review if confidence is low |
| `MISSING` | This term is not in the lease | ⚪ Gray — not applicable or omitted |
| `CONFLICT` | Two clauses contradict | 🔴 Red — stop, human must decide |

**Teaching point:** These aren't technical jargon — they're the same flags you'd use when training a junior abstractor.

---

## Phase 3: Introduce the Technical Pieces (One at a Time)

### Technical Concept 1: The Prompt Is the Instruction Sheet

**Show them:** A simple prompt structure.

```
You are a lease abstraction specialist. Your job is to extract terms
from a commercial lease and fill in the template below.

RULES:
1. Every field must be filled or marked "Not Found"
2. Quote the exact lease language for every fact
3. Include page number and clause reference
4. If two clauses contradict, flag both — don't pick one
5. If you're not sure, say so and explain why

TEMPLATE:
[Insert 25-section template]
```

**Say:** *"This is you, telling a very detail-oriented junior exactly how to do the job. The junior is the AI. The instruction sheet is the prompt."*

---

### Critical Insight: AI Knows Generic Leases, But Doesn't Know *Your* Firm's Template

**The AI has been trained on:**
- Generic lease structures and common clauses
- Standard legal terminology
- General CRE concepts (rent, term, parties, options, etc.)
- Common legal patterns across many documents

**The AI has NOT been trained on:**
- Your firm's specific abstract template
- Your client's reporting requirements
- Your internal approval workflows
- Your edge case handling rules (e.g., "When rent is TBD, flag for partner review")
- Your risk tolerance (what to escalate vs. what to note quietly)
- **Your firm's schedule naming conventions** (e.g., Schedule G = Special Provisions — but another firm might use Schedule H, or no letter at all)
- **Your particular corpus of lease agreements** — the AI has never seen your portfolio's leases, their quirks, or common amendments
- **Your downstream requirements** — what systems consume your abstract data (Yardi, MRI, custom reports) and what field formats they expect

**Why this matters:** You're not teaching the AI what a lease is. You're teaching it **how your firm abstracts leases** — including which schedules matter, what they're called, and how to handle contradictions.

| Generic Knowledge (AI Has) | Your Firm's Knowledge (You Provide) |
|----------------------------|-------------------------------------|
| What a renewal option looks like | Which renewal deadlines are P1 vs. P2 for your clients |
| What base rent is | How you handle rent abatements in rent calculations |
| That leases have special provisions | That *Schedule G* is where Special Provisions live in your templates — and that Schedule G always trumps main body |
| What an assignment clause is | That you need to track the full assignment chain, not just current landlord |

**The skill encodes the difference.**

---

### Technical Concept 2: Context Window Is "How Much the AI Can Read at Once"

**Analogy:** Think of it like reading a book with a narrow highlighter.

- A normal conversation = reading a few pages at a time
- A 200k-token context = the entire lease, all at once

**Why it matters:** "If the AI can read the whole lease at once, it can cross-reference Schedule G against the main body. If it can only read a few pages, it'll miss contradictions."

### Technical Concept 3: Subagents Are Specialist Colleagues

**Analogy:** You wouldn't ask one person to:
1. Read the lease
2. Extract financial terms
3. Extract legal terms
4. Build the critical dates calendar
5. Format the output
6. Validate quality

**Instead:** You delegate.

| Subagent | Role |
|----------|------|
| Extraction agent | Reads the lease, fills the template |
| Critical dates agent | Focuses only on dates and deadlines |
| Validation agent | Checks the work for errors |

**Say:** *"A subagent is like asking a colleague to handle one part of the job. You give them clear instructions, they come back with results."*

### Technical Concept 4: The Output Contract Is "What Goes Into Yardi"

**Show them:** A JSON field mapping to Yardi/Argus.

```json
{
  "parties.landlord.name": "ABC Properties Inc.",
  "premises.area.rentableAreaSqFt": 100000,
  "term.commencementDate": "2024-01-01"
}
```

**Say:** *"Remember how you said you have to re-type everything into Yardi? This JSON is what you'd paste directly into Yardi's import tool. The skill produces this automatically."*

---

## Phase 4: Build the Skill Together (Hands-On)

### Step 1: Write the "What" Before the "How"

**Document:** What the skill should do (in plain English).

```
The skill should:
1. Read the lease PDF
2. Identify if it's Office or Industrial
3. Extract all 25 sections from the template
4. Flag any contradictions between Schedule G and main body
5. Generate a critical dates table
6. Save output to Reports folder
```

**Don't worry about:** Tool syntax, JSON schema, prompt engineering.

### Step 2: Define Success Criteria (The "Done" Checklist)

**Ask:** *"How do you know an abstract is complete and correct?"*

They'll say things like:
- "All 258 fields are filled or marked N/A"
- "Parties are correctly identified — not swapped"
- "Rent numbers match what's in the lease exactly"
- "Critical dates are all there — especially renewal deadlines"

**This becomes your validation rules.**

### Step 3: Identify Failure Modes (What Not to Do)

**Ask:** *"What are the worst mistakes an abstractor could make?"*

They'll tell you:
- "Swapping landlord and tenant"
- "Missing a renewal deadline"
- "Using the wrong currency"
- "Making up a number when it's not in the lease"

**This becomes your AutoFail conditions.**

### Step 4: Iterate on the Prompt Together

**Start with:** Their instructions in plain English.

```
"Find the landlord name. It's usually on page 1, but check for
assignments later in the lease. Quote it exactly."
```

**Refine to:** Structured prompt language.

```
RULE: Extract landlord.name from lease.
- Search page 1 first (typically in header or preamble)
- Search for assignment clauses (typically Section 12 or 13)
- If assignment found, use assigned landlord, note original
- Status: FACT with verbatim quote and page reference
```

**Do this together — they learn prompt engineering by doing, not by lecture.**

---

## Phase 5: Test and Debug (The "Training the Junior" Phase)

### Test Case 1: The Easy Lease

**Use:** A clean, standard office lease.

**Expected:** Skill extracts everything correctly.

**If it fails:** "Okay, the AI missed the renewal option. How would you tell a junior to not miss this next time? Write that instruction down."

### Test Case 2: The Messy Lease

**Use:** A lease with amendments, assignments, and Schedule G overrides.

**Expected:** Skill flags contradictions and missing info.

**If it fails:** "The AI didn't catch the Schedule G override. What clue would you look for? Add that to the instructions."

### Test Case 3: The Edge Case

**Use:** A lease with unusual terms (TBD dates, market rent, co-tenancy clauses).

**Expected:** Skill marks uncertain fields as `INFERENCE` with low confidence.

**If it fails:** "The AI guessed instead of flagging uncertainty. What rule would prevent that?"

**Teaching point:** Debugging a skill is like training a junior. You don't rewrite the whole instruction manual — you add specific guidance for the edge case.

---

## What You Need to Teach (Curriculum Summary)

| Topic | How to Teach It | Analogy |
|-------|-----------------|---------|
| **Workflow mapping** | Think-aloud protocol | "Show me how you do it today" |
| **Output schema** | Show their existing abstract template | "Same 258 boxes for every lease" |
| **Status tags** | Traffic light system | 🟢🟡🔴 Green/yellow/red flags |
| **Prompts** | Instruction sheet for a junior | "Tell the AI exactly what you'd tell a trainee" |
| **Context window** | How much the AI can read at once | "Reading the whole book vs. a few pages" |
| **Subagents** | Delegating to specialists | "Ask a colleague to handle one part" |
| **Validation rules** | Success criteria from their experience | "How do you know it's done right?" |
| **AutoFail conditions** | Worst mistakes to avoid | "What would get a junior fired?" |
| **Output formats** | Yardi/Argus import templates | "What goes into the system" |

---

## What NOT to Teach (At Least Not Initially)

| Topic | Why Skip It |
|-------|-------------|
| Token counts and context limits | Abstract concept; "how much the AI can read" is enough |
| JSON schema syntax | They care about the fields, not the syntax |
| Agent tool API | They care about delegation, not the function signature |
| Embedding vectors | Irrelevant to their mental model |
| Temperature and sampling | They care about consistency, not the knob |
| RAG vs. fine-tuning | Implementation detail, not a user concern |

**Teach these later, if they ask "how does this work under the hood?"**

---

## Sample First Session (2 Hours)

| Time | Activity |
|------|----------|
| 0–15 min | "Walk me through your last lease abstraction" (listen, don't interrupt) |
| 15–30 min | "What are the 10 most important fields? What mistakes do people make?" |
| 30–60 min | Hands-on: They abstract one lease while narrating; you take notes |
| 60–75 min | Break |
| 75–90 min | Show them: "Here's what I heard. This is the checklist. This is the template." |
| 90–105 min | Introduce: "A skill is this checklist, written so an AI can follow it." |
| 105–120 min | Together: Write the first draft of the prompt (in plain English, not code) |

**End of session deliverable:** A one-page document that says:
- What the skill should do (5 bullets)
- What the output looks like (their template)
- What mistakes to avoid (5 AutoFail conditions)

**Next session:** Turn that into a working skill.

---

## Success Indicators

You'll know they're ready to build when they:

- ✅ Say things like "The AI needs to check Schedule G for overrides" (delegating tasks)
- ✅ Catch themselves saying "I'd look for..." and rephrase to "The skill should look for..."
- ✅ Ask "How do I tell it to..." instead of "Can it..."
- ✅ Start thinking in edge cases: "What if there are two renewal clauses?"

You'll know they're not ready when they:

- ❌ Ask "Does the AI understand legal language?" (anthropomorphizing)
- ❌ Say "Just make it work like me" (can't articulate the workflow)
- ❌ Get overwhelmed by technical jargon (back up, use analogies)

---

## Bottom Line

**Start with their expertise. Translate it to instructions. Introduce technology as the tool that executes those instructions.**

The goal isn't to make them an agentic engineer. The goal is to make them a **skill author** — someone who can encode their domain knowledge into a form an AI can execute.

You're not teaching them to code. You're teaching them to articulate what they already know so precisely that a very literal-minded junior (the AI) could execute it without asking questions.

Everything else is implementation detail.
