from src.app.graph.state import AgentState
from src.app.services.retrieval_service import retrieve_papers_for_topic
from src.app.services.paper_service import upsert_paper


def retriever_agent(state: AgentState) -> AgentState:
    topic = state["topic"]
    db = state["db"]

    papers = retrieve_papers_for_topic(db, topic, max_results=10)

    saved = []
    for p in papers:
        row = upsert_paper(db, p)
        saved.append({
            "id": row.id,
            "source": row.source,
            "source_id": row.source_id,
            "title": row.title,
            "year": row.year,
            "doi": row.doi,
            "abstract": row.abstract,
            "url": row.url,
        })

    state["papers"] = saved
    return state
