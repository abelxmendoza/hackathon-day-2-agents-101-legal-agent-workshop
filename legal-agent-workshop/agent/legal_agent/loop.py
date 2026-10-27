"""The Legal Agent: the agentic loop.

run_agent works the case; resume_run continues a run that stopped.
"""

from __future__ import annotations

import json
from pathlib import Path

from openai import OpenAI

from agent_kit import progress, tools
from agent_kit.settings import case_dir, model

NUDGE = (
    "Call exactly one tool this turn; never answer in plain text. "
    "When every checklist item is settled, file the memo with submit_memo."
)
LAST_TURN = (
    "This is your last turn. Call exactly one tool: file the memo now "
    "with submit_memo, using what you have."
)


def run_agent(*, root: Path, client: OpenAI, turns: int = 30) -> dict:
    instructions = (Path(__file__).parent / "system_instructions.md").read_text()
    objective = (case_dir(root) / "objective.md").read_text()
    run_id = progress.new_run(root, instructions=instructions, objective=objective)
    messages = [{"role": "user", "content": objective}]
    status, note = _work(root, run_id, client, messages, instructions, turns)
    return _result(root, run_id, status, note)


def resume_run(*, root: Path, run_id: str, client: OpenAI, turns: int = 15) -> dict:
    saved = progress.load_progress(root, run_id)
    step = progress.resume(root, run_id)
    if step["message"] is None:
        return {
            "run_id": run_id,
            "status": step["status"],
            "turn": saved["turn"],
            "note": step["note"],
        }
    instructions = (root / "workspace/runs" / run_id / "instructions.md").read_text()
    messages = saved["messages"] + [{"role": "user", "content": step["message"]}]
    status, note = _work(root, run_id, client, messages, instructions, turns)
    return _result(root, run_id, status, note)


def _work(
    root: Path,
    run_id: str,
    client: OpenAI,
    messages: list,
    instructions: str,
    budget: int,
) -> tuple[str, str]:
    """The turn loop: one model call per turn; the model picks one tool; the kit
    runs it and the result is fed back. Returns (status, note) when the run stops."""
    offered = tools.definitions(root, run_id)
    for turn in range(1, budget + 1):
        if turn == budget:
            messages.append({"role": "user", "content": LAST_TURN})
        try:
            response = client.responses.create(
                model=model(),
                instructions=instructions,
                input=messages,
                tools=offered,
            )
        except Exception as error:  # a model API failure pauses the run; it can resume
            progress.save_progress(root, run_id, messages, status="paused")
            return "paused", f"model call failed: {error}"
        messages += list(response.output)
        calls = [item for item in response.output if item.type == "function_call"]
        if not calls:
            messages.append({"role": "user", "content": NUDGE})
            progress.save_progress(root, run_id, messages, response)
            continue
        status = "running"
        for call in calls:
            result = tools.run(client, root, run_id, call)
            messages.append(
                {
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": json.dumps(result),
                }
            )
            if result.get("status"):
                status = result["status"]
                break
        progress.save_progress(root, run_id, messages, response, status=status)
        if status != "running":
            return status, ""
    progress.save_progress(root, run_id, messages, status="paused")
    return "paused", ""


def _result(root: Path, run_id: str, status: str, note: str) -> dict:
    return {
        "run_id": run_id,
        "status": status,
        "turn": progress.load_progress(root, run_id)["turn"],
        "note": note,
    }
