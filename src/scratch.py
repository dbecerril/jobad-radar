from jobad_radar.model import JobAd, CandidateProfile
from jobad_radar.analytics import compatibility_score_1to10, combined_fit_score, compute_skill_frequencies, compute_tool_frequencies    
from jobad_radar.advice import llm_fit_score
from jobad_radar.study_plan import load_study_plan, update_study_plan
from jobad_radar.storage import load_jobs
from openai import OpenAI
from jobad_radar.config import settings

# ----------------------------
# Setup
# ----------------------------
client = OpenAI(api_key=settings.openai_api_key)
profile = CandidateProfile()

# ----------------------------
# Test job ad
# ----------------------------
job = JobAd(
    id="test",
    title="Computer Vision Engineer",
    company="ACME",
    source="test",
    location="Remote",
    remote_allowed=True,
    contract_type="Permanent",
    seniority="Junior",
    domain_tags=["Computer Vision"],
    must_have_skills=["Python", "PyTorch", "Computer Vision"],
    nice_to_have_skills=["TensorFlow"],
    ml_topics=["segmentation"],
    ml_tools=["pytorch"],
    optics_topics=[],
    optics_tools=[],
    raw_text="We are looking for a computer vision engineer with Python and PyTorch.",
)

# ----------------------------
# Step 1: Heuristic score
# ----------------------------
heuristic_score = compatibility_score_1to10(job, profile)
print("Heuristic (keyword) score:", heuristic_score)

# ----------------------------
# Step 2: LLM assessment
# ----------------------------
llm_assessment = llm_fit_score(client, job, profile)
print("LLM assessment:", llm_assessment)

# ----------------------------
# Step 3: Combined score
# ----------------------------
total_score = combined_fit_score(
    heuristic_score_1to10=heuristic_score,
    llm_score_1to10=llm_assessment.fit_score_1to10,
)

print("TOTAL FIT SCORE:", total_score)

# ----------------------------
# Step 4: Gated curriculum update
# ----------------------------
THRESHOLD = 7.0

if total_score >= THRESHOLD:
    print("✅ High-fit job detected → updating study plan")

    current_plan = load_study_plan()
    jobs = load_jobs()

    # Aggregate signals ONLY from stored jobs
    skill_freqs = compute_skill_frequencies(jobs)
    tool_freqs = compute_tool_frequencies(jobs)

    updated_plan = update_study_plan(
        current_plan=current_plan,
        skill_freqs=skill_freqs,
        tool_freqs=tool_freqs,
    )

    print("Updated study plan preview:")
    print(updated_plan[:500], "...")
else:
    print("⏭ Job below threshold → study plan unchanged")
from jobad_radar.storage import load_jobs
from jobad_radar.analytics import (
    compute_skill_frequencies,
    compute_ml_frequencies,
    compute_optics_frequencies,
)
from jobad_radar.visualization import plot_top_frequencies

jobs = load_jobs()

skill_freqs = compute_skill_frequencies(jobs)
ml_freqs = compute_ml_frequencies(jobs)
optics_freqs = compute_optics_frequencies(jobs)

plot_top_frequencies(
    skill_freqs,
    title="Top skills across all job ads",
)

plot_top_frequencies(
    ml_freqs,
    title="Top ML topics & tools",
)

plot_top_frequencies(
    optics_freqs,
    title="Top Optics topics & tools",
)
