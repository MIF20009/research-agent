from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from src.app.db.base import Base
from src.app.core.enums import RunStatus

class Run(Base):
    __tablename__ = "runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    topic: Mapped[str] = mapped_column(String(300), nullable=False)
    status: Mapped[RunStatus] = mapped_column(String(50), nullable=False, default=RunStatus.CREATED.value)

    # Store filters or extra info as text for now (we’ll improve later)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
