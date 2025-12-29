from src.app.graph.state import AgentState
from src.app.services.run_knowledge_service import build_run_evidence
from src.app.tools.openai_client import generate_review_outputs


def synthesizer_agent(state: AgentState) -> AgentState:
    db = state["db"]
    run_id = state["run_id"]
    topic = state["topic"]

    evidence = build_run_evidence(db, run_id=run_id, max_items=12)
    outputs = generate_review_outputs(topic=topic, evidence=evidence)

    # synthesis should be a string
    state["synthesis"] = outputs.get("synthesis", "")

    # gaps should be a list -> convert to readable bullets
    gaps = outputs.get("gaps", [])
    if isinstance(gaps, list):
        state["gaps"] = "\n".join([f"- {g}" for g in gaps])
    else:
        state["gaps"] = str(gaps)

    # hypotheses should be a list -> convert to readable paragraphs
    hyps = outputs.get("hypotheses", [])
    if isinstance(hyps, list):
        formatted = []
        for i, h in enumerate(hyps, start=1):
            if isinstance(h, dict):
                hyp = _pick(h, "hypothesis", "statement", "Hypothesis", "claim")
                rat = _pick(h, "rationale", "reason", "Rationale", "justification")
                val = _pick(h, "validation", "test", "Validation", "evaluation")

                # If model returned a dict but not in expected keys, fallback to stringify dict
                if not hyp and not rat and not val:
                    formatted.append(f"Hypothesis {i}: {str(h)}")
                else:
                    formatted.append(
                        f"Hypothesis {i}: {hyp}\n"
                        f"Rationale: {rat}\n"
                        f"Validation: {val}"
                    )
            else:
                formatted.append(f"Hypothesis {i}: {str(h)}")
        state["hypotheses"] = "\n\n".join(formatted)
    else:
        state["hypotheses"] = str(hyps)

    print("HYPOTHESES RAW:", outputs.get("hypotheses"))

    return state

def _pick(d: dict, *keys: str) -> str:
    for k in keys:
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""