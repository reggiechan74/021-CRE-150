# Daily Priority + Time-Blocking — Scheduled Task Prompt

## Overview

Use this prompt with Claude Cowork's **Scheduling** feature to automate a daily briefing that:
- Reviews email from the past 24 hours
- Checks your calendar for today and the week ahead
- Prioritizes what needs actioning
- Delivers a time-blocked daily plan to a file inside your Project each morning (with optional phone delivery via Dispatch)

Claude **reads and recommends**. You decide what to reply to, accept, or decline.

Terminology note: **Scheduling** is the Cowork feature that runs a prompt on a recurring schedule (e.g. every weekday at 7:30 AM). **Dispatch** is a separate feature that pairs your phone with your desktop Cowork session so output can be delivered to your phone and you can send tasks back from your phone. This template uses Scheduling; Dispatch is optional and only used for phone delivery of the briefing.

---

## Prerequisites

1. **Gmail** and **Google Calendar** connectors enabled in Cowork Settings → Connectors
2. Your work preferences filled in below
3. (Optional) **Dispatch** paired with your phone via QR code — only required if you want phone delivery of the briefing; otherwise the briefing is written to a file inside your Project

---

## Your Work Preferences

Fill this in before using the prompt. Be honest about your actual patterns, not aspirational ones.

```markdown
### My Work Preferences

**Peak Focus Hours (deep work):** [e.g., 10:00 AM – 12:00 PM]

**Admin Hours (email, calls, light tasks):** [e.g., 8:30 – 10:00 AM, 3:00 – 5:00 PM]

**No Heavy Work Zones:** [e.g., 12:00 – 2:00 PM, after 5:00 PM]

**Meeting Preferences:** [e.g., cluster on Tue/Thu, no meetings before 10 AM]

**Task Duration Defaults:**
- Email triage: 30 min
- Document review: 60 min
- Financial analysis: 90 min
- Phone calls: 30 min

**Hard Stops:** [e.g., Lunch 12:00 – 1:00 PM, leave by 6:00 PM]

**Energy Patterns:** Morning [HIGH/MED/LOW] · Post-lunch [HIGH/MED/LOW] · Late afternoon [HIGH/MED/LOW]
```

---

## The Prompt

Copy everything in the code block below into a Cowork scheduled task. Paste your filled-in work preferences where indicated.

```markdown
# DAILY PRIORITY + TIME-BLOCKING TASK

You are my executive assistant. Run this every weekday at 7:30 AM.

## Context

**Today's Date:** [auto-fill from system]

**My Work Preferences:**
[PASTE YOUR FILLED-IN WORK PREFERENCES HERE]

**Connectors:** Gmail (read only), Google Calendar (read only)

---

## Task 1: Review Calendar

Query Google Calendar for today and the rest of the week. Then:

- List today's meetings (time, title, location, attendees)
- Summarize the week: meeting count and hours per day; flag days >4 hours of meetings
- Identify today's available time blocks and classify each:
  - 🔵 DEEP WORK — matches peak focus hours
  - 🟢 ADMIN — matches admin hours
  - 🟡 FLEXIBLE — neutral
  - 🔴 RECOVERY — no heavy work

Output:
```
## Today's Calendar — [Date]

### Scheduled Meetings
| Time | Event | Location | Notes |
|------|-------|----------|-------|

### Week Ahead
| Day | Meetings | Hours | Status |
|-----|----------|-------|--------|

### Available Time Blocks Today
| Time | Duration | Energy Match |
|------|----------|--------------|
```

---

## Task 2: Review Email

Search Gmail for the past 24 hours (`in:inbox newer_than:1d -label:promotions -label:social`).

Classify each email:

**Priority:**
- 🔴 URGENT — action today (tenant emergencies, deal deadlines, legal/compliance)
- 🟡 IMPORTANT — action within 48 hours (broker inquiries, vendor proposals)
- 🟢 ROUTINE — action this week or delegate
- ⚪ LOW — read/archive/batch

**Action Type:** 📧 Reply · 📋 Review · 📞 Call · 📊 Analysis · 🗓️ Schedule · 📁 File · 🔄 Delegate

**CRE Context:** Tenant · Lease · Financial · Market · Vendor · Legal · Internal

Output:
```
## Email Summary — Past 24 Hours

### 🔴 URGENT
| From | Subject | Action | Context | Est. Time |

### 🟡 IMPORTANT
| From | Subject | Action | Context | Est. Time |

### 🟢 ROUTINE
| From | Subject | Action | Context | Est. Time |

### ⚪ LOW
| From | Subject | Notes |

### Stats
Total: [n] · Urgent: [n] · Important: [n] · Routine: [n] · Low: [n]
Estimated action time: [min]
```

Do **not** draft replies. Just flag what needs one.

---

## Task 3: Build Time-Blocked Plan

Match prioritized emails to available blocks using these rules:

1. Deep work tasks → 🔵 DEEP WORK blocks only
2. Admin tasks → 🟢 ADMIN blocks preferred
3. No tasks in 🔴 RECOVERY blocks
4. Urgent emails scheduled today; important today or tomorrow
5. Respect buffer time and hard stops

Output:
```
## Time-Blocked Plan — [Date]

### Morning
| Time | Block | Task | Priority |

### Lunch
| Time | Block | Task |

### Afternoon
| Time | Block | Task | Priority |

### Summary
Urgent scheduled: [n] · Important: [n] · Routine: [n]
Focused work: [hrs] · Meetings: [hrs] · Admin: [hrs]
```

If tasks exceed capacity:
```
### ⚠️ Overflow
| Task | Priority | Reason | Suggested Day |
```

If conflicts detected (overloaded day, no deep work block, urgent tasks without time):
```
### ⚠️ Conflicts / Decisions Needed
| Issue | Details | Recommended Action |
```

---

## Task 4: Generate Daily Briefing

Create the summary for delivery (to file and optionally to phone via Dispatch):

```
# Daily Briefing — [Date]

## Today at a Glance
- Meetings: [n] ([hrs] hrs)
- Focused work blocks: [n] ([hrs] hrs)
- Priority level: 🔴 HIGH / 🟡 MEDIUM / 🟢 LIGHT

## Your Top 3 Priorities
1. [task] — [time]
2. [task] — [time]
3. [task] — [time]

## Energy Match
Morning: [level] → [task type]
Afternoon: [level] → [task type]

## ⚠️ Watch-Outs
- [conflicts, overloaded periods, boundary risks]

## Full Schedule
[time-blocked plan from Task 3]

## Email Summary
🔴 Urgent: [n] · 🟡 Important: [n] · 🟢 Routine: [n]

---

Reply "approve" or tell me what to adjust.
```

---

## Output Instructions

1. Write the Daily Briefing to `daily-briefings/YYYY-MM-DD.md` inside this Project. If Dispatch is paired with my phone, also send the summary section (Top 3 Priorities + Energy Match + Watch-Outs) to my phone.
2. Wait for my response. Do not take any action on emails or calendar on my behalf.
3. If I approve: confirm "Plan approved — I'll check in at 5 PM for wrap-up."
4. If I request changes: adjust and re-send.

---

## Task 5: End-of-Day Wrap-Up (5:00 PM)

Send:
```
## End-of-Day Wrap-Up — [Date]

1. How did today go? [1–5]
2. What got done?
3. What didn't?
4. Any surprises?

## Tomorrow Preview
- Meetings: [n] ([hrs] hrs)
- Deep work blocks: [n]
- Carrying over: [tasks]

## One Win from Today
[acknowledge something that went well]

Reply with your check-in, or say "skip".
```

---

## Scheduling

- **Frequency:** Weekdays
- **Morning briefing:** 7:30 AM
- **Wrap-up:** 5:00 PM

If a connector fails, notify me and retry once after 10 minutes.
If my calendar shows "Out of Office" all day, skip the briefing and ask if I want a light version.
```

---

## Setup Steps

1. **Test run:** Paste the full prompt into Cowork and say *"Run this once now as a test."* Review the output.
2. **Adjust preferences** based on whether priorities and time blocks feel right.
3. **Schedule recurring:** In Cowork → Scheduling, create two scheduled tasks (weekdays):
   - Morning briefing at 7:30 AM
   - Wrap-up at 5:00 PM
4. **First week:** Review each briefing, note what's off, and tune preferences.

---

## Example Output

**7:30 AM Morning Briefing:**
```
Daily Briefing — Wed, Apr 23, 2026

Top 3 Priorities:
1. CAM reconciliation review — 10:00 AM – 12:00 PM
2. Broker call re: new listing — 2:00 – 2:30 PM
3. Lease abstract for 456 Oak — 3:00 – 4:00 PM

Energy Match: Morning HIGH (deep work) · Afternoon MEDIUM (calls + admin)

Urgent emails: 1 (tenant leak — scheduled 9:00 AM)
Important: 4 (2 scheduled, 2 pushed to tomorrow)

Reply "approve" or tell me what to adjust.
```

**5:00 PM Wrap-Up:**
```
End-of-Day Wrap-Up — Wed, Apr 23, 2026

Today: CAM rec done, broker call done, lease abstract pushed to tomorrow.
Surprise: HVAC emergency ate 90 min in the morning.
Carry-over: Lease abstract (456 Oak).

Tomorrow: 2 meetings (1.5 hrs), 1 deep work block, lighter day.

One Win: You cleared the tenant emergency same-day.
```

---

## Bottom Line

Claude scans and prioritizes. You approve and execute. The goal isn't a perfect plan — it's a **useful starting point** that respects your energy, priorities, and capacity. Set it up, tune it over the first week, then let it run.
