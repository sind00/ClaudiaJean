# The West Wing - System Architecture Spec

**Version:** 2.0
**Status:** Reference Implementation

---

## Overview

A personal operating system with three components:
1. **Local capture** - text files you control (Presidential memos)
2. **AI processing** - Claudia (the AI), with full context of your life
3. **Notion backend** - databases, views, the system of record

The AI isn't just chat - it has your history, patterns, goals, and relationships. It's Claudia - synthesizing complexity into clarity.

---

## Local Project Structure

```
/TheWestWing
├── /entries                    # Your raw dumps (Presidential memos)
│   ├── 2026-01-30_0930_meeting_notes.txt
│   ├── 2026-01-30_1415_post_meeting_thoughts.txt
│   └── 2026-01-30_2100_evening_dump.txt
│
├── /processed                  # Archived after briefing
│   └── 2026-01-30_0930_meeting_notes.txt
│
├── /config
│   ├── system_prompt.md        # How Claudia thinks (editable)
│   ├── context.md              # Your Presidential profile
│   └── .state.json             # Tracks last processed entry
│
├── /scripts
│   ├── process.py              # The briefing generator
│   ├── notion_client.py        # Notion API wrapper
│   └── requirements.txt
│
├── .env                        # API keys (Claude, Notion) - gitignored
└── README.md                   # How to use
```

### Entry File Format

Just plain text. Filename provides metadata:
```
YYYY-MM-DD_HHMM_short_description.txt
```

Examples:
- `2026-01-30_0930_project_kickoff.txt`
- `2026-01-30_1415_project_kickoff_update.txt` (Claudia sees "update" and links to original)
- `2026-01-30_2100_evening.txt`
- `2026-01-31_0800_morning.txt`

Inside the file, just write naturally:
```
Had the project kickoff meeting. Timeline is aggressive - 6 weeks
to MVP. Team seems capable but understaffed. Feeling energized but
also a bit overwhelmed by the scope. Need to break this down into
something manageable. Also realized I forgot to follow up with the
client from last week.
```

No special formatting required. Claudia figures out what's what.

### Linking Related Entries

Use `_update` or `_followup` in filename:
- `2026-01-30_0930_project_kickoff.txt`
- `2026-01-30_1415_project_kickoff_update.txt`

Or reference in the text:
```
Following up on the kickoff from this morning - talked to Sarah
and she said...
```

Claudia maintains the thread.

---

## Processing Flow

### When You Run `python process.py`:

```
1. READ new entries from /entries (since last briefing)

2. LOAD context:
   - system_prompt.md (Claudia's logic)
   - context.md (your Presidential profile)
   - Recent Notion data (goals, patterns, current items)

3. FOR EACH entry (in chronological order):
   - Parse content
   - Identify: items, people, health notes, financial things, emotions
   - Connect to existing threads (project_kickoff → project_kickoff_update)
   - Update Notion databases
   - Move file to /processed

4. GENERATE briefing:
   - Claudia-style response
   - Updated priorities
   - Pattern observations
   - What changed in the system

5. OUTPUT:
   - Print briefing to terminal
   - Optionally save to a daily summary file
```

### What Claudia Has Access To (The Context Advantage)

When processing your entry "feeling overwhelmed about work stuff", Claudia knows:

| Context Type | Source | Example |
|--------------|--------|---------|
| Today's entries | /entries folder | Project kickoff happened this morning |
| Your history | Notion Voice Log | You've mentioned feeling overwhelmed in similar situations |
| Health patterns | Notion Health Log | Stress shows up as sleep issues for you |
| Goals | Notion Goals DB | "Ship MVP by Q2" is the current mission |
| Avoidance patterns | Notion Life Items | Client follow-up pushed 3 times |
| Relationships | Notion People DB | Sarah is a coworker you trust |
| Your logic | system_prompt.md | How you want Claudia to prioritize |
| Your context | context.md | Your personality, patterns, constraints |

This is what makes Claudia more than just a chatbot.

---

## Page 1: The Oval Office (Daily Ritual)

**What you see when you open Notion.**

### Layout

```
┌─────────────────────────────────────────────────────────┐
│  Today: Thursday, Jan 30                                │
│  Location: [Home / Office / Travel dropdown]            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  MORNING MEMO                                           │
│  [Large text input area]                                │
│                                                         │
│  Quick tags: [Energy: Low/Med/High] [Slept: Bad/OK/Good]│
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  LEO'S BRIEFING                                         │
│  ─────────────────────────────────────────────────      │
│  "Good morning, Mr. President. Sounds like you're       │
│  feeling the pressure from yesterday's kickoff -        │
│  that's the third time this month scope concerns        │
│  have come up. We should talk about why.                │
│                                                         │
│  THE AGENDA:                                            │
│  1. Client follow-up (15 min) - this keeps slipping     │
│  2. Break down MVP scope into phases                    │
│                                                         │
│  IF YOU GET A SECOND WIND:                              │
│  - Draft resource request email                         │
│  - Review technical specs                               │
│                                                         │
│  HOLDING FOR ANOTHER DAY:                               │
│  - Long-term roadmap planning                           │
│  - Team 1:1 scheduling"                                 │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [Continue to Situation Room →]                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Evening Version

Same page, second section below:

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  EVENING MEMO                                           │
│  [Large text input area]                                │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  LEO'S EVENING BRIEFING                                 │
│  ─────────────────────────────────────────────────      │
│  "Client call done - that's been on the board for two   │
│  weeks. Good. Presentation outline looks solid.         │
│                                                         │
│  I'm noting that you mentioned feeling better after     │
│  breaking it into sections - that tracks with your      │
│  pattern of needing to decompose big things.            │
│                                                         │
│  Tomorrow's looking manageable. If morning energy is    │
│  good, we tackle the draft."                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Page 2: The Situation Room (Command Center)

**One click from the Oval Office. Everything visible.**

### Layout

```
┌─────────────────────────────────────────────────────────┐
│  THE SITUATION ROOM                                     │
│  Mission: [Your current primary goal]                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────┐
│  │  WORK           │ │  HEALTH         │ │  CREATIVE   │
│  │  ────────────── │ │  ────────────── │ │  ────────── │
│  │  Blocked        │ │  Blocked        │ │  Blocked    │
│  │  • Item 1       │ │  • Item 1       │ │  (none)     │
│  │                 │ │                 │ │             │
│  │  Next           │ │  Next           │ │  Next       │
│  │  • Item 2       │ │  • Item 2       │ │  • Item 1   │
│  │  • Item 3       │ │  • Item 3       │ │  • Item 2   │
│  │                 │ │                 │ │             │
│  │  In Progress    │ │  Ongoing        │ │  Done       │
│  │  • Item 4       │ │  • Habit 1      │ │  • Item 3   │
│  │  • Item 5       │ │  • Habit 2      │ │             │
│  └─────────────────┘ └─────────────────┘ └─────────────┘
│                                                         │
│  ┌─────────────────┐ ┌─────────────────┐               │
│  │  FINANCES       │ │  PEOPLE         │               │
│  │  ────────────── │ │  ────────────── │               │
│  │  Overview:      │ │  Follow up      │               │
│  │  [Summary]      │ │  • Person 1     │               │
│  │                 │ │  • Person 2     │               │
│  │  Action items:  │ │                 │               │
│  │  • Item 1       │ │  Reconnect      │               │
│  │  • Item 2       │ │  • Person 3     │               │
│  └─────────────────┘ └─────────────────┘               │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  GOALS & PROGRESS                                       │
│  ─────────────────────────────────────────────────      │
│  Goal 1:    [=====>        ] Milestone description      │
│  Goal 2:    [==>           ] Milestone description      │
│  Goal 3:    [========>     ] Milestone description      │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  PATTERNS & INTEL                                       │
│  ─────────────────────────────────────────────────      │
│  • Pattern observation 1                                │
│  • Pattern observation 2                                │
│  • Friction point identified                            │
│  • Conditions for best work                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Databases

### 1. Voice Log (Presidential Memos)
Stores raw dumps for reference and pattern analysis.

| Field | Type | Purpose |
|-------|------|---------|
| Date | Date | When |
| Time of Day | Select: Morning/Evening | Which briefing |
| Raw Entry | Long text | Your actual words |
| Location | Select: Home/Office/Travel | Context |
| Energy | Select: Low/Med/High | Quick tag |
| Sleep | Select: Bad/OK/Good | Quick tag |
| Claudia's Summary | Long text | Processed version |
| Items Extracted | Relation → Life Items | What got created/updated |

### 2. Life Items (The Board)
Everything in one database, tagged by area. This is what feeds the kanban boards.

| Field | Type | Purpose |
|-------|------|---------|
| Item | Title | What it is |
| Area | Select: Work/Health/Creative/Finance/People | Which board |
| Status | Select: Blocked/Next/In Progress/Done/Ongoing | Kanban column |
| Blocked By | Text | What's stopping it |
| Priority | Select: Critical/High/Medium/Low | Weight |
| Due Date | Date | If applicable |
| Related Person | Relation → People | If applicable |
| Notes | Long text | Context |
| Times Pushed | Number | Tracks avoidance patterns |
| Last Touched | Date | Staleness tracking |
| Created From | Relation → Voice Log | Origin |

### 3. People (The Rolodex)
Your relationship CRM.

| Field | Type | Purpose |
|-------|------|---------|
| Name | Title | Who |
| Type | Multi-select: Professional/Personal/Creative/Technical | Context |
| Company/Context | Text | Where you know them from |
| City | Select | Location |
| Warmth | Select: Hot/Warm/Cold | Relationship status |
| Last Contact | Date | When you last talked |
| Follow Up By | Date | When to reach out |
| Can Help With | Multi-select | Job referral, advice, etc. |
| Personal Notes | Text | Kids names, interests, etc. |
| Birthday | Date | For outreach |

### 4. Transactions (The Budget)
For finance tracking.

| Field | Type | Purpose |
|-------|------|---------|
| Description | Title | What |
| Amount | Number (dollar) | How much |
| Category | Select | Rent, Groceries, Subscriptions, etc. |
| Date | Date | When |
| Type | Select: Expense/Income | Direction |
| Recurring | Checkbox | Subscription flag |
| Cancel? | Checkbox | Flagged for cutting |

### 5. Health Log (Medical Intel)
Tracks patterns over time.

| Field | Type | Purpose |
|-------|------|---------|
| Date | Date | When |
| Type | Select: Symptom/Appointment/Note/Medication | What kind |
| Description | Text | Details |
| Severity | Select: Mild/Moderate/Severe | For patterns |
| Stress Level | Select: Low/Med/High | Correlation tracking |
| Related Voice Log | Relation | Origin |

### 6. Goals (The Agenda)
Progress tracking for Claudia to reference.

| Field | Type | Purpose |
|-------|------|---------|
| Goal | Title | What |
| Area | Select | Which life area |
| Target Date | Date | Deadline |
| Progress | Number (%) | How far along |
| Current Milestone | Text | Where you are now |
| Blocked By | Text | What's in the way |

---

## Claudia's Logic (System Prompt)

Stored in `/config/system_prompt.md`. Contains:

1. **Context about you** - personality, energy patterns, what works/doesn't
2. **Current priorities** - the mission, what matters now
3. **Weighting logic** - how to prioritize (tiers, energy adjustments, location context)
4. **Pattern recognition rules** - what to watch for (repeated avoidance, health correlations, etc.)
5. **Briefing format** - how to structure the morning/evening output
6. **Goals reference** - current state of major goals (updated monthly)

See `config/system_prompt.md` for the template.

---

## How It Works Daily

### Morning:
1. You open Notion → The Oval Office
2. You dump into Morning Memo
3. You tag Energy + Sleep
4. Claudia reads dump + checks Voice Log history + checks Life Items + checks Health Log + references System Prompt
5. Claudia responds with briefing: contextual read + THE AGENDA
6. Items get created/updated in Life Items database
7. You click through to Situation Room if you want the full picture

### Evening:
1. You dump what happened into Evening Memo
2. Claudia processes → updates Life Items (status changes, new items, etc.)
3. Claudia updates Health Log if relevant
4. Claudia notes patterns
5. Claudia gives brief summary + preview of tomorrow

### Weekly:
- Review Situation Room
- Check Patterns & Intel section
- Update Goals progress
- Finance review (subscriptions, runway)

### Monthly:
- Update System Prompt with any new context
- Review and archive completed items
- Adjust priorities if needed

---

## Output Examples

### After Running process.py

**Terminal output:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE WEST WING BRIEFING - Jan 30, 2026 @ 3:45 PM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Processed 2 new memos:
  • 2026-01-30_0930_project_kickoff.txt
  • 2026-01-30_1415_project_kickoff_update.txt

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Good afternoon, Mr. President. Big day.

The project scope is ambitious but you've handled similar
timelines before. Let's break it down before the overwhelm
sets in.

Your sleep was rough last night - that often happens when
you're processing a lot. Let's keep today focused on clarity,
not output.

UPDATED IN NOTION:
  • Created: "MVP Phase 1 scope" in Work (Status: Next)
  • Created: "Client follow-up" in Work (Status: Next, flagged - pushed 3x)
  • Updated: Voice Log with kickoff notes
  • Linked: Sarah to project kickoff thread

THE AGENDA FOR REST OF TODAY:
  1. Client follow-up call (15 min) - this keeps slipping
  2. Draft MVP phase breakdown
  3. Rest early if energy dips

HOLDING FOR ANOTHER DAY:
  • Resource request (wait until scope is clearer)
  • Long-term roadmap (next week)

PATTERN NOTED:
  Scope concerns have come up 3 times this month. Might be
  worth examining why - is it project selection or estimation
  approach?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Implementation Plan

### Phase 1: Foundation
- [ ] Create Notion databases (Voice Log, Life Items, People, Transactions, Health Log, Goals)
- [ ] Create Notion pages (Oval Office, Situation Room)
- [ ] Set up linked views and kanban boards
- [ ] Create local project structure
- [ ] Write system_prompt.md and context.md
- [ ] Basic process.py script (reads files, outputs to terminal)

### Phase 2: Integration
- [ ] Connect process.py to Notion API
- [ ] Full processing logic (parse entries, identify items, update DBs)
- [ ] Pattern detection from historical data
- [ ] Claudia-style briefing generation

### Phase 3: Refinement
- [ ] Tune system prompt based on what's working
- [ ] Add more pattern recognition
- [ ] Whisper integration for voice recordings
- [ ] Meeting/call transcription pipeline

---

## Customization Guide

### Adapting for Your Use Case

1. **Edit `config/context.md`** - Fill in your Presidential profile
2. **Edit `config/system_prompt.md`** - Define your priority tiers and how Claudia should think
3. **Modify database areas** - Change "Work/Health/Creative/Finance/People" to whatever categories fit your life
4. **Adjust briefing style** - Update the system prompt to match how you want Claudia to talk to you

### Common Modifications

**For career transitions:**
- Add job application tracking to Life Items
- Create interview prep area
- Add networking warmth tracking to People

**For health management:**
- Expand Health Log with medication tracking
- Add symptom correlation fields
- Create appointment scheduling views

**For creative projects:**
- Add project stages to Life Items
- Track client relationships in People
- Add portfolio/deadline views

**For students:**
- Rename "Work" to "Academic"
- Add assignment tracking
- Create exam prep areas

---

*"What's next?"*
