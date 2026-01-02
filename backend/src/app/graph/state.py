from typing import TypedDict, List, Dict, Any, Optional
from sqlalchemy.orm import Session


class AgentState(TypedDict, total=False):
    db: Session
    run_id: int
    topic: str

    papers: List[Dict[str, Any]]
    extractions: List[Dict[str, Any]]

    synthesis: Optional[str]
    gaps: Optional[str]
    hypotheses: Optional[str]
