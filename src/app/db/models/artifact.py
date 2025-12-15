from sqlalchemy import Integer, ForeignKey, String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from src.app.db.base import Base

class Artifact(Base):
    __tablename__ = "artifacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id", ondelete="CASCADE"), nullable=False, index=True)

    # "synthesis", "gaps", "contradictions", "hypotheses"
    kind: Mapped[str] = mapped_column(String(50), nullable=False)

    content: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
