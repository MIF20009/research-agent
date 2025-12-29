from sqlalchemy.orm import Session
from src.app.db.models.artifact import Artifact


def save_artifact(db: Session, run_id: int, kind: str, content: str) -> Artifact:
    a = Artifact(run_id=run_id, kind=kind, content=content)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a