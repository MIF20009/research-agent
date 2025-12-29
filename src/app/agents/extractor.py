from src.app.services.extraction_service import save_extraction
from src.app.graph.state import AgentState
from src.app.tools.openai_client import extract_paper_fields


def extractor_agent(state: AgentState) -> AgentState:
    db = state["db"]
    run_id = state["run_id"]
    papers = state.get("papers", [])
    extractions = []

    for p in papers:
        title = p.get("title") or ""
        abstract = p.get("abstract") or ""
        paper_id = p.get("id")

        extracted = extract_paper_fields(title=title, abstract=abstract)

        # Persist extraction
        save_extraction(db, run_id=run_id, paper_id=paper_id, data=extracted)

        # Also keep it in state for the next agents
        extractions.append({
            "paper_id": paper_id,
            "title": title,
            "extracted": extracted,
        })

    state["extractions"] = extractions
    return state
