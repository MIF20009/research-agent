import requests
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from src.app.services.retrieval_cache_service import (
    get_cached_payload,
    save_payload,
)


def _fetch_from_openalex(topic: str, max_results: int = 10) -> List[Dict[str, Any]]:
    url = "https://api.openalex.org/works"
    params = {
        "search": topic,
        "per-page": max_results,
    }

    resp = requests.get(url, params=params, timeout=20)
    resp.raise_for_status()
    data = resp.json()

    papers = []
    for w in data.get("results", []):
        papers.append({
            "source": "openalex",
            "source_id": w.get("id"),
            "title": w.get("title"),
            "year": w.get("publication_year"),
            "doi": w.get("doi"),
            "abstract": w.get("abstract"),
            "url": w.get("id"),
        })

    return papers


def retrieve_papers_for_topic(
    db: Session,
    topic: str,
    max_results: int = 10,
) -> List[Dict[str, Any]]:

    cached = get_cached_payload(
        db=db,
        topic=topic,
        source="openalex",
        ttl_hours=24,
    )

    if cached and "papers" in cached:
        print("OpenAlex cache HIT")
        return cached["papers"][:max_results]

    print("OpenAlex cache MISS → fetching")
    papers = _fetch_from_openalex(topic, max_results=max_results)

    save_payload(
        db=db,
        topic=topic,
        payload={"papers": papers},
        source="openalex",
    )

    return papers
