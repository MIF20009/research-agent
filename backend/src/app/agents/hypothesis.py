from src.app.graph.state import AgentState


def hypothesis_agent(state: AgentState) -> AgentState:
    topic = state["topic"]
    state["hypotheses"] = (
        f"Hypothesis for {topic}: "
        "If placeholder X is improved, placeholder Y increases under condition Z."
    )
    return state
