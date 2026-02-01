# Claudia Jean "CJ" Creggs (from West Wing)

A personal operating system that turns raw voice dumps and notes into AI-processed, prioritized action items with full life context.

**This is your Claudia Jean (CJ's full name in the show).**

---

## The Premise

In *The West Wing*, CJ Cregg was the one who synthesized complexity into clarity. She took everything happening in the administration and communicated it - directly, intelligently, with no BS. She didn't just relay information; she understood the full picture and delivered what mattered.

Most productivity systems treat you like a task-completion machine. This one treats you like what you are: someone running a complex operation (your life) who needs someone with institutional knowledge to cut through the noise and tell you what actually matters.

---

## How It Works

```
You (President)          The West Wing (System)       Claudia (AI)
     │                          │                            │
     │  Voice dump/notes        │                            │
     │ ─────────────────────►   │                            │
     │                          │  Process with full context │
     │                          │ ──────────────────────────►│
     │                          │                            │
     │                          │   Contextual briefing      │
     │                          │ ◄──────────────────────────│
     │   "Here's what matters"  │                            │
     │ ◄─────────────────────── │                            │
```

1. **Capture** - Write or voice dump into local text files (you own your data)
2. **Process** - AI reads your entry with full context: goals, patterns, health, relationships
3. **Brief** - Get a Claudia-style response: clear, contextual, no BS
4. **Track** - Notion databases update automatically

---

## The Daily Briefing

**Morning:**
> "Good morning, Mr. President. Based on last night's entry, sounds like you're anxious about the presentation. That's the third time this month scope has come up - we should talk about why.
>
> Energy's medium, you slept poorly. Let's keep today tight.
>
> **The agenda:**
> 1. That client call you've pushed twice - 15 minutes, let's clear it
> 2. Outline the presentation structure (don't write it yet)
>
> **If you get a second wind:**
> - Draft the intro section
>
> **Holding for another day:**
> - The budget review
> - Team scheduling"

**Evening:**
> "Client call done - that's been on the board for two weeks. Good. Presentation outline looks solid.
>
> I'm noting that you mentioned feeling better after breaking it into sections - that tracks with your pattern of needing to decompose big things before you can move.
>
> Tomorrow's looking lighter. If morning energy is good, we tackle the draft."

---

## Who This Is For

**Career transitions** - Job search tracking, interview prep, networking warmth

**Health management** - Correlating symptoms with stress, tracking patterns over time

**ADHD or executive function support** - External structure that adapts to variable energy, not rigid systems that create shame

**Creative projects** - Managing multiple threads without losing context

**Anyone tired of productivity systems that make them feel like a failure** - This one adapts to you, not the other way around

---

## Architecture

```
/TheWestWing
├── /entries                    # Your raw dumps (Presidential memos)
│   └── 2026-01-30_0800_morning.txt
├── /processed                  # Archived after briefing
├── /config
│   ├── system_prompt.md        # How Claudia thinks (editable)
│   └── context.md              # Your Presidential profile
├── /scripts
│   └── process.py              # The briefing generator
└── /docs
    ├── SPEC.md                 # Full system architecture
    └── PHILOSOPHY.md           # Why this exists
```

---

## Setup

### Prerequisites
- Python 3.8+
- Notion account + API key
- Anthropic API key (Claude)

### Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/the-west-wing.git
cd the-west-wing

# Install dependencies
pip install -r scripts/requirements.txt

# Configure
cp .env.example .env
# Edit .env with your API keys
```

### Configuration

1. **Fill out `config/context.md`** - Tell Claudia about yourself (the Presidential profile)
2. **Customize `config/system_prompt.md`** - Define your priorities and briefing style
3. **Connect Notion** - Add your database IDs to `.env`

### Daily Use

```bash
# Write your memo
echo "Had a rough morning, presentation anxiety..." > entries/2026-01-30_0800_morning.txt

# Get your briefing
python scripts/process.py
```

---

## The Notion Backend

Two pages, minimal clicking:

**The Oval Office** (Daily Ritual)
- Morning/evening dump inputs
- Claudia's briefing response
- Quick energy/sleep tags
- One click to the Situation Room

**The Situation Room** (Command Center)
- Kanban boards by life area
- Goals and progress tracking
- Pattern insights
- People/relationship tracking

---

## Philosophy

> "I usually hate TODO apps because they lack a reflective, journaling, whiteboarding social aspect. It's not about checking boxes. It's about discussing the current situation with someone who knows your whole context and objectively be told what actually matters today."

Read more in [docs/PHILOSOPHY.md](docs/PHILOSOPHY.md)

---

## Contributing

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)

---

## License

MIT - See [LICENSE](LICENSE)

---

*"What's next?"* - President Bartlet
