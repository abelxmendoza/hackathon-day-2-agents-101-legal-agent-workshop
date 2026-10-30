# Workshop 3 — Building Specialized Intelligence on Fireworks: Muse Open Models — Fri Oct 30, 2026

- **Session:** Hackathon LIVE: Building Specialized Intelligence on Fireworks — Muse Open Models
- **Full session description (calendar):** "From Inference to Training with Muse Open Models"
- **When:** Fri Oct 30, 2026, 9:00–10:00 AM PT (listed 12:00–1:00 PM ET)
- **Speaker:** Sinan Ozdemir (per the calendar listing)
- **Stream:** https://cerebralvalley.ai/e/meta-ai-developer-hackathon/live — Meta Global AI Developer Hackathon, Meta & Cerebral Valley, Oct 26 – Nov 4
- **Capture:** Abel attended live and photographed the stream at ~9:12 AM PT; the stream showed 186 attendees at that moment. These notes record only what that slide showed — the rest of the session was not captured in writing, and nothing below is inferred beyond the slide.
- **Grouped with:** Agents 101 (Oct 27) and Agents 102 (Oct 28) in the same workshops repo, at Abel's direction on Oct 30 — the hackathon's live workshops live together in one place, even though this session's topic (measuring open models on Fireworks) is different from the first two sessions' Legal Agent build.

## Slide shown — "MEASURE IT"

### The recipe: models, benches, grader, dial

1. **THE MODELS** — Muse Spark Open vs DeepSeek V4.1 Flash, both at low effort.
2. **THE BENCHES** — GSM8K, BoolQ, NQ-Open, ARC-Easy: 100 each.
3. **THE GRADER** — Plain Python per answer type. No LLM judge.
4. **THE DIAL** — Then Muse alone, from low to xhigh effort.

## Why this maps to Abel's work

- The recipe is the same discipline RobotForge already uses: fix the models and the effort level, run a fixed set of benches, grade with plain code instead of a model judge, then vary one dial at a time. RobotForge's own provider sweep did the equivalent for the describe step (fixed 24-description set, code-side parsing/validation, per-provider results) — and Agents 102 made the same point for verification: deterministic first, judge second.
- "No LLM judge" is the load-bearing line: a grader you can re-run in plain Python gives the same verdict every time, which is what makes a low-vs-xhigh effort comparison mean anything.

## Not captured

- No hands-on build, repo, or code from this session was recorded — unlike Sessions 1–2, there is no workshop project tree for Session 3 in this repo, only these notes.
- The presenter's photo from Abel's screenshot is not uploaded here (this repo is pushed through a text-only path; the screenshot stays in Abel's own media library).
