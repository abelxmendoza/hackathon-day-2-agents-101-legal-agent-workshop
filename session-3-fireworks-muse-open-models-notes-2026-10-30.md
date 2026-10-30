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

**Why low effort for the head-to-head (Abel's narration, ~9:21 AM PT):** with the benchmarks in hand, everything is set to low effort for the comparison run — it ran faster and spit out fewer reasoning tokens. Low is the headline setting for the two-model run; the effort dial gets swept afterwards, on Muse alone (notebook 2), where the cost/accuracy trade is the thing being measured.

The notebook's Setup cell was visible behind the slide. Legible parts only — the photo does not support a verbatim code transcription:

- Live mode line: `RUN_SWEEP = True` — re-runs Fireworks (resumable).
- Demo knobs visible in the code: `RUN_SWEEP = True`, `EFFORT = "low"`, `N_PER_BENCH = 100`.
- Model names in the code: `MUSE = "Muse Spark Open"`, `DS = "DeepSeek V4.1 Flash"`.
- Results are cached to `results.jsonl` next to the notebook (with a fallback path into `experiments/meta-hackathon-muse/`), and the repo root's `.env` is loaded via `load_dotenv` — keys stay in `.env`, same rule as Sessions 1–2.

## The presenter's experiments repo — PULLED (~9:35 AM PT)

The repo is public: **`sinanuozdemir/ai-experiments`** (the presenter's surname is spelled Uzdemir in his GitHub handle; session listings show "Ozdemir"). Abel asked if I had pulled it; I found it by searching GitHub code for the notebook name and cloned it: local copy at `~/workspace/hackathon/ai-experiments/`, HEAD `69cb19f` ("tweaks"). `experiments/` contains four folders: `meta-hackathon-muse`, `reasoning-effort-uipad`, `difficulty-router-langchain`, and `scion`. The exact results tables in this file come from `experiments/meta-hackathon-muse/README.md`. Note: `results.jsonl` is listed in that README's file table but is NOT in the cloned folder (it's the presenter's local cache). The chart PNGs from the notebooks (demo_pass_by_type.png, muse_effort_sweep.png, router_base_vs_tuned.png, and the muse_ahead_* slide assets) ARE in the repo.

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

"Models run on Fireworks serverless. Grading is deterministic (number within 1%, yes/no match, string alias match, letter match), 100 per bench." The head-to-head section runs both models at `reasoning_effort=low`; its results table (Bench | Muse | DeepSeek | Δ) was cut off at the bottom of that photo — the results themselves arrived in Abel's next photo, below.

This is the presenter's experiments repo, shown on his screen — Abel did not clone or build it during the session, as far as the photos show.

## Head-to-head results — EXACT figures from the presenter's repo (pulled ~9:35 AM PT, see below)

Both models at `reasoning_effort=low`, from the official README table in `experiments/meta-hackathon-muse/`:

| Bench | Muse | DeepSeek | Δ |
|---|---:|---:|---:|
| GSM8K | **99.0** | 96.0 | +3.0 |
| NQ-Open | **69.0** | 62.0 | +7.0 |
| BoolQ | 90.0 | 91.0 | −1.0 |
| ARC-Easy | 96.0 | 97.0 | −1.0 |
| **Overall** | **88.5** | 86.5 | **+2.0** |

So Muse's overall win comes from GSM8K and especially NQ-Open (+7); DeepSeek actually edges BoolQ and ARC-Easy by a point each. The notebook also plots published Specialized Intelligence Index results where Muse leads DeepSeek — that is the "Where Muse already leads publicly" section visible at the bottom of Abel's chart photo.

**Correction note:** Abel's ~9:26 AM chart photo was blurred, and my first readings logged here (Muse ≈84.5 vs DeepSeek ≈81.3 overall; NQ-Open ≈64 vs ≈53; BoolQ/ARC-Easy as ties) were wrong in detail. Abel asked whether I had pulled the official repo — I hadn't — so I found and cloned it (public: `sinanuozdemir/ai-experiments`, HEAD `69cb19f`, local copy at `~/workspace/hackathon/ai-experiments/`), and the table above replaces those readings. The sweep chart readings below, by contrast, matched the repo exactly.

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

## Slide: "Which method, when" (photo, ~9:39 AM PT) — how notebook 3's training method was chosen

A comparison table (source line on the slide: "Rules of thumb, not guarantees. Source: Field Guide to Training Modern AI (Fireworks), Fig. 4.2"):

| | Supervised Fine-Tuning (SFT) | Direct Preference Optimization (DPO) | Reinforcement Learning (RL) |
|---|---|---|---|
| You provide | Complete, correct examples ending on the model's turn | Pairs: one preferred, one rejected answer | Prompts + rewards, an environment and a grader |
| Explores on its own? | No | No | Yes |
| Relative cost | Lowest | Low | Highest |
| Use it when | There's one right answer, or a format, tone or teacher to copy | Several answers work and you know which is better | The model already succeeds some of the time |
| Watch out for | Memorizing instead of generalizing | A poor fit when there's one right answer | It optimizes whatever the reward measures, loopholes included |
| Where you'll see it | **Today: Muse Glimmer as the router** | Managed DPO runs on Glimmer too | See our cookbook for more! |

So the router is trained with SFT precisely because routing has one right answer per prompt — the cheapest method is the right one. Abel's one-line narration of this segment: **"train muse glimmer to be a router."**

## Slide: "NEXT STEP — When you can score it: reinforcement learning" (photo, ~9:44 AM PT)

Verbatim from the slide:

"No answer key. The model learns from its own attempts.

1. **Observe** — the agent sees the task
2. **Act** — it calls a tool or answers
3. **Reward** — a grader scores the try, 0 to 1
4. **Learn** — weights shift toward reward
5. **Repeat** — hundreds of times"

The diagram is the standard loop: an AGENT ("the model we train," labeled Muse Glimmer + LoRA) acts on an ENVIRONMENT ("task, tools, grader") — action (tool calls, answers) flows down, state + reward flow back, next prompt comes in at the top. Footer: "Adapted from Field Guide to Training Modern AI, Fig. 4.4. The cookbook's serverless RL example runs on Muse Glimmer 30B."

RobotForge parallel worth noting: RL's entry requirement is exactly a trustworthy 0-to-1 grader — which is the thing RobotForge already builds (deterministic validation + the 5% / 5° gate). SFT taught the router to imitate labels; RL would let a model learn from scored attempts instead. That is a post-hackathon direction, not a this-week one — RL is also the one method the Fireworks promotion does NOT cover.

## Slide: "TRAIN IT — The recipe: model, data, surfaces, eval" (photo + Abel's narration, ~9:46 AM PT)

Abel's narration: **"the cookbook on fireworks has more examples. we're going to use muse glimmer to fine tune it on some data set."**

The recipe slide, verbatim:

1. **THE MODEL** — Muse Glimmer 30B + LoRA rank 8. SFT free until Nov 30.
2. **THE DATA** — 600 prompts from the cookbook's prompt-router case study.
3. **THE SURFACE** — Serverless Training: your process runs the loop. No upload.
4. **THE EVAL** — Base vs tuned on 40 held-out prompts, same decoding.

Same four-part shape as the earlier MEASURE IT slide (models / benches / grader / dial → model / data / surface / eval). This is the exact recipe the cloned notebook 3 implements — and the exact recipe Torque's own run on Abel's Fireworks account is following (spawned ~9:41 AM PT; the cookbook's other case studies are the "more examples" Abel noted).

## Slide: "TRAIN IT — One row of training data" (photo, ~9:46 AM PT)

Verbatim substance:

"Chat JSONL, one example per line. The model learns to answer the user turn with a compact JSON decision. Loss lands only on the assistant reply. The prepare step renders one row with the Muse Glimmer tokenizer to confirm it."

The row's anatomy, as diagrammed: **system** (classifier intro + JSON schema, no rule) → **user** (example shown: "Design a sharded rate limiter...") → **reply** (complexity, math, code, reasoning, route) → **loss** (only on the reply tokens) → **result** (a LoRA adapter in your account).

Footer: "Your own data uses the same format: {"messages": [system, user, assistant]}." — i.e., the same starter trains on Abel's own chat JSONL later; nothing about the format is router-specific.

## The dataset, verified on Hugging Face (~9:49 AM PT)

Abel's pointer ("prompt routing dataset on hugginface") checked directly against the HF API: **SupraLabs/Prompt-Routing-Dataset**, public, **MIT license**, last modified 2026-07-05. One train split of **992 examples** (single file, `router_dataset_openai_gpt-oss-120b.jsonl` — the labels were generated with gpt-oss-120b). Columns: `prompt`, `full_answer`, `complexity_score`, `primary_domain`, `coding_task`, `math_task`, `requires_reasoning`, `routing_choice`, `routing_justification` — which map one-to-one onto the router's output JSON (complexity / math / code / reasoning / route). The dataset card's stated purpose: train "Edge Orchestrators and Routing Models" so small local models don't attempt multi-step math or complex software tasks they would botch. The notebook samples 600 of the 992 (seed-0 shuffle) — so the router's training labels are another model's judgments, which is the audit caveat from earlier stated at the source.

## Notebook 3 intro, photographed (~9:49 AM PT) — matches the cloned repo verbatim

Abel photographed the top of `muse_glimmer_train_router.ipynb` ("Part III: Train Muse Glimmer to be the router"). Its text matches the copy Torque cloned, including: "In Part II we built a router by hand: measure, make a table, put a classifier in front. Here we **train a model to make the decision itself**." Data line confirms the counts: "public SupraLabs/Prompt-Routing-Dataset on Hugging Face (**992 prompts; we train on 600**)". The promo boundary is stated in the notebook itself: "The free promotion covers LoRA SFT jobs **started before 2026-12-01 00:00 PT**. It does not cover RL, DPO, full-parameter training, deployments, or sampling outside the training run. The Serverless path samples about 80 answers to compare base and tuned; that sampling is billed at normal per-token rates, and `launch` prints the cost." And the data-handling promise: "This notebook never calls `datasets.upload`. Data stays local (built from Hugging Face) and is streamed by the Serverless Training client." Setup cell is the cookbook clone + pinned install (transformers==5.10.4) that Torque's own run is executing. (The photo shows only the placeholder `fw-...` for the API key — no real key on screen.)

## Notebook 2 — the reasoning-effort sweep (photos, ~9:33 AM PT)

`muse_reasoning_sweep.ipynb`, in the presenter's words: "Same short-answer suite as the Muse vs DeepSeek demo, but Muse only, sweeping the full effort ladder: minimal → low → medium → high → xhigh → max." And the stated point: **"more effort is not always better on these easy short-answer tasks (Muse often peaks at low)."**

Setup (legible in the photos): `RUN_SWEEP = True`, `N_PER_BENCH = 100`, `EFFORTS = ["minimal", "low", "medium", "high", "xhigh", "max"]` (with the comment that Muse rejects "none"), `MUSE = "Muse Spark Open"`. Results cache to the shared `results.jsonl`; the sweep fills only missing (Muse, effort, id) rows and reuses the existing low / partial high cache. The scoreboard is a pivot of pass@1 by bench × effort.

**Results — EXACT, from the repo README (my chart-photo readings matched these to the decimal):**

| Bench | minimal | low | medium | high | xhigh | max |
|---|---:|---:|---:|---:|---:|---:|
| GSM8K | 98 | **99** | **99** | 94 | 98 | 97 |
| BoolQ | **93** | 90 | **93** | 86 | 89 | 84 |
| NQ-Open | 64 | **69** | 67 | 64 | 66 | 65 |
| ARC-Easy | 95 | **96** | 92 | 83 | 85 | 86 |
| **Overall** | 87.5 | **88.5** | 87.8 | 81.8 | 84.5 | 83.0 |

The README's own summary: "On these easy tasks Muse peaks at `low`, with `minimal` and `medium` within a point. Higher effort costs more tokens and lowers pass@1. **Part of the `max` drop is truncation: 19 of 400 `max` answers were empty because reasoning used up the 2,048-token output limit.**" Chart saved by the notebook as `muse_effort_sweep.png` (also in the cloned repo).

Abel's follow-up, in his words (~9:37 AM PT): **"the cut off is usually at the medium effort reasoning — more effort does not mean better results."** The exact table backs the shape of that: the plateau is low–medium (88.5 / 87.8 overall; GSM8K ties low and medium at 99), and the cliff comes after medium — high drops to 81.8. So the useful cutoff is right where he put it: past medium you're paying more to get less.

Abel's reaction, in his words: **"you would assume more reasoning would lead to better results."** It doesn't here — that's the demo's designed point, and now there's a concrete mechanism for part of it: at max effort the model sometimes thinks so long it runs out of output budget and returns *nothing*. The rest is the usual overthinking tax on easy questions — second-guessing and drift, paid for in extra tokens. Reasoning effort pays off on hard multi-step problems, not one-line answers. Same lesson as the head-to-head setup: measure on YOUR task type instead of assuming.

## Sibling experiment spotted in the same repo (photo, ~9:33 AM PT)

Abel also photographed the GitHub preview of a different notebook in the presenter's repo: `experiments/reasoning-effort-uipad/uipad_reasoning_sweep.ipynb` (1,342 lines). Its centerpiece: **"Efficiency frontier — all models (up-and-left is better)"** — pass@1 (zoomed) against cost per successful task ($, log scale) for four models (K3, Opus 4.8, 5.6 Sol, 5.5), each traced across effort levels. Every model's line rises from "none" to a peak around low–high, then bends back down at max — more cost, less accuracy. Its per-type code lists answer types counting / yes-no / string / **coords** — a vision-QA suite, unlike the text-only Meta hackathon one. Same lesson from the cost side: the winner is the cheapest point on the frontier, not the most reasoning you can buy.

## Abel's question during the session (~9:24 AM PT): can the router pick from more than two models?

Abel's definition, in his words: route means picking one model from a list of models. He asked whether a third system can intelligently route between the models, and whether you can route more than two at the same time.

Answer (Torque, in-session): yes — a router is just a classifier, and two models is the smallest case, not the limit. The workshop's notebook 3 trains Glimmer to pick between two; the same setup extends to N models by making the router's output one label out of N:

- **Labels come from the benchmark:** run every candidate model over the test set and grade deterministically; each prompt's label is the model that did best on it (ties broken by cheapest/fastest that still passes).
- **Router:** fine-tune the small model (Glimmer) to predict that label from the prompt alone.
- **At run time:** the router sees the prompt and picks exactly one model from the list — only that model runs, so you pay for the router plus one model, never all of them.
- **What gets harder with more models:** you need enough graded examples per model or the rare classes never get picked; and you want a confidence fallback — when the router is unsure, send the prompt to the strongest default model instead of guessing.
- **Not the same as an ensemble:** routing picks one; ensembling runs several and combines answers. Routing is the cheap one.

RobotForge note: what the live endpoint has today is a *fallback chain* (Baseten primary → Fireworks on failure), which reacts to errors. A router would be the step before that — choosing per request, e.g. by description type — and its training labels could come straight from the existing 24-description sweep results.

**What the workshop's own router actually is (exact, from the repo README):** notebook 3 fine-tunes **Muse Glimmer 30B with LoRA SFT** on the SupraLabs/Prompt-Routing-Dataset (600 training prompts). Given a prompt, the tuned model returns JSON — `complexity`, `math`, `code`, `reasoning`, `route` — and the router sends the prompt to **DeepSeek V4.1 Flash (small route) or Muse Spark Open (big route)**. Base vs tuned on 40 held-out prompts: **route accuracy 22.5% → 90.0%**; exact match on all fields 2.5% → 57.5%; unterminated answers 6 → 0 (McNemar: 22 fixed, 0 broken, p = 4.8e-7). Training cost $0 under the promotion; the tuned LoRA deploys as `muse-router-demo` and bills per GPU-hour, so the README says to delete the deployment afterward. LoRA SFT is free for jobs started before 2026-12-01. Also relevant: the same repo's root README lists a sibling experiment, `experiments/difficulty-router-langchain` — "Does routing easy tasks to a cheap model and hard ones to a strong model cut cost per successful task without losing accuracy?" — the routing question asked in exactly Abel's terms.

## Why this maps to Abel's work

- The recipe is the same discipline RobotForge already uses: fix the models and the effort level, run a fixed set of benches, grade with plain code instead of a model judge, then vary one dial at a time. RobotForge's own provider sweep did the equivalent for the describe step (fixed 24-description set, code-side parsing/validation, per-provider results) — and Agents 102 made the same point for verification: deterministic first, judge second.
- "No LLM judge" is the load-bearing line: a grader you can re-run in plain Python gives the same verdict every time, which is what makes a low-vs-xhigh effort comparison mean anything.

## Not captured

- Unlike Sessions 1–2, Abel did no hands-on build in this session — there is no Session 3 project tree in this repo, only these notes. The notebook and experiments repo above are the presenter's, shown on the stream.
- ~~The head-to-head results table and reasoning-sweep results as exact numbers~~ — RESOLVED ~9:35 AM PT: Abel asked whether the official repo had been pulled; it was then found (public, `sinanuozdemir/ai-experiments`) and cloned, and the exact tables above now come from its README. Only the presenter's `results.jsonl` raw cache is not in the repo.
- Abel's screenshots of the stream are not uploaded here (this repo is pushed through a text-only path; the screenshots stay in Abel's own media library).

## Audit of the presenter's repo (Torque, ~9:40 AM PT, at Abel's request)

Read after cloning: `run_simple_bench.py`, all three notebooks including their stored outputs, `MUSE_AHEAD.md`, `.gitignore`.

**Verified — README claims match the code and the stored outputs:**
- Grading is exactly as advertised: deterministic Python, no LLM judge (number within 1%, yes/no match, string normalized alias match, choice letter match); temperature 0; seed 7; the named dataset splits.
- Head-to-head: the demo notebook's stored output reads "Muse Spark Open: 88.5% / DeepSeek V4.1 Flash: 86.5% / Muse lead: +2.0 pp, n=100/bench" — matches the README table. `MUSE_AHEAD.md` adds the paired count: of 400 items, Muse wins 16, DeepSeek wins 8, 376 tie — the +2.0 is real but thin.
- Sweep: the notebook's stored output reproduces the overall-by-effort line exactly (87.5 / 88.5 / 87.8 / 81.8 / 84.5 / 83.0, "peak effort: low").
- Router: stored outputs match the README to the decimal — base route accuracy 0.225 → tuned 0.900, exact match 0.025 → 0.575, unterminated 6 → 0, McNemar 22 fixed / 0 broken, p = 4.77e-07; LoRA rank 8 / alpha 32, 1 epoch, 560 train + 40 holdout from the 600-prompt dataset; training $0 under the promotion (deadline 2026-12-01, confirmed in the run plan output).
- No secrets: `.gitignore` excludes `.env` and `*.jsonl`; a scan of the repo found no API keys.

**Caveats — where the repo can't prove its own numbers, or the method has soft edges:**
1. `results.jsonl` is gitignored, so the raw per-item data is NOT in the repo. The tables rest on the notebooks' stored outputs, not on data a reader can recompute. The "19 of 400 max answers empty" claim likewise can't be recounted from the repo — it's plausible (the code caps output at 2,048 tokens and an empty answer scores 0), but it is the author's word.
2. `run_simple_bench.py` defaults to `N_PER_BENCH = 40`; the n=100 comes from the notebooks / CLI flag. Running the script bare would silently sample 40.
3. String grading is lenient: normalized substring containment in either direction counts as correct. Same rule for both models, but NQ-Open — Muse's biggest win (+7) — is the bench it inflates most.
4. Extractors grade the LAST number / yes-no / letter anywhere in the full answer text (string uses the last line only). By design with the "final answer on the last line" system prompt, but a wandering answer is graded on its last stray token.
5. A failed API call is written as score 0 and marked done — the resume logic never retries it. `summarize()` skips failed rows; the notebook pivots average the score column including any. Whether any failures sit inside the published numbers can't be told from the repo.
6. The router is evaluated on 40 held-out prompts, and its labels are the dataset's own complexity/route judgments — the tuned Glimmer learns to imitate those labels (90% agreement), which is not the same as measuring which downstream model actually answers better. For a RobotForge-style router, labels from measured outcomes (like the 24-description sweep) would be the stronger version.
7. `MUSE_AHEAD.md` is candidly a slide deck: its talking point reads "UiPad *coordinates* favor DeepSeek; drop that panel," and the SII panel is explicitly the benches where Muse leads. Cherry-picked, but labeled as such in the file itself.

**Verdict:** honest workshop code — no fabrication found; every headline number in the README traces to a stored notebook output or the grading code. The limits are reproducibility (raw data withheld by the gitignore) and small samples, not honesty.
