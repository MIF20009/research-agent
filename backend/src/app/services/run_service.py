from sqlalchemy.orm import Session
from src.app.db.models.run import Run
from src.app.schemas.run import RunCreate

def create_run(db= Session, payload= RunCreate) -> Run:
    run = Run(
        topic = payload.topic,
        notes = payload.notes,
        status = "created"
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run

def list_runs(db: Session) -> list[Run]:
    return db.query(Run).all()