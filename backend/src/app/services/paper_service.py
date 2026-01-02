from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Dict, Any, Optional

from src.app.db.models.paper import Paper


def upsert_paper(db: Session, data: Dict[str, Any]) -> Paper:
    """
    Insert a paper if (source, source_id) not موجود.
    Otherwise update basic fields and return the existing record.
    """
    source = data.get("source")
    source_id = data.get("source_id")

    stmt = select(Paper).where(Paper.source == source, Paper.source_id == source_id)
    existing: Optional[Paper] = db.execute(stmt).scalar_one_or_none()

    if existing:
        # update fields if newly available
        existing.title = data.get("title") or existing.title
        existing.year = data.get("year") or existing.year
        existing.doi = data.get("doi") or existing.doi
        existing.abstract = data.get("abstract") or existing.abstract
        existing.url = data.get("url") or existing.url
        db.commit()
        db.refresh(existing)
        return existing

    paper = Paper(
        source=source,
        source_id=source_id,
        title=data.get("title"),
        year=data.get("year"),
        doi=data.get("doi"),
        abstract=data.get("abstract"),
        url=data.get("url"),
    )
    db.add(paper)
    db.commit()
    db.refresh(paper)
    return paper
