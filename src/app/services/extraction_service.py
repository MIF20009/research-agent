from sqlalchemy.orm import Session
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
