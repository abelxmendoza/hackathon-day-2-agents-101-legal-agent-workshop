"""Does the agent's checklist cover what the case needs? run_verification is not implemented yet.

Called when the agent calls set_checklist with VERIFICATION=on, and by
./helper verify RUN --checklist.

    run_verification(ctx, items) -> {"passed": bool, "score": float, "feedback": str}

- items: the agent's checklist items: [{"id", "question", "evidence_needed", ...}, ...]
- load_reference(ctx.root) (pre-built, below) returns the case's ground truth,
  [{"id": "...", "question": "..."}, ...], or None when the case has none (then the
  checklist passes).

1. Ask Muse Spark (ctx.client.responses.create, JSON output) to mark each reference item
   covered or not by some agent item, even if worded differently, and to write feedback.
2. score = covered reference items / all reference items; passed = every one is covered.
3. feedback: what kind of question the checklist is missing, and any item that only
   restates background. It goes to the agent, so it must point to the direction only:
   never quote, paraphrase, or count the reference items. Empty when it passes.

Only passed and feedback reach the agent; the score is shown in the console.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from agent_kit.settings import case_dir

# ---- pre-built: the ground truth (don't change) ----------------------------------------
# It lives outside this folder (GROUND_TRUTH_DIR, default ../ground_truth), one
# <case folder name>.json per case. Read it only through load_reference.


def reference_path(root: Path) -> Path:
    folder = Path(os.environ.get("GROUND_TRUTH_DIR") or "../ground_truth").expanduser()
    if not folder.is_absolute():
        folder = (Path(root) / folder).resolve()
    return folder / f"{case_dir(root).name}.json"


def load_reference(root: Path) -> list | None:
    """The case's ground-truth items, or None if the case has none."""
    path = reference_path(root)
    return json.loads(path.read_text())["items"] if path.is_file() else None


# ---- yours ---------------------------------------------------------------------------

from typing import cast

from agent_kit.settings import model
from openai.types.responses import Response

PROMPT = """REFERENCE CHECKLIST. The first list is the reference: the questions a complete
checklist for this case must cover. The second list is the agent's checklist.

{reference}

{checklist}

For each reference item, decide whether some agent item covers it, even if it is
worded differently. Also write feedback for the agent: what kind of question the
checklist is missing, and any agent item that only restates background. The feedback
must point to the direction only — never quote, paraphrase, or count the reference
items, and never name their ids.

Answer only with JSON: {{"covered": {{"<reference id>": true or false, ...}},
"feedback": "<feedback, empty if nothing is missing>"}}"""


def run_verification(ctx, items: list) -> dict:
    reference = load_reference(ctx.root)
    if reference is None:
        return {"passed": True, "score": None, "feedback": ""}
    response = cast(
        Response,
        ctx.client.responses.create(
            model=model(),
            input=PROMPT.format(
                reference=json.dumps(reference, indent=1),
                checklist=json.dumps(items, indent=1),
            ),
            text={"format": {"type": "json_object"}},
        ),
    )
    try:
        verdict = json.loads(response.output_text)
        covered_raw = verdict.get("covered") or {}
    except (ValueError, AttributeError):
        return {
            "passed": False,
            "score": 0.0,
            "feedback": "The checklist could not be checked. Try setting it again.",
        }

    def is_covered(ref_id: str) -> bool:
        # The judge is asked for a mapping, but a live model may answer with
        # a list of covered ids, or a list of {id, covered} objects. Accept
        # all three shapes; anything else counts as not covered.
        if isinstance(covered_raw, dict):
            return covered_raw.get(ref_id) is True
        if isinstance(covered_raw, list):
            for entry in covered_raw:
                if isinstance(entry, str) and entry == ref_id:
                    return True
                if isinstance(entry, dict):
                    entry_id = (
                        entry.get("id")
                        or entry.get("item")
                        or entry.get("reference_id")
                    )
                    if entry_id == ref_id:
                        return entry.get("covered") is True
        return False

    score = sum(1 for ref in reference if is_covered(ref.get("id"))) / len(reference)
    passed = score == 1.0
    return {
        "passed": passed,
        "score": score,
        "feedback": "" if passed else (verdict.get("feedback") or ""),
    }
