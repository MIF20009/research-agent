from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional

from src.app.db.models.embedding import Embedding
from src.app.tools.openai_client import embed_text


def get_embedding(db: Session, kind: str, paper_id: int) -> Optional[Embedding]:
    stmt = (
        select(Embedding)
        .where(Embedding.kind == kind, Embedding.paper_id == paper_id)
        .limit(1)
    )
    return db.execute(stmt).scalar_one_or_none()


def get_or_create_paper_embedding(db: Session, paper_id: int, text: str) -> Embedding:
    kind = "paper_abstract"
    existing = get_embedding(db, kind=kind, paper_id=paper_id)
    if existing:
        return existing

    vec = embed_text(text)

    row = Embedding(
        kind=kind,
        paper_id=paper_id,
        run_id=None,
        vector=vec,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
