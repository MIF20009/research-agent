from sqlalchemy import Integer, String, Text, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.app.db.base import Base

class Paper(Base):
    __tablename__ = "papers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Source identifiers
    source: Mapped[str] = mapped_column(String(50), nullable=False)  # "openalex", "semanticscholar", "arxiv"
    source_id: Mapped[str] = mapped_column(String(200), nullable=False)

    title: Mapped[str] = mapped_column(Text, nullable=False)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    doi: Mapped[str | None] = mapped_column(String(200), nullable=True)

    abstract: Mapped[str | None] = mapped_column(Text, nullable=True)
    url: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint("source", "source_id", name="uq_papers_source_sourceid"),
    )
