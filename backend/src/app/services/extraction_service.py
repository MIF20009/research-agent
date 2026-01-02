from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional
from src.app.db.models.extraction import Extraction


def save_extraction(
    db: Session,
    run_id: int,
    paper_id: int,
    data: dict,
) -> Extraction:
    e = Extraction(
        run_id=run_id,
        paper_id=paper_id,
        data=data,  
    )
    db.add(e)
    db.commit()
    db.refresh(e)
    return e

def get_latest_extraction_for_paper(db: Session, paper_id: int) -> Optional[Extraction]:
    stmt = (
        select(Extraction)
        .where(Extraction.paper_id == paper_id)
        .order_by(Extraction.id.desc())
        .limit(1)
    )
    return db.execute(stmt).scalar_one_or_none()