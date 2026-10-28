# Hackathon Workshops — Agents 101 + Agents 102: Legal Agent Workshop

**Meta Global AI Developer Hackathon — live workshop sessions, October 27–28, 2026**

This repo groups my work from the hackathon's live agent workshops together: both
sessions build on the same project — Meta's Legal Agent Workshop — so they live
here as one project with two sessions, not as separate repos.

## The workshop (Meta's names)

- **Project:** [`meta-models/legal-agent-workshop`](https://github.com/meta-models/legal-agent-workshop) — "Legal Agent Workshop" (handbook: *Building a Multimodal Document Agent with Muse Code*)
- Participants clone Meta's workshop repo and launch Muse Code from `agent/` only, building a legal case-investigation agent for the fictional case **Northbridge v. Caldera** using Muse Code and Muse Spark (Meta Model API).

## Sessions

### Session 1 — Agents 101 (Tue Oct 27, 9:00–10:00 AM PT, presenter Suraj Subramanian)

- **Build:** the agentic loop in `legal-agent-workshop/agent/legal_agent/loop.py` (`run_agent` + `resume_run`) on Meta's pre-built kit — one tool per turn, stop statuses (answered / needs_input / awaiting_signoff / paused), paused-save on API error or turn-budget exhaustion, memo filed by the model through `submit_memo`. The implementation converged point-for-point with the presenter's on-stage reference build (same stop set, same resume semantics, compile-verified, `legal_agent/loop.py` the only file changed).
- A completed reference run from the session: 21 turns, status *answered* — the agent's memo concluded Caldera knew of 21 open Severity-1 defects while certifying zero, with its evidence gaps named honestly in the memo itself.
- **Notes:** [`agents-101-notes-2026-10-27.md`](agents-101-notes-2026-10-27.md) — kit map, the case, the loop contract the offline tests pin, and the Session 2 preview.

### Session 2 — Agents 102: Verifiable Agents (Wed Oct 28, 9:00 AM PT)

- **Build:** the verification layer in `legal-agent-workshop/agent/verification/` — the checks the tools call at fixed points so the agent cannot skip them.
  - `verify_checklist.py` — **built.** Does the agent's checklist cover the case's ground truth? Muse Spark marks each ground-truth item covered or not; code turns that into a score. Feedback points to what kind of question is missing without ever quoting, paraphrasing, or counting the ground-truth items.
  - `verify_memo.py` — **built and executed.** The memo rules: every item proven or escalated, every citation matching a recorded fact, nothing confidential cited, signature checks consistent, no open evidence requests. Run against scripted memos: a partial memo is refused with named problems; a complete memo passes. No model call — the memo is compared with the case record in code.
  - `verify_checklist.py` additionally hardened during the session: the judge's coverage answer is accepted as a mapping, a list of covered ids, or a list of {id, covered} objects (a live run elsewhere crashed on the list shape).
  - Pre-built by Meta: the evidence-request check, the claims check, escalation after refused memos, and attorney sign-off.
- **Notes:** [`agents-102-notes-2026-10-28.md`](agents-102-notes-2026-10-28.md) — session flow (incl. the Session 1 recap run: memo filed, checklist 5/5 proven), verification patterns, and what maps to my own project.

## What's intentionally not in this copy

- `agent/.env` (API key file — never committed), `agent/.venv/`, and `agent/workspace/` runtime data (seeded inbox copies and run state).
- The binary case documents (the fictional case PDFs, page-render PNGs, and one photo in `cases/` and `world/follow_up/`) — this upload went through a text-only path. The originals are in Meta's upstream repo, linked above; everything needed to read the code, handbook, and notes is here.

## Credit

Workshop materials © Meta / the `meta-models` workshop team — see the upstream repo. The case, parties, and documents are entirely fictional. Session builds and notes by Abel Mendoza, built with AI assistance (Muse Spark via the Meta Model API in the product; Muse Spark / Torque assisted the build in the workshop sessions).
