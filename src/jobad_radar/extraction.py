from __future__ import annotations

from typing import List
from datetime import datetime

from openai import OpenAI

from .config import settings
from .model import JobAd


client = OpenAI(api_key=settings.openai_api_key)


SYSTEM_PROMPT = """
You are an assistant that extracts structured information from job ads.
IMPORTANT:
- Output MUST be strict JSON.
- Do NOT include comments, explanations, or trailing text.
- Do NOT use markdown.
Your task: read the raw text of a job description and fill a JobAd object.

Rules:
- Be concise and standardized in skill names.
- Use lower_snake_case or simple lowercase phrases for skills (e.g., 'docker', 'fastapi', 'azure_databricks').
- If something is not specified, leave the field empty or use 'Unknown' where appropriate.
- Use domain_tags as high-level topics like 'computer_vision', 'recommender_systems', 'optics', 'mlops', etc.
- seniority must be one of: 'Junior', 'Mid', 'Senior', 'Lead', 'Unknown'.
- contract_type must be one of: 'Permanent', 'Freelance', 'Internship', 'Unknown'.
"""


def _generate_job_id(title: str) -> str:
    """
    Simple helper to generate a reproducible-ish ID string.
    You can replace this later with something more robust.
    """
    slug = title.lower().replace(" ", "_")[:40]
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"{ts}_{slug}"


def extract_job_ad(raw_text: str, *, source: str | None = None) -> JobAd:
    """
    Use the OpenAI client to extract a structured JobAd from raw text.
    """

    # We'll do structured output via JSON mode (no explicit Pydantic integration needed here).
    response = client.responses.create(
        model=settings.extraction_model,
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
                + "\n\n"
                + "IMPORTANT: Respond with ONLY valid JSON. No explanations, no markdown.",
            },
            {"role": "user", "content": raw_text},
        ],
        temperature=0.0,
    )

    # Extract JSON from the response
    #json_str = response.output[0].content[0].text
    import json

        # ---- SAFE JSON EXTRACTION ----
    if hasattr(response, "output_text") and response.output_text:
        raw_text = response.output_text
    else:
        raw_text = response.output[0].content[0].text

    import json

    try:
        raw_data = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            "Failed to parse JobAd JSON from LLM output.\n"
            "Raw LLM output was:\n"
            f"{raw_text}"
        ) from e

    data = normalize_llm_output(raw_data)

    title = data.get("title")
    if not title:
        raise RuntimeError(
            "Model response JSON missing required 'title' field "
            f"after normalization. Raw output was:\n{response.output_text}"
        )


    # Fill in missing bits & raw_text
    if "id" not in data or not data["id"]:
        data["id"] = _generate_job_id(data["title"])

    data.setdefault("company", None)
    data.setdefault("location", None)
    data.setdefault("remote_allowed", None)
    data.setdefault("contract_type", "Unknown")
    data.setdefault("seniority", "Unknown")
    data.setdefault("source", source)
    data.setdefault("domain_tags", [])
    data.setdefault("must_have_skills", [])
    data.setdefault("nice_to_have_skills", [])
    data.setdefault("ml_topics", [])
    data.setdefault("metrics", [])
    data.setdefault("tools", [])

    # Add raw_text; JobAd will add created_at itself
    data["raw_text"] = raw_text
    # Normalize generic 'skills' field if present
    skills = data.pop("skills", [])

    if skills:
        data.setdefault("must_have_skills", [])
        data.setdefault("ml_tools", [])

        for s in skills:
            s_l = s.lower()
            if s_l in {"python", "numpy", "opencv", "pytorch", "tensorflow"}:
                data["ml_tools"].append(s)
            else:
                data["must_have_skills"].append(s)

    # Let Pydantic validate & coerce to JobAd
    job_ad = JobAd(**data)
    return job_ad

def normalize_llm_output(data: dict) -> dict:
    """
    Normalize LLM output keys to match JobAd schema.
    This is REQUIRED because LLMs do not guarantee field names.
    """

    # ---- Title ----
    if "title" not in data:
        if "job_title" in data:
            data["title"] = data.pop("job_title")

    # ---- Skills ----
    if "must_have_skills" not in data:
        if "required_skills" in data:
            data["must_have_skills"] = data.pop("required_skills")

    if "nice_to_have_skills" not in data:
        if "optional_skills" in data:
            data["nice_to_have_skills"] = data.pop("optional_skills")

    # ---- Safety defaults ----
    data.setdefault("must_have_skills", [])
    data.setdefault("nice_to_have_skills", [])
    data.setdefault("domain_tags", [])

    return data
