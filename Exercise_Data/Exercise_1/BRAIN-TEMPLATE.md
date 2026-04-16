# BRAIN.md — Your CRE Professional Persona

> **Purpose:** This file is persistent context that Claude reads at the start of every chat inside your Cowork Project. It tells Claude who you are, what you work on, how you think, and how you communicate — so you do not have to re-explain yourself in every new conversation.
>
> **How to use this template:**
> 1. Copy this file into your `CRE-150-Workshop` folder
> 2. Rename it to `brain.md`
> 3. Fill in the seven short fields below with your own draft (2-3 sentences each is fine)
> 4. Then run the interview prompt at the bottom of this file — Claude will expand each section with targeted follow-up questions
> 5. Save the expanded file. This is your brain.

---

## 1. Role

*What is your job title, seniority, and primary focus area? What decisions do you own versus recommend? What does a typical week look like?*

[ Write 2-3 sentences. Example: "I am a Senior Director of Asset Management at a mid-sized REIT. I own leasing strategy and operating budgets for a 2.4M SF Canadian office portfolio. I spend most weeks in review meetings with leasing brokers, property managers, and the CFO."]

---

## 2. Firm

*What kind of firm do you work at — REIT, private equity, family office, developer, broker, lender, owner-operator? What is the firm's AUM, portfolio size, or deal volume? What is the firm's investment philosophy or service positioning?*

[ Write 2-3 sentences. Example: "Private REIT, approximately $1.8B AUM, focused on value-add office and industrial in tier-2 Canadian markets. We hold 7-10 years and operate through internal asset management — we do not outsource property management except for janitorial and maintenance."]

---

## 3. Portfolio or Deal Flow

*What asset classes do you work on? What geography? What building classes, tenant profiles, or deal sizes? If you are a broker or intermediary, describe the deals you typically work rather than a portfolio.*

[ Write 2-3 sentences. Example: "Office (60%) and industrial (40%) in GTA, Ottawa, Montreal. Class B+ and A- buildings, 50,000-250,000 SF per asset. Tenant mix is roughly 40% government, 30% professional services, 20% logistics, 10% specialty."]

---

## 4. Team

*Who do you work with regularly? Name the roles (not necessarily the people): direct reports, peers, managers, external partners. How do decisions flow in your organization?*

[ Write 2-3 sentences. Example: "I report to the SVP of Real Estate. I have two Asset Managers and one Analyst reporting to me. I work daily with the VP of Leasing, the Director of Property Management, and external brokers at CBRE and Colliers. Major leasing decisions go to the CIO for approval."]

---

## 5. Clients or Counterparties

*Who are you typically negotiating with, advising, or representing? Tenants or landlords? Buyers or sellers? Lenders or borrowers? What is the power dynamic in your typical transaction?*

[ Write 2-3 sentences. Example: "I sit on the landlord side. Counterparties are mid-market tenants (50-500 employees) represented by tenant brokers. In acquisitions, we are usually the buyer negotiating with institutional sellers. For capital transactions, we interact with insurance lenders and Canadian banks."]

---

## 6. Working Preferences

*How do you like to receive work back from Claude? What formats, lengths, and review cadences work for you? What tools do you already use — Excel, Yardi, Argus, CoStar, Outlook, Teams, Notion? What should Claude always ask before doing?*

[ Write 2-3 sentences. Example: "Give me bullet-point summaries first, then detailed analysis if I ask for it. Always show your reasoning for financial calculations — I do not trust black-box numbers. I work in Excel and Yardi daily; I do not use Notion. Always ask before drafting emails to external parties."]

---

## 7. Voice and Communication Notes

*How do you write? Formal or conversational? Short or detailed? What words or phrases do you use a lot? What do you not want Claude to ever write (em dashes, hedging phrases, AI-sounding filler)? Are there examples of your writing Claude should emulate?*

[ Write 2-3 sentences. Example: "My emails are short and direct — 3-5 sentences maximum to external parties. I write internal memos with clear section headers and numbered recommendations. I do not use em dashes. I do not write 'I hope this finds you well.' Examples of my writing are in the email ingestion skill built in Exercise 2."]

---

## Interview Prompt — Run This After Filling In The Template

Copy the prompt below into a new chat inside your CRE-150-Workshop Project. Claude will expand each section of your brain.md with targeted follow-up questions.

```
I have filled in the skeleton of brain.md in my project folder. I want you to interview
me to expand each section into a rich persona document.

Rules:
1. Start with Section 1 (Role). Ask me one follow-up question at a time. When I have
   given you substantive detail — typically 3-5 exchanges per section — move to the
   next section.
2. Your questions should probe for specifics: names of systems I use, the kinds of
   decisions I make, the language I use with different audiences, what I wish was
   automated, what I would never trust to AI.
3. When you ask about voice and communication, have me paste 2-3 examples of my actual
   writing. Analyze the patterns out loud. Document those patterns in Section 7.
4. When we finish all seven sections, save the expanded file as brain.md in this Project
   folder. Do not send it anywhere else.
5. At the end, summarize back to me the three most important things you now know about
   how I work. This is my check that you actually listened.
```

---

## Maintenance

Your brain.md is a living document. Update it as your role changes, as you learn what Claude does well or poorly, and as you add new working preferences. A few maintenance patterns:

- **After Exercise 2 (connectors):** Ask Claude to analyze your sent email and update Section 7 with evidence-based voice notes.
- **After Exercise 4 (legal plugin):** If you have CRE-specific lease preferences (preferred escalator type, free-rent tolerance, co-tenancy standards), add them to Section 3 or create an eighth section for "Standard Lease Positions."
- **Quarterly:** Re-read your brain.md. Delete what no longer applies. Add what you wish Claude had known during tough decisions.
- **When you notice Claude getting something wrong:** Ask yourself whether the gap is in brain.md or in a skill. Brain.md is for who you are; skills are for what you do.

---

*This template is part of CRE-150 Exercise 1, Part A.0. 