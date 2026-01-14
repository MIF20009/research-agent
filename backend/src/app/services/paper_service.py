from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Dict, Any, Optional, List

from src.app.db.models.paper import Paper
from src.app.db.models.run_paper import RunPaper


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


def link_paper_to_run(db: Session, run_id: int, paper_id: int) -> RunPaper:
    """Link a paper to a run"""
    run_paper = RunPaper(run_id=run_id, paper_id=paper_id)
    db.add(run_paper)
    db.commit()
    db.refresh(run_paper)
    return run_paper


def get_papers_for_run(db: Session, run_id: int) -> List[Dict[str, Any]]:
    """Get all papers linked to a run formatted for agent processing"""
    stmt = select(Paper).join(RunPaper).where(RunPaper.run_id == run_id)
    papers = db.execute(stmt).scalars().all()
    
    return [
        {
            "id": p.id,
            "source": p.source,
            "source_id": p.source_id,
            "title": p.title,
            "year": p.year,
            "doi": p.doi,
            "abstract": p.abstract,
            "url": p.url,
        }
        for p in papers
    ]
