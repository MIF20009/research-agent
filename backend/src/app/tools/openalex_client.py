import os
from typing import List, Dict, Any
import requests


OPENALEX_BASE_URL = "https://api.openalex.org/works"


def search_works_by_topic(topic: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Simple OpenAlex search by topic string.

    Returns a list of dicts with:
    - source: "openalex"
    - source_id: openalex id
    - title
    - abstract
    - year
    - doi (if any)
    - url (landing page)
    """
    params = {
        "search": topic,
        "per-page": max_results,
    }

    # Optional: polite usage (you can add your email here)
    mailto = os.getenv("OPENALEX_MAILTO")
    if mailto:
        params["mailto"] = mailto

    resp = requests.get(OPENALEX_BASE_URL, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    results = []
    for item in data.get("results", []):
        openalex_id = item.get("id")
        title = item.get("title")
        publication_year = item.get("publication_year")
        doi = item.get("doi")
        primary_location = item.get("primary_location") or {}
        landing_page = primary_location.get("landing_page_url")

        # abstracts_inverted_index is a weird structure; we’ll just join tokens if present
        abstract_text = None
        abstract_inv = item.get("abstract_inverted_index")
        if abstract_inv:
            # flatten inverted index into ordered tokens
            # keys = word, values = positions
            # we invert that mapping
            pos_to_word = {}
            for word, positions in abstract_inv.items():
                for p in positions:
                    pos_to_word[p] = word
            tokens = [w for _, w in sorted(pos_to_word.items(), key=lambda x: x[0])]
            abstract_text = " ".join(tokens)

        results.append(
            {
                "source": "openalex",
                "source_id": openalex_id,
                "title": title,
                "abstract": abstract_text,
                "year": publication_year,
                "doi": doi,
                "url": landing_page,
            }
        )

    return results
