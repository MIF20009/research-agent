from typing import List, Dict, Any
from src.app.tools.openalex_client import search_works_by_topic


def retrieve_papers_for_topic(topic: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    High-level retrieval function.

    Currently uses OpenAlex only, but later we can:
    - combine with Semantic Scholar
    - add deduplication
    - add caching
    """
    papers = search_works_by_topic(topic, max_results=max_results)
    return papers
