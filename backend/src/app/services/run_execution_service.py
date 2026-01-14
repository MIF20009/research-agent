from sqlalchemy.orm import Session
from src.app.db.models.run import Run
from src.app.core.enums import RunStatus
from src.app.graph.lit_review_graph import build_lit_review_graph
from src.app.services.artifact_service import save_artifact
from src.app.services.paper_service import get_papers_for_run


def execute_run(db: Session, run: Run):
    try:
        # 1. mark running
        run.status = RunStatus.RUNNING.value
        db.commit()

        # 2. agent pipeline execution
        graph = build_lit_review_graph()

        # Get papers if they were uploaded with this run
        papers = []
        if run.upload_papers:
            papers = get_papers_for_run(db, run.id)

        initial_state = {
            "run_id": run.id,
            "topic": run.topic,
            "upload_papers": run.upload_papers,
            "papers": papers,
            "db": db
        }
        final_state = graph.invoke(initial_state)

        # Save artifacts (so you can view results)
        if final_state.get("synthesis"):
            save_artifact(db, run.id, "synthesis", final_state["synthesis"])
        if final_state.get("gaps"):
            save_artifact(db, run.id, "gaps", final_state["gaps"])
        if final_state.get("hypotheses"):
            save_artifact(db, run.id, "hypotheses", final_state["hypotheses"])

        # 3. mark completed
        run.status = RunStatus.COMPLETED.value
        db.commit()

    except Exception as e:
        db.rollback()
        run.status = RunStatus.FAILED.value
        db.commit()
        raise e
