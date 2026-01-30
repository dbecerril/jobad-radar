from pydantic_settings import BaseSettings
from pydantic import Field
from .profile import CandidateProfile


class Settings(BaseSettings):
    openai_api_key: str = Field(alias="OPENAI_API_KEY")

    # Explicit model roles
    extraction_model: str = Field(
        default="gpt-4.1-mini",
        alias="OPENAI_EXTRACTION_MODEL",
    )

    reasoning_model: str = Field(
        default="gpt-4.1",
        alias="OPENAI_REASONING_MODEL",
    )

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

# somewhere in config.py or similar
SKILL_ALIASES = {
    "python": {"python3"},
    "pytorch": {"torch", "py torch"},
    "tensorflow": {"tf"},
    "computer vision": {"cv", "image processing", "vision"},
    "deep learning": {"dl"},
    "near-field optics": {"snom", "near field", "near-field"},
    "u-net": {"unet", "u net"},
    # extend as you see repeated patterns
}

def normalize_term(term: str) -> str:
    return term.strip().lower().replace("-", " ").replace("_", " ")

def expand_profile_skills(profile: CandidateProfile) -> set[str]:
    base = {normalize_term(s) for s in (profile.tools + profile.ml_topics)}
    expanded = set(base)

    for canonical, variants in SKILL_ALIASES.items():
        canon_norm = normalize_term(canonical)
        if canon_norm in base or any(normalize_term(v) in base for v in variants):
            expanded.add(canon_norm)
            expanded.update(normalize_term(v) for v in variants)

    return expanded

