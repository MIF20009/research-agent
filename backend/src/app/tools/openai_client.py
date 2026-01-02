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

def embed_text(text: str) -> list[float]:
    model = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
    resp = client.embeddings.create(model=model, input=text)
    return resp.data[0].embedding

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

def generate_review_outputs(topic: str, evidence: str) -> Dict[str, Any]:
    """
    Produce synthesis, gaps/contradictions, and hypotheses grounded in evidence.
    Returns a JSON object with keys:
    synthesis, gaps, hypotheses
    """
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    prompt = f"""
    You are an academic research assistant.

    TOPIC: {topic}

    EVIDENCE PACK (each entry contains extracted fields from a paper):
    {evidence}

    Task:
    Return ONLY valid JSON with keys:
    1) synthesis: a short literature overview (8-12 lines), grouping papers into themes/trends.
    2) gaps: list 3-5 bullet points of open research gaps AND contradictions (if none, return empty array []). Each bullet must reference paper titles (short).
    3) hypotheses: a JSON array of 3–5 objects.
        Each object MUST have exactly these keys:
        - hypothesis
        - rationale
        - validation
        All values must be non-empty strings.

    Rules:
    - Do NOT invent citations. Use only paper titles that appear in the evidence pack.
    - Do NOT add "No clear contradictions found" anywhere. If none, contradictions must be [].
    """.strip()

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Return strictly valid JSON only."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
    )

    return json.loads(resp.choices[0].message.content)