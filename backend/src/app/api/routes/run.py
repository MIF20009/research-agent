from fastapi import APIRouter, Depends, Query, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import uuid

from src.app.api.deps import get_db
from src.app.schemas.run import RunCreate, RunOut
from src.app.services.run_service import create_run, list_runs
from src.app.services.run_execution_service import execute_run
from src.app.services.paper_service import upsert_paper, link_paper_to_run
from src.app.db.models.run import Run

router = APIRouter(prefix="/runs", tags=["runs"])


@router.post("", response_model=RunOut)
def create_run_endpoint(payload: RunCreate, db: Session = Depends(get_db)):
    return create_run(db, payload)


@router.get("", response_model=list[RunOut])
def list_runs_endpoint(db: Session = Depends(get_db)):
    return list_runs(db)


@router.get("/{run_id}", response_model=RunOut)
def get_run_endpoint(run_id: int, db: Session = Depends(get_db)):
    run = db.get(Run, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.post("/{run_id}/upload-papers")
def upload_papers_endpoint(
    run_id: int,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """Upload PDF papers for a run"""
    run = db.get(Run, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    if not run.upload_papers:
        raise HTTPException(
            status_code=400,
            detail="This run is not configured for paper uploads"
        )
    
    if len(files) > 20:
        raise HTTPException(
            status_code=400,
            detail="Maximum 20 papers allowed per run"
        )
    
    uploaded_papers = []
    
    try:
        for file in files:
            if file.content_type != 'application/pdf':
                raise HTTPException(
                    status_code=400,
                    detail=f"File {file.filename} is not a PDF"
                )
            
            # Use filename as title
            title = file.filename.replace('.pdf', '').strip() if file.filename else f"Paper_{uuid.uuid4()}"
            
            # Create paper entry
            paper_data = {
                "source": "uploaded",
                "source_id": str(uuid.uuid4()),
                "title": title,
                "year": None,
                "doi": None,
                "abstract": None,
                "url": None,
            }
            
            paper = upsert_paper(db, paper_data)
            link_paper_to_run(db, run_id, paper.id)
            
            uploaded_papers.append({
                "id": paper.id,
                "title": paper.title,
                "source_id": paper.source_id
            })
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
    return {
        "run_id": run_id,
        "papers_uploaded": len(uploaded_papers),
        "papers": uploaded_papers
    }


@router.post("/{run_id}/execute")
def execute_run_endpoint(run_id: int, db: Session = Depends(get_db)):
    run = db.get(Run, run_id)
    if not run: 
        raise HTTPException(status_code=404, detail="Run not found")
    if run.status != "created":
        raise HTTPException(status_code=400, detail="Only runs with status 'created' can be executed")
    execute_run(db, run)
    return {"message": "Run execution started", "run_id": run_id}

