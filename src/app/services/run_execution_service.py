from sqlalchemy.orm import Session
from src.app.db.models.run import Run
from src.app.core.enums import RunStatus


def execute_run(db: Session, run: Run):
    try:
        # 1. mark running
        run.status = RunStatus.RUNNING.value
        db.commit()

        # 2. (placeholder) agent pipeline execution
        # In Step 8+, LangGraph will be called here
        # graph.invoke(...)

        # 3. mark completed
        run.status = RunStatus.COMPLETED.value
        db.commit()

    except Exception as e:
        run.status = RunStatus.FAILED.value
        db.commit()
        raise e
