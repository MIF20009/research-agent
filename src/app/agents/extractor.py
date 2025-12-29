from src.app.graph.state import AgentState


def extractor_agent(state: AgentState) -> AgentState:
    papers = state.get("papers", [])
    extractions = []

    for p in papers:
        extractions.append({
            "paper_source": p.get("source"),
            "paper_source_id": p.get("source_id"),
            "title": p.get("title"),
            "year": p.get("year"),
            "doi": p.get("doi"),
            "url": p.get("url"),
            # placeholders for now – later we will use LLMs to fill these
            "problem": "TODO: problem (LLM extraction)",
            "method": "TODO: method (LLM extraction)",
            "result": "TODO: result (LLM extraction)",
            "limitation": "TODO: limitation (LLM extraction)",
        })

    state["extractions"] = extractions
    return state
