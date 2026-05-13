name: hantavirus-news-tracker
description: "Fetch incremental Hantavirus (Hanta virus) news since the last time this skill was used. Tracks persistent last-run timestamp for time-aware updates on outbreaks, cases, research, CDC/WHO alerts. Trigger with 'hantavirus news', 'hanta virus update', 'latest hanta developments', or 'hantavirus tracker'."

# Hantavirus News Tracker

## Overview

This skill delivers **only** new Hantavirus-related news published after your previous use of it. It maintains a persistent timestamp (`last_run.txt`) to avoid duplicate reporting and focus exclusively on fresh developments: case reports, outbreaks, research, prevention updates, or public health alerts from credible sources.

## Instructions

**Follow this workflow exactly for accurate, incremental results:**

### 1. Get the cutoff time (since last use)
- Execute:  
  `python /home/workdir/.grok/skills/hantavirus-news-tracker/scripts/hantavirus_news_helper.py get-since`
- This prints an ISO 8601 UTC timestamp (e.g. `2026-05-05T14:30:00+00:00`).
- **Only** include articles published **strictly after** this cutoff. (First-time use defaults to 7 days ago.)

### 2. Search for candidate news
- Call `web_search` tool:
  - Query: `Hantavirus OR "Hanta virus" OR "Hantavirus Pulmonary Syndrome" OR hantavirus outbreak OR hantavirus case OR hantavirus research`
  - `num_results`: 15–20
- For stronger recency, you may also `browse_page` on `https://news.google.com/search?q=Hantavirus+OR+Hanta+virus&hl=en-US&gl=US&ceid=US:en` with instructions to "Extract the 10 most recent articles with their titles, URLs, publication times (e.g. '2 hours ago', 'May 10, 2026'), and short descriptions. Ignore ads and unrelated results."

### 3. Filter strictly to new items only
- For every result, determine the **publication date/time**:
  - Prefer explicit dates in snippets, titles, or structured data.
  - If missing or ambiguous: Use `browse_page` on the URL with instructions: "Extract the exact publication date, time, author, and first paragraph. State the publish timestamp in ISO if possible or human-readable."
- **Discard** any item whose publish time ≤ cutoff timestamp.
- Prioritize primary/credible sources only: CDC.gov, WHO.int, state health departments, PubMed/Nature/Science/Lancet, Reuters, AP, BBC, NYT, local official health agencies. Skip blogs, unverified social posts, or low-quality aggregators.

### 4. Summarize new developments (if any)
- Group by category:
  - **Outbreaks/Cases**: Location, confirmed cases, deaths, rodent exposure details.
  - **Research/Advances**: New studies, vaccines, treatments, transmission insights.
  - **Alerts/Prevention**: Official warnings, travel advisories, control measures.
  - **Other**: Policy, funding, notable events.
- For each qualifying item provide:
  - 1–2 sentence factual summary.
  - Key details (who, what, where, when, impact).
  - Source name + direct URL.
  - Exact publish date/time.
- If **zero new items**: State clearly —  
  "No new Hantavirus news since [human-readable cutoff, e.g. May 5, 2026 14:30 UTC]. No outbreaks, alerts, or significant research reported in the interval. The epidemiological situation appears stable."
- Always close with: "Skill last-run timestamp updated to [now]. Future queries will only surface items after this point."

### 5. Persist the new last-run time
- **Only after** you have presented the news to the user, run:  
  `python /home/workdir/.grok/skills/hantavirus-news-tracker/scripts/hantavirus_news_helper.py update-last`
- This writes the current UTC time to `last_run.txt`.

### 6. Edge cases & user control
- **No new news or quiet period**: Report honestly; Hantavirus activity is typically low and sporadic.
- **Script or file error**: Fall back to last 48 hours manually, warn the user, and suggest `rm /home/workdir/.grok/skills/hantavirus-news-tracker/last_run.txt` to reset.
- **Force full history**: User (or you) can delete `last_run.txt` or edit it to an old ISO date.
- **Multiple rapid calls**: The cutoff only advances on successful `update-last`, so repeated calls in one session still work correctly.
- **Truth-seeking note**: Report only verifiable facts from reputable sources. Do not speculate or amplify unconfirmed rumors. Hantavirus is a serious but rare zoonosis; context matters.

**Activation triggers:** Any query containing "hantavirus news", "hanta virus latest", "hantavirus tracker", "hanta update since last", or similar.

This design guarantees you receive **precisely** the delta of news since your last interaction — nothing more, nothing less.