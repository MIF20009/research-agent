from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.api.deps import get_db
from src.app.db.models.artifact import Artifact

router = APIRouter(prefix="/runs/{run_id}/artifacts", tags=["artifacts"])


@router.get("")
def list_artifacts(run_id: int, db: Session = Depends(get_db)):
    items = db.query(Artifact).filter(Artifact.run_id == run_id).all()
    return [
        {"id": a.id, "kind": a.kind, "content": a.content, "created_at": a.created_at}
        for a in items
    ]
