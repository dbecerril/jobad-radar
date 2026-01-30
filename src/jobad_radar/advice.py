from openai import OpenAI

from .config import settings


client = OpenAI(api_key=settings.openai_api_key)


def advise_study_plan(
    skill_freqs: dict[str, int],
    tool_freqs: dict[str, int],
    current_plan: str,
) -> str:
    """
    Use a stronger reasoning model to advise how to rebalance
    a 4-week study plan based on job-market signals.
    """

    prompt = f"""
You are a senior technical career advisor.

User background:
- PhD in physics
- Strong optics and scientific background
- Transitioning into applied ML / computer vision roles
- Goal: maximize interview readiness in the next 4 weeks

Observed job-market signals (from real job ads):

Top skills (frequency across jobs):
{skill_freqs}

Top tools (frequency across jobs):
{tool_freqs}

Current 4-week preparation plan:
{current_plan}

Task:
- Recommend how to rebalance the 4-week plan.
- Be concrete and practical.
- Say what to emphasize, what to reduce, and what to defer.
- Focus on interview-relevant skills, not academic depth.
- Assume limited time and cognitive load.

Output format:
- Short intro (2–3 lines)
- Bullet-point recommendations grouped by week
- Optional final note on priorities or trade-offs
"""

    response = client.responses.create(
        model=settings.reasoning_model,
        input=prompt,
        temperature=0.3,
    )

    return response.output_text
from openai import OpenAI
from .config import settings

client = OpenAI(api_key=settings.openai_api_key)


def update_study_plan(
    current_plan: str,
    skill_freqs: dict[str, int],
    tool_freqs: dict[str, int],
) -> str:
    """
    Update an existing study plan conservatively based on job-market signals.
    """

    prompt = f"""
You are a senior technical career advisor.

The user already has a 4-week study plan.
Your task is to UPDATE it, not replace it.

STRICT RULES:
- Keep the same 4-week structure.
- Make minimal, conservative changes.
- Reorder, emphasize, or slightly trim topics.
- Do NOT add new weeks.
- Do NOT remove entire weeks.
- Preserve the original style and formatting.

Job-market signals (aggregated from real job ads):

Skills frequency:
{skill_freqs}

Tools frequency:
{tool_freqs}

Current study plan (edit this):
----------------
{current_plan}
----------------

Return ONLY the updated study plan.
Do NOT add explanations or commentary outside the plan.
"""

    response = client.responses.create(
        model=settings.reasoning_model,
        input=prompt,
        temperature=0.2,
    )

    return response.output_text
# advice.py
# advice.py

import json
from .analytics import build_fit_features

# advice.py

import json
from .analytics import build_fit_features


import json
from .analytics import build_fit_features
from .model import LLMFitAssessment
from pydantic import ValidationError

def llm_fit_score(client, job, profile) -> dict:
    """
    LLM-based judgement of job–candidate fit.
    """

    features = build_fit_features(job, profile)
    features_json = json.dumps(features, ensure_ascii=False, indent=2)

    prompt = f"""
You are a senior technical recruiter for physics, optics, and machine learning roles.

Evaluate how well the candidate fits the job described below.

Return ONLY valid JSON with this structure:

{{
  "fit_score_1to10": number,
  "summary": string,
  "strengths": [string, ...],
  "gaps": [string, ...],
  "recommendation": string
}}

Input:
{features_json}
"""

    response = client.responses.create(
        model=settings.reasoning_model,
        input=prompt,
        temperature=0.2,
    )

    # ---- SAFE OUTPUT EXTRACTION ----
    if hasattr(response, "output_text") and response.output_text:
        raw_text = response.output_text
    else:
        raw_text = response.output[0].content[0].text

    try:
        parsed = json.loads(raw_text)
        return LLMFitAssessment(**parsed)
    except (json.JSONDecodeError, ValidationError) as e:
        return LLMFitAssessment(
            fit_score_1to10=0.0,
            summary="Invalid or unparseable LLM output.",
            strengths=[],
            gaps=["LLM output could not be validated"],
            recommendation="Ignore this assessment.",
        )
