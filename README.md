# Hackathon Day 2 Workshop — Agents 101: Legal Agent Workshop

**Meta Global AI Developer Hackathon — Day 2, Tuesday October 27, 2026**

This repo holds my work from the hackathon's Day 2 live workshop session.

## The workshop (Meta's names)

- **Session:** Agents 101 — the hands-on "Agent Workshop" (live, 9:00–10:00 AM PT, presenter Suraj Subramanian)
- **Workshop title (handbook):** *Building a Multimodal Document Agent with Muse Code*
- **Upstream repo:** [`meta-models/legal-agent-workshop`](https://github.com/meta-models/legal-agent-workshop) — "Legal Agent Workshop"

Participants clone Meta's workshop repo and launch Muse Code from `agent/` only, building a legal case-investigation agent for the fictional case **Northbridge v. Caldera** using Muse Code and Muse Spark (Meta Model API).

## What's in here

- **`legal-agent-workshop/`** — the workshop tree (code and docs) as worked in the session.
  - **Session 1 build:** the agentic loop implemented in `legal-agent-workshop/agent/legal_agent/loop.py` (`run_agent` + `resume_run`) on Meta's pre-built kit — one tool per turn, stop statuses (answered / needs_input / awaiting_signoff / paused), paused-save on API error or turn-budget exhaustion, memo filed by the model through `submit_memo`. The implementation converged point-for-point with the presenter's on-stage reference build (same stop set, same resume semantics, compile-verified, `legal_agent/loop.py` the only file changed).
  - A completed reference run from the session: 21 turns, status *answered* — the agent's memo concluded Caldera knew of 21 open Severity-1 defects while certifying zero, with its evidence gaps named honestly in the memo itself.
- **`agents-101-notes-2026-10-27.md`** — my session notes: kit map, the case, the loop contract the offline tests pin, and the Session 2 verification layer preview (verify memo/checklist, branch with verification on, escalation, sign-off).

## What's intentionally not in this copy

- `agent/.env` (API key file — never committed), `agent/.venv/`, and `agent/workspace/` runtime data (seeded inbox copies and run state).
- The binary case documents (the fictional case PDFs, page-render PNGs, and one photo in `cases/` and `world/follow_up/`) — this upload went through a text-only path. The originals are in Meta's upstream repo, linked above; everything needed to read the code, handbook, and notes is here.

## Credit

Workshop materials © Meta / the `meta-models` workshop team — see the upstream repo. The case, parties, and documents are entirely fictional. Session 1 loop implementation and notes by Abel Mendoza, built with AI assistance (Muse Spark via the Meta Model API, per the workshop's design).
