from sqlalchemy import Integer, ForeignKey, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector
from src.app.db.base import Base

class Embedding(Base):
    __tablename__ = "embeddings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # what the embedding is for: "paper_abstract", "claim"
    kind: Mapped[str] = mapped_column(String(50), nullable=False)

    # optional links
    paper_id: Mapped[int | None] = mapped_column(ForeignKey("papers.id", ondelete="CASCADE"), nullable=True, index=True)
    run_id: Mapped[int | None] = mapped_column(ForeignKey("runs.id", ondelete="CASCADE"), nullable=True, index=True)

    # store the vector (dimension will depend on your embedding model; 1536 is common)
    vector: Mapped[list[float]] = mapped_column(Vector(1536), nullable=False)

    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
