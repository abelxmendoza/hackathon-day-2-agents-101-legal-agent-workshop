"""Session 2, yours: the memo rules.

The checks submit_memo runs on every memo the agent files while verification
is on (agent/agent_kit/tools/submit_memo.py). No model call: these compare
the memo with the case record.

    run_verification(ctx, memo) -> {"passed": bool, "feedback": [problem, ...]}

memo is {"conclusion": str, "findings": [{"item", "status", "summary",
"citations": [{"document_id", "page", "quote"}]}], "gaps": str}; ctx.case is
the run's CaseRecord: case.data["checklist"] (each item has the facts
recorded for it and a needs_signature_check flag), case.data["facts"],
case.data["signature_checks"], case.flagged(document_id), and
case.open_requests(). Compare quotes with agent_kit.document_text.normalize:
facts were checked against the page when they were recorded, so a citation
that matches no recorded fact was never verified anywhere.

Rules (one problem string per break; passed means no problems):
  * every checklist item has a finding in the memo;
  * a finding's status settles its item: "proven" or "escalated"; a finding
    that leaves an item "open" is a problem;
  * a "proven" finding has a recorded fact for its item, and cites at least
    one;
  * every citation matches a recorded fact (same document, page, and quote);
  * no citation comes from a document flagged confidential;
  * a checklist item marked needs_signature_check whose finding says
    "proven" has a signature check on a document it cites, and every such
    check's verdict is "consistent"; a check that is not consistent means
    the signature cannot carry the item — name it as a gap instead of
    marking the item proven;
  * no evidence request is still open.
"""

from __future__ import annotations

from agent_kit import document_text


def run_verification(ctx, memo: dict) -> dict:
    case = ctx.case
    checklist = case.data["checklist"]
    findings = {}
    for finding in memo.get("findings") or []:
        if isinstance(finding, dict) and finding.get("item"):
            findings[finding["item"]] = finding

    problems: list[str] = []

    for item, entry in checklist.items():
        finding = findings.get(item)
        if finding is None:
            problems.append(
                f"the memo has no finding for {item}: "
                "it is neither proven nor escalated"
            )
            continue
        status = finding.get("status")
        if status not in ("proven", "escalated"):
            problems.append(
                f"the finding for {item} is neither proven nor escalated "
                f"(status: {status})"
            )
            continue
        citations = finding.get("citations") or []
        facts = [f for f in case.data["facts"] if f["item"] == item]
        if status == "proven":
            if not facts:
                problems.append(
                    f"the finding for {item} says proven, "
                    "but no fact is recorded for it"
                )
            if not citations:
                problems.append(
                    f"the proven finding for {item} cites nothing"
                )
        cited_docs = []
        for citation in citations:
            doc = citation.get("document_id")
            page = citation.get("page")
            quote = citation.get("quote", "")
            cited_docs.append(doc)
            if case.flagged(doc):
                problems.append(
                    f"{doc} is flagged confidential and can never be cited "
                    f"(finding for {item})"
                )
                continue
            match = any(
                fact["document_id"] == doc
                and int(fact["page"]) == int(page)
                and document_text.normalize(fact["quote"])
                == document_text.normalize(quote)
                for fact in facts
            )
            if not match:
                problems.append(
                    f"the citation to {doc} p{page} for {item} "
                    "has no matching recorded fact"
                )
        if status == "proven" and entry.get("needs_signature_check"):
            checks = [
                check
                for check in case.data["signature_checks"]
                if check.get("document_id") in cited_docs
            ]
            if not checks:
                problems.append(
                    f"the finding for {item} rests on a signature, "
                    "but no cited document was checked"
                )
            for check in checks:
                if check.get("verdict") != "consistent":
                    problems.append(
                        f"{check['document_id']} p{check['page']} is "
                        f"{check.get('verdict')}, so {item} is not proven; "
                        "name it as a gap instead"
                    )

    for request in case.open_requests():
        problems.append(
            f"evidence request {request['id']} for {request['item']}: "
            "this request is still open"
        )

    return {"passed": not problems, "feedback": problems}
