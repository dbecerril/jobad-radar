from __future__ import annotations

from collections import Counter
from typing import Dict, List

from .model import JobAd 
from .profile import CandidateProfile
from .config import SKILL_ALIASES, normalize_term, expand_profile_skills


def compute_skill_frequencies(jobs: List[JobAd]) -> Dict[str, int]:
    counter = Counter()
    for job in jobs:
        counter.update(job.must_have_skills)
        counter.update(job.nice_to_have_skills)
    return dict(counter)


def compute_tool_frequencies(jobs: List[JobAd]) -> Dict[str, int]:
    counter = Counter()
    for job in jobs:
        counter.update(job.ml_tools)
        counter.update(job.optics_tools)
    return dict(counter)


def compatibility_score(job: JobAd, profile: CandidateProfile) -> float:
    score = 0.0
    max_score = 1e-6  # avoid division by zero

    your_skills = expand_profile_skills(profile)
    your_domains = {normalize_term(d) for d in profile.domains}

    def has_skill(skill: str) -> bool:
        s = normalize_term(skill)

        # Direct match
        if s in your_skills:
            return True

        # Alias match
        for canonical, variants in SKILL_ALIASES.items():
            canon_norm = normalize_term(canonical)
            variant_norms = {normalize_term(v) for v in variants}

            if s == canon_norm or s in variant_norms:
                if (
                    canon_norm in your_skills
                    or any(v in your_skills for v in variant_norms)
                ):
                    return True

        return False

    # Must-have skills
    for skill in job.must_have_skills:
        max_score += 2.0
        if has_skill(skill):
            score += 2.0

    # Nice-to-have skills
    for skill in job.nice_to_have_skills:
        max_score += 1.0
        if has_skill(skill):
            score += 1.0

    # ML tools
    for tool in job.ml_tools:
        max_score += 1.5
        if has_skill(tool):
            score += 1.5

    # Optics tools
    for tool in job.optics_tools:
        max_score += 1.5
        if has_skill(tool):
            score += 1.5

    # Domain tags
    for tag in job.domain_tags:
        max_score += 1.0
        if normalize_term(tag) in your_domains:
            score += 1.0

    return min(1.0, score / max_score)


def compatibility_score_1to10(job: JobAd, profile: CandidateProfile) -> float:
    return round(compatibility_score(job, profile) * 10, 1)


def build_fit_features(job: JobAd, profile: CandidateProfile) -> dict:
    """
    Structured, deterministic summary of job–candidate fit.
    This is fed to the LLM, logged, and used for analysis.
    """
    return {
        "job": {
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "source": job.source,
            "location": job.location,
            "remote_allowed": job.remote_allowed,
            "contract_type": job.contract_type,
            "seniority": job.seniority,
            "domain_tags": job.domain_tags,
            "must_have_skills": job.must_have_skills,
            "nice_to_have_skills": job.nice_to_have_skills,
            "ml_topics": job.ml_topics,
            "ml_tools": job.ml_tools,
            "optics_topics": job.optics_topics,
            "optics_tools": job.optics_tools,
            "raw_text": job.raw_text,
        },
        "candidate": {
            "name": profile.name,
            "domains": profile.domains,
            "tools": profile.tools,
            "ml_topics": profile.ml_topics,
            "optics_topics": profile.optics_topics,
        },
        "heuristics": {
            "keyword_score_1to10": compatibility_score_1to10(job, profile),
        },
    }
def combined_fit_score(
    heuristic_score_1to10: float,
    llm_score_1to10: float,
    *,
    heuristic_weight: float = 0.6,
) -> float:
    llm_weight = 1.0 - heuristic_weight
    return round(
        heuristic_weight * heuristic_score_1to10
        + llm_weight * llm_score_1to10,
        1,
    )
from collections import Counter
from typing import Dict, List
from .model import JobAd


def compute_ml_frequencies(jobs: List[JobAd]) -> Dict[str, int]:
    """
    Aggregate ML-related topics and tools across job ads.
    """
    counter = Counter()
    for job in jobs:
        counter.update(job.ml_topics)
        counter.update(job.ml_tools)
    return dict(counter)


def compute_optics_frequencies(jobs: List[JobAd]) -> Dict[str, int]:
    """
    Aggregate optics-related topics and tools across job ads.
    """
    counter = Counter()
    for job in jobs:
        counter.update(job.optics_topics)
        counter.update(job.optics_tools)
    return dict(counter)
