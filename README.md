# grok-skills

Collection of custom **Grok Skills** developed by @myrhex (Myrhex-x) for use with xAI's Grok.

These skills are designed to be practical, incremental, truth-seeking, and reusable. They leverage Grok's tool-calling capabilities, persistent state, and structured workflows.

## Current Skills

### 1. hantavirus-news-tracker

**Description**: An incremental news tracker for Hantavirus (Hanta virus) developments.

This skill fetches **only new** Hantavirus-related news, research, outbreaks, or public health alerts since the last time it was used. It avoids flooding you with duplicate information.

**Key Feature - Persistent Timestamp Tracking**
- Uses a local `last_run.txt` file to store the last successful run timestamp (in ISO 8601 UTC format).
- On first use: Defaults to 7 days ago.
- Subsequent uses: Only returns articles published **strictly after** the previous run time.
- After successfully delivering results to the user, the timestamp is automatically updated via the helper script.
- This creates a clean, delta-based news feed.

**Files included**:
- `SKILL.md` — Full skill definition and detailed usage instructions
- `scripts/hantavirus_news_helper.py` — Python helper for managing the `last_run.txt` timestamp

**Activation triggers**: `hantavirus news`, `hanta virus update`, `hantavirus tracker`, etc.

**How to install**:
1. Copy the entire `hantavirus-news-tracker/` folder into your local Grok skills directory (`~/.grok/skills/` or equivalent).
2. Make the helper script executable if needed: `chmod +x hantavirus_news_helper.py`

---

More skills coming soon. Focused on high-signal, low-noise, evidence-based tools.

Built for maximum truth-seeking and practical utility with Grok.
