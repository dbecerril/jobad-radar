from openai import OpenAI
from .config import settings
from .extraction import extract_job_ad
from .storage import append_job, load_jobs
from .analytics import (
    compatibility_score_1to10,
    combined_fit_score,
    compute_skill_frequencies,
    compute_tool_frequencies,
)
from .advice import llm_fit_score
from .study_plan import load_study_plan, update_study_plan, save_study_plan
from .profile import CandidateProfile


def add_job_workflow(raw_text: str, *, threshold: float = 6.0):
    client = OpenAI(api_key=settings.openai_api_key)
    profile = CandidateProfile()

    job = extract_job_ad(raw_text, source="interactive")

    saved = append_job(job)

    heuristic = compatibility_score_1to10(job, profile)
    llm = llm_fit_score(client, job, profile)

    total = combined_fit_score(
        heuristic_score_1to10=heuristic,
        llm_score_1to10=llm.fit_score_1to10,
    )

    result = {
        "job": job,
        "saved": saved,
        "heuristic": heuristic,
        "llm": llm,
        "total": total,
    }

    if total >= threshold:
        jobs = load_jobs()
        skill_freqs = compute_skill_frequencies(jobs)
        tool_freqs = compute_tool_frequencies(jobs)

        current_plan = load_study_plan()
        updated_plan = update_study_plan(
            current_plan=current_plan,
            skill_freqs=skill_freqs,
            tool_freqs=tool_freqs,
        )
        save_study_plan(updated_plan)

        result["study_plan_updated"] = True
    else:
        result["study_plan_updated"] = False

    return result
