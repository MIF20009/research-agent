import json
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.app.db.models.retrieval_cache import RetrievalCache


def get_cached_payload(
    db: Session,
    topic: str,
    source: str = "openalex",
    ttl_hours: int = 24,
) -> Optional[Dict[str, Any]]:
    stmt = (
        select(RetrievalCache)
        .where(RetrievalCache.topic == topic, RetrievalCache.source == source)
        .order_by(RetrievalCache.id.desc())
        .limit(1)
    )
    row = db.execute(stmt).scalar_one_or_none()
    if not row:
        return None

    # TTL check
    created = row.created_at
    if created.tzinfo is None:
        created = created.replace(tzinfo=timezone.utc)

    if datetime.now(timezone.utc) - created > timedelta(hours=ttl_hours):
        return None

    return json.loads(row.payload)


def save_payload(
    db: Session,
    topic: str,
    payload: Dict[str, Any],
    source: str = "openalex",
) -> None:
    row = RetrievalCache(
        topic=topic,
        source=source,
        payload=json.dumps(payload),
    )
    db.add(row)
    db.commit()
