from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.app.api.deps import get_db
from src.app.schemas.run import RunCreate, RunOut
from src.app.services.run_service import create_run, list_runs

router = APIRouter(prefix="/runs", tags=["runs"])


@router.post("", response_model=RunOut)
def create_run_endpoint(payload: RunCreate, db: Session = Depends(get_db)):
    return create_run(db, payload)


@router.get("", response_model=list[RunOut])
def list_runs_endpoint(db: Session = Depends(get_db)):
    return list_runs(db)
