#!/usr/bin/env python3
"""
Command Center - Entry Processor

Reads entries from /entries, processes with Claude, updates Notion.
Run with: python scripts/process.py
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

import anthropic
from notion_client import Client

# Initialize clients
claude = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
notion = Client(auth=os.getenv('NOTION_API_KEY'))

# Paths
BASE_DIR = Path(__file__).parent.parent
ENTRIES_DIR = BASE_DIR / 'entries'
PROCESSED_DIR = BASE_DIR / 'processed'
CONFIG_DIR = BASE_DIR / 'config'
STATE_FILE = CONFIG_DIR / '.state.json'


def load_config():
    """Load system prompt and context files."""
    system_prompt = (CONFIG_DIR / 'system_prompt.md').read_text()
    context = (CONFIG_DIR / 'context.md').read_text()
    return system_prompt, context


def load_state():
    """Load processing state."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"last_processed": None, "processed_files": []}


def save_state(state):
    """Save processing state."""
    STATE_FILE.write_text(json.dumps(state, indent=2))


def get_new_entries(state):
    """Get entries that haven't been processed yet."""
    if not ENTRIES_DIR.exists():
        ENTRIES_DIR.mkdir(parents=True)
        return []

    all_entries = sorted(ENTRIES_DIR.glob('*.txt'))
    processed = set(state.get('processed_files', []))

    new_entries = [e for e in all_entries if e.name not in processed]
    return new_entries


def parse_entry_filename(filepath):
    """Extract date/time and description from filename."""
    # Format: YYYY-MM-DD_HHMM_description.txt
    name = filepath.stem
    parts = name.split('_', 2)

    if len(parts) >= 2:
        date_str = parts[0]
        time_str = parts[1] if len(parts[1]) == 4 else "0000"
        description = parts[2] if len(parts) > 2 else "entry"
    else:
        date_str = datetime.now().strftime('%Y-%m-%d')
        time_str = "0000"
        description = name

    return {
        "date": date_str,
        "time": time_str,
        "description": description,
        "filename": filepath.name
    }


def fetch_notion_context():
    """Fetch recent data from Notion for context."""
    context_parts = []

    # Fetch recent Life Board items
    try:
        life_board = notion.databases.query(
            database_id=os.getenv('NOTION_LIFE_BOARD_ID'),
            page_size=20
        )
        items = []
        for page in life_board.get('results', []):
            props = page.get('properties', {})
            item = props.get('Item', {}).get('title', [{}])[0].get('plain_text', '')
            status = props.get('Status', {}).get('select', {})
            status_name = status.get('name', '') if status else ''
            area = props.get('Area', {}).get('select', {})
            area_name = area.get('name', '') if area else ''
            if item:
                items.append(f"- [{area_name}] {item} ({status_name})")

        if items:
            context_parts.append("## Current Life Board Items\n" + "\n".join(items))
    except Exception as e:
        print(f"Warning: Could not fetch Life Board: {e}")

    # Fetch goals
    try:
        goals = notion.databases.query(
            database_id=os.getenv('NOTION_GOALS_ID'),
            page_size=10
        )
        goal_items = []
        for page in goals.get('results', []):
            props = page.get('properties', {})
            goal = props.get('Goal', {}).get('title', [{}])[0].get('plain_text', '')
            progress = props.get('Progress', {}).get('number', 0) or 0
            if goal:
                goal_items.append(f"- {goal}: {int(progress * 100)}%")

        if goal_items:
            context_parts.append("## Goals Progress\n" + "\n".join(goal_items))
    except Exception as e:
        print(f"Warning: Could not fetch Goals: {e}")

    # Fetch recent health log
    try:
        health = notion.databases.query(
            database_id=os.getenv('NOTION_HEALTH_LOG_ID'),
            page_size=5,
            sorts=[{"property": "Date", "direction": "descending"}]
        )
        health_items = []
        for page in health.get('results', []):
            props = page.get('properties', {})
            entry = props.get('Entry', {}).get('title', [{}])[0].get('plain_text', '')
            entry_type = props.get('Type', {}).get('select', {})
            type_name = entry_type.get('name', '') if entry_type else ''
            if entry:
                health_items.append(f"- [{type_name}] {entry}")

        if health_items:
            context_parts.append("## Recent Health Log\n" + "\n".join(health_items))
    except Exception as e:
        print(f"Warning: Could not fetch Health Log: {e}")

    return "\n\n".join(context_parts)


def process_entries(entries, system_prompt, context):
    """Process entries with Claude and get response."""

    # Build the entries content
    entries_text = []
    for entry_path in entries:
        meta = parse_entry_filename(entry_path)
        content = entry_path.read_text()
        entries_text.append(f"### Entry: {meta['date']} {meta['time']} - {meta['description']}\n\n{content}")

    all_entries = "\n\n---\n\n".join(entries_text)

    # Fetch current Notion state
    notion_context = fetch_notion_context()

    # Build the full prompt
    full_context = f"""# System Prompt (Sydney's Logic)

{system_prompt}

---

# Persistent Context

{context}

---

# Current Notion State

{notion_context}

---

# New Entries to Process

{all_entries}
"""

    # Call Claude
    response = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system="""You are Sydney's chief of staff. You have full context about her life, goals, patterns, and current state.

Process her entries and respond with:
1. A conversational read of what's going on (acknowledge feelings, notice patterns)
2. UPDATED IN NOTION: List what should be created/updated in her databases
3. THE LIST: Prioritized, contextualized list for today/this session
4. PARKING LOT: Things mentioned but not for today
5. PATTERN NOTED: Any patterns you're noticing (optional)

Be direct but kind. No guilt trips. Sound like a person who knows her, not a robot.""",
        messages=[
            {"role": "user", "content": full_context}
        ]
    )

    return response.content[0].text


def add_to_voice_log(entry_path, ai_summary):
    """Add entry to Notion Voice Log."""
    meta = parse_entry_filename(entry_path)
    content = entry_path.read_text()

    try:
        notion.pages.create(
            parent={"database_id": os.getenv('NOTION_VOICE_LOG_ID')},
            properties={
                "Entry": {"title": [{"text": {"content": meta['description'][:100]}}]},
                "Date": {"date": {"start": meta['date']}},
                "Raw Dump": {"rich_text": [{"text": {"content": content[:2000]}}]},
                "AI Summary": {"rich_text": [{"text": {"content": ai_summary[:2000]}}]}
            }
        )
        print(f"  Added to Voice Log: {meta['description']}")
    except Exception as e:
        print(f"  Warning: Could not add to Voice Log: {e}")


def main():
    print("=" * 50)
    print(f"COMMAND CENTER UPDATE - {datetime.now().strftime('%b %d, %Y @ %I:%M %p')}")
    print("=" * 50)
    print()

    # Load config and state
    system_prompt, context = load_config()
    state = load_state()

    # Get new entries
    entries = get_new_entries(state)

    if not entries:
        print("No new entries to process.")
        print(f"\nTo add entries, create .txt files in: {ENTRIES_DIR}")
        print("Filename format: YYYY-MM-DD_HHMM_description.txt")
        return

    print(f"Processing {len(entries)} new entries:")
    for e in entries:
        print(f"  - {e.name}")
    print()
    print("-" * 50)
    print()

    # Process with Claude
    response = process_entries(entries, system_prompt, context)
    print(response)

    # Add entries to Voice Log and move to processed
    print()
    print("-" * 50)
    print("Updating Notion...")

    for entry_path in entries:
        add_to_voice_log(entry_path, response[:500])

        # Move to processed
        shutil.move(str(entry_path), str(PROCESSED_DIR / entry_path.name))
        state['processed_files'].append(entry_path.name)

    state['last_processed'] = datetime.now().isoformat()
    save_state(state)

    print()
    print("=" * 50)
    print("Done. Check Notion for updates.")


if __name__ == "__main__":
    main()
