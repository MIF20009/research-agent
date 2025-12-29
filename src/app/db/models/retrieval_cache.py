from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from src.app.db.base import Base


class RetrievalCache(Base):
    __tablename__ = "retrieval_cache"

    id = Column(Integer, primary_key=True)
    topic = Column(String(500), nullable=False, index=True)
    source = Column(String(50), nullable=False)  # openalex
    payload = Column(Text, nullable=False)       # json string
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
