from pathlib import Path
from jobad_radar.config import settings
from openai import OpenAI
# ----------------------------
# Setup
# ----------------------------
client = OpenAI(api_key=settings.openai_api_key)

PLAN_PATH = Path("data/study_plan.md")


def load_study_plan() -> str:
    if not PLAN_PATH.exists():
        raise FileNotFoundError(
            "study_plan.md not found. Create it in data/ first."
        )
    return PLAN_PATH.read_text(encoding="utf-8")


def save_study_plan(updated_plan: str):
    PLAN_PATH.write_text(updated_plan, encoding="utf-8")


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
        model= settings.reasoning_model,
        input=prompt,
        temperature=0.2,
    )

    return response.output_text