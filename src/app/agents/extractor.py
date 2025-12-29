from src.app.graph.state import AgentState
from src.app.tools.openai_client import extract_paper_fields
from src.app.services.extraction_service import save_extraction, get_latest_extraction_for_paper
from src.app.services.embedding_service import get_or_create_paper_embedding


def extractor_agent(state: AgentState) -> AgentState:
    db = state["db"]
    run_id = state["run_id"]
    papers = state.get("papers", [])

    extractions = []

    for p in papers:
        paper_id = p.get("id")
        title = p.get("title") or ""
        abstract = p.get("abstract") or ""

        text_to_embed = abstract.strip() or title.strip()
        if text_to_embed:
            get_or_create_paper_embedding(db, paper_id=paper_id, text=text_to_embed)

        cached = get_latest_extraction_for_paper(db, paper_id=paper_id)

        if cached:
            extracted = cached.data
        else:
            extracted = extract_paper_fields(title=title, abstract=abstract)
            save_extraction(db, run_id=run_id, paper_id=paper_id, data=extracted)

        extractions.append({
            "paper_id": paper_id,
            "title": title,
            "extracted": extracted,
        })

    state["extractions"] = extractions
    return state
