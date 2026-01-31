# Contributing

This is a personal project, but if you find it useful and want to contribute, here's how.

## Ways to Contribute

### 1. Use It and Share Feedback

The most valuable contribution is using the system and reporting what works and what doesn't. Open an issue with:
- What you tried
- What you expected
- What actually happened
- Your context (ADHD? Health conditions? Career transition?)

### 2. Improve the Processing Logic

The `scripts/process.py` file handles parsing and Claude interaction. Improvements welcome:
- Better entry parsing
- Smarter thread linking (connecting related entries)
- More robust Notion API handling
- Error handling improvements

### 3. Add Integrations

Planned integrations that need building:
- Whisper for voice transcription
- Apple Notes sync (export handling)
- Calendar integration
- iMessage/SMS outreach automation

### 4. Improve Documentation

- Clearer setup instructions
- More examples in SPEC.md
- Video walkthrough
- Translation to other languages

### 5. Share Your Config

If you've customized `system_prompt.md` or `context.md` in useful ways, share them (anonymized) as examples for others.

## Development Setup

```bash
# Fork and clone
git clone https://github.com/yourusername/command-center.git
cd command-center

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r scripts/requirements.txt

# Copy and configure
cp .env.example .env
# Add your API keys

# Run tests (when we have them)
python -m pytest tests/
```

## Code Style

- Python: Follow PEP 8
- Markdown: Keep it readable, not pretty
- Comments: Explain why, not what

## Pull Request Process

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/whisper-integration`)
3. Make your changes
4. Test locally
5. Submit PR with clear description of what and why

## Questions?

Open an issue or reach out directly.
