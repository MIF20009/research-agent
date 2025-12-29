from src.app.graph.state import AgentState


def synthesizer_agent(state: AgentState) -> AgentState:
    topic = state["topic"]
    extractions = state.get("extractions", [])

    synthesis = (
        f"Synthesis for topic: {topic}\n"
        f"Reviewed {len(extractions)} papers.\n"
        "Key trends: placeholder trend.\n"
    )
    gaps = "Open gaps: placeholder gap 1; placeholder gap 2."

    state["synthesis"] = synthesis
    state["gaps"] = gaps
    return state
