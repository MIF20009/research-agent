import os
import json
import re
from typing import Dict, Any
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _strip_code_fences(s: str) -> str:
    # removes ```json ... ``` or ``` ... ```
    s = s.strip()
    s = re.sub(r"^```(?:json)?\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*```$", "", s)
    return s.strip()


def extract_paper_fields(title: str, abstract: str) -> Dict[str, Any]:
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    prompt = f"""
Extract structured information from the following paper title and abstract.

Return ONLY valid JSON (no markdown, no code fences), with keys:
problem, method, dataset_or_domain, key_results, limitations

Rules:
- Each value should be 1–3 short sentences.
- If a field is missing, use "unknown".

Title: {title}
Abstract: {abstract}
""".strip()

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You output strictly valid JSON only."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    text = resp.choices[0].message.content.strip()
    text = _strip_code_fences(text)

    return json.loads(text)
