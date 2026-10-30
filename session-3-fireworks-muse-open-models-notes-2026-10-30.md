# Workshop 3 — Building Specialized Intelligence on Fireworks: Muse Open Models — Fri Oct 30, 2026

- **Session:** Hackathon LIVE: Building Specialized Intelligence on Fireworks — Muse Open Models
- **Full session description (calendar):** "From Inference to Training with Muse Open Models"
- **When:** Fri Oct 30, 2026, 9:00–10:00 AM PT (listed 12:00–1:00 PM ET)
- **Speaker:** Sinan Ozdemir (per the calendar listing)
- **Stream:** https://cerebralvalley.ai/e/meta-ai-developer-hackathon/live — Meta Global AI Developer Hackathon, Meta & Cerebral Valley, Oct 26 – Nov 4
- **Capture:** Abel attended live and photographed the stream at ~9:12 AM PT (the stream showed 186 attendees at that moment), then sent three follow-up photos at ~9:15 AM PT as the presenter moved from the slide into the demo notebook and the experiments repo. These notes record only what those photos show; wording that was not legible in a photo is paraphrased or flagged, never filled in.
- **Grouped with:** Agents 101 (Oct 27) and Agents 102 (Oct 28) in the same workshops repo, at Abel's direction on Oct 30 — the hackathon's live workshops live together in one place, even though this session's topic (measuring open models on Fireworks) is different from the first two sessions' Legal Agent build.

## The point of the session (Abel's summary, ~9:20 AM PT)

In Abel's words: "We need an evaluation. A test set to make sure model A is better than model B. We need a benchmark evaluation — to prove that you chose the best model for your task."

That is the whole recipe below in one line: you don't pick a model by reputation or by trying it twice — you build a fixed test set, grade it deterministically, and the numbers are the evidence for the choice. It is also exactly what RobotForge already did for its own model choice: a fixed 24-description test set (including deliberate traps) run through the real prompt/schema/validator across providers — Baseten (Muse Spark Open) 24/24, Meta 23/24, Fireworks 21/24 — which is why Baseten is the live endpoint's primary provider and the others are fallbacks. Chosen by measurement, not by default.

## Slide shown — "MEASURE IT"

### The recipe: models, benches, grader, dial

1. **THE MODELS** — Muse Spark Open vs DeepSeek V4.1 Flash, both at low effort.
2. **THE BENCHES** — GSM8K, BoolQ, NQ-Open, ARC-Easy: 100 each.
3. **THE GRADER** — Plain Python per answer type. No LLM judge.
4. **THE DIAL** — Then Muse alone, from low to xhigh effort.

## Kick off: the head-to-head (follow-up photos, ~9:15 AM PT)

Next slide, verbatim:

> Open: `muse_vs_deepseek_demo.ipynb`
> **Kick off: the head-to-head**
> 4 benches x 100 questions x 2 models, effort = low
> Responses cache to results.jsonl and resume

The notebook's Setup cell was visible behind the slide. Legible parts only — the photo does not support a verbatim code transcription:

- Live mode line: `RUN_SWEEP = True` — re-runs Fireworks (resumable).
- Demo knobs visible in the code: `RUN_SWEEP = True`, `EFFORT = "low"`, `N_PER_BENCH = 100`.
- Model names in the code: `MUSE = "Muse Spark Open"`, `DS = "DeepSeek V4.1 Flash"`.
- Results are cached to `results.jsonl` next to the notebook (with a fallback path into `experiments/meta-hackathon-muse/`), and the repo root's `.env` is loaded via `load_dotenv` — keys stay in `.env`, same rule as Sessions 1–2.

## The experiments repo the presenter worked from

Shown on GitHub (branch `main`, path `ai-experiments / experiments / meta-hackathon-muse`). Its README, as legible in the photo:

**"Meta hackathon: Muse open models on Fireworks"** — "Three notebooks for the Meta Global Hackathon workshop on Muse Spark Open and Muse Glimmer."

| Notebook | Question it answers |
|---|---|
| `muse_vs_deepseek_demo.ipynb` | Does Muse Spark Open beat DeepSeek V4.1 Flash on simple short-answer text? |
| `muse_reasoning_sweep.ipynb` | Does more Muse reasoning effort help on those tasks? |
| `muse_glimmer_train_router.ipynb` | Can a fine-tuned Muse Glimmer decide which model a prompt should go to? |

Also in the folder: `muse_effort_sweep.png`, `router_base_vs_tuned.png`, `run_simple_bench.py`, and a `simple_bench` chart image.

**Short-answer suite (notebooks 1 and 2):** the four answer types are number, yes/no, string, and choice — text only, no screenshots and no click coordinates.

| Answer type | Bench |
|---|---|
| number | GSM8K |
| yes/no | BoolQ |
| string | NQ-Open |
| choice | ARC-Easy |

"Models run on Fireworks serverless. Grading is deterministic (number within 1%, yes/no match, string alias match, letter match), 100 per bench." The head-to-head section runs both models at `reasoning_effort=low`; its results table (Bench | Muse | DeepSeek | Δ) was cut off at the bottom of the photo — **no scores were captured, and none are quoted here.**

This is the presenter's experiments repo, shown on his screen — Abel did not clone or build it during the session, as far as the photos show.

## Checking the models on Fireworks (~9:17 AM PT, Abel's narration + photo)

Abel's own description of this part, in his words: checking models and capabilities on Fireworks — trending, and what people are using. Muse Spark shows token prices; Muse Glimmer does not. Clicking **Serverless** shows the models you can run without having to create a dedicated deployment.

What the photo itself shows:

- The Fireworks console **Models** page (Explore → Models): **334 models**, sorted by **Trending**.
- Left nav — Create: Serverless, Deployments, Training, Batch API. Explore: Models, Playgrounds, Nexus. Manage: Reservations, Custom Models, Datasets.
- Rows carry per-model pricing in $/M (uncached / cached / output), capability tags (Serverless, Tunable, Function-calling), and context length — **the actual price figures are not legible in the photo, so none are quoted here.**
- Legible trending/new names at the top of the list: FireRouter with Opus, MiniMax M2.1 Flash, DeepSeek V4.1 Flash, GLM-5.5 (further rows, incl. a GLM Flash and a Pro-RL model, were cut off or too blurred to name reliably).
- Point that matters for the workshop's arc: Serverless is the no-deployment path — the same way RobotForge already calls Muse Spark Open on Fireworks — while a dedicated deployment (and the Cookbook's training loops) is the step you take only when you actually need your own tuned model, e.g. the Glimmer router in notebook 3.

## Resource shown: Fireworks AI Cookbook

The presenter also showed the public GitHub repo **fw-ai/cookbook** ("Fireworks AI Cookbook", Apache-2.0): "Recipes and resources for training, building generative AI with Fireworks" (fireworks.ai/docs). Its README describes training loops and worked examples for RL, preference optimization, SFT, distillation, and embedding fine-tuning on Fireworks — the training half of this session's "From Inference to Training" arc, and the pointer to use if the Glimmer router fine-tune (notebook 3) is ever picked up.

## Why this maps to Abel's work

- The recipe is the same discipline RobotForge already uses: fix the models and the effort level, run a fixed set of benches, grade with plain code instead of a model judge, then vary one dial at a time. RobotForge's own provider sweep did the equivalent for the describe step (fixed 24-description set, code-side parsing/validation, per-provider results) — and Agents 102 made the same point for verification: deterministic first, judge second.
- "No LLM judge" is the load-bearing line: a grader you can re-run in plain Python gives the same verdict every time, which is what makes a low-vs-xhigh effort comparison mean anything.

## Not captured

- Unlike Sessions 1–2, Abel did no hands-on build in this session — there is no Session 3 project tree in this repo, only these notes. The notebook and experiments repo above are the presenter's, shown on the stream.
- The head-to-head results (the Bench | Muse | DeepSeek | Δ table) and the reasoning-sweep results were below the fold in Abel's photos — not captured, not quoted.
- Abel's screenshots of the stream are not uploaded here (this repo is pushed through a text-only path; the screenshots stay in Abel's own media library).
