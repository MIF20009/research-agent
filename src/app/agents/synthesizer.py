from src.app.graph.state import AgentState


def synthesizer_agent(state: AgentState) -> AgentState:
    topic = state["topic"]
    extractions = state.get("extractions", [])

    synthesis_lines = [f"Synthesis for topic: {topic}", f"Reviewed {len(extractions)} papers."]

    # simple aggregation (MVP)
    for i, ex in enumerate(extractions[:5], start=1):
        title = ex.get("title", "unknown")
        extracted = ex.get("extracted", {})
        synthesis_lines.append(f"{i}. {title} — method: {extracted.get('method','unknown')}")

    state["synthesis"] = "\n".join(synthesis_lines)
    state["gaps"] = "Open gaps: derived from extracted limitations (MVP)."
    return state
