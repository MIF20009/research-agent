from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from src.app.api.deps import get_db
from src.app.schemas.run import RunCreate, RunOut
from src.app.services.run_service import create_run, list_runs
from src.app.services.run_execution_service import execute_run
from src.app.db.models.run import Run

router = APIRouter(prefix="/runs", tags=["runs"])


@router.post("", response_model=RunOut)
def create_run_endpoint(payload: RunCreate, db: Session = Depends(get_db)):
    return create_run(db, payload)


@router.get("", response_model=list[RunOut])
def list_runs_endpoint(db: Session = Depends(get_db)):
    return list_runs(db)

@router.post("/{run_id}/execute")
def execute_run_endpoint(run_id: int, db: Session = Depends(get_db)):
    run = db.get(Run, run_id)
    if not run: 
        raise HTTPException(status_code=404, detail="Run not found")
    if run.status != "created":
        raise HTTPException(status_code=400, detail="Only runs with status 'created' can be executed")
    execute_run(db, run)
    return {"message": "Run execution started", "run_id": run_id}

