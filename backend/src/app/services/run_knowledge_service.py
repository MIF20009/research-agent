from sqlalchemy.orm import Session
from src.app.db.models.extraction import Extraction
from src.app.db.models.paper import Paper


def build_run_evidence(db: Session, run_id: int, max_items: int = 12) -> str:
    """
    Build a compact evidence text from DB (papers + extractions)
    that we can feed to an LLM for synthesis/gaps/hypotheses.

    We keep it short to control token usage.
    """
    q = (
        db.query(Extraction, Paper)
        .join(Paper, Paper.id == Extraction.paper_id)
        .filter(Extraction.run_id == run_id)
        .order_by(Extraction.id.desc())
        .limit(max_items)
    )

    blocks = []
    for ex, paper in q.all():
        d = ex.data or {}
        blocks.append(
            f"""PAPER: {paper.title or "unknown"} ({paper.year or "unknown"})
            DOI: {paper.doi or "unknown"}
            URL: {paper.url or "unknown"}
            PROBLEM: {d.get("problem", "unknown")}
            METHOD: {d.get("method", "unknown")}
            DATA/DOMAIN: {d.get("dataset_or_domain", "unknown")}
            KEY RESULTS: {d.get("key_results", "unknown")}
            LIMITATIONS: {d.get("limitations", "unknown")}
            ---"""
                    )

    return "\n".join(blocks)
