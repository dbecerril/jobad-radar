from __future__ import annotations
from typing import List, Optional, Literal
from datetime import datetime

from pydantic import BaseModel, Field


Seniority = Literal["Junior", "Mid", "Senior", "Lead", "Unknown"]
ContractType = Literal["Permanent", "Freelance", "Internship", "Unknown"]


class JobAd(BaseModel):
    """
    Canonical structured representation of a job ad.
    Everything else in the project will work with this model.
    """

    id: str = Field(
        ...,
        description="Internal identifier, e.g. '2026-01-29_streaming_applied_ds'",
    )
    title: str
    company: Optional[str] = None
    source: Optional[str] = Field(
        default=None, description="Where you found it (LinkedIn, company site, etc.)"
    )

    location: Optional[str] = None
    remote_allowed: Optional[bool] = None
    contract_type: ContractType = "Unknown"
    seniority: Seniority = "Unknown"

    domain_tags: List[str] = Field(
        default_factory=list,
        description="High-level domains like 'Computer Vision', 'Recommender Systems', 'Optics'",
    )

    # Core skill buckets
    must_have_skills: List[str] = Field(default_factory=list)
    nice_to_have_skills: List[str] = Field(default_factory=list)

    # More specific ML / DS aspects
    ml_topics: List[str] = Field(
        default_factory=list,
        description="Concepts like 'segmentation', 'recommender systems', 'transformers'",
    )

#    ml_metrics: List[str] = Field(
#        default_factory=list,
#        description="Metrics explicitly mentioned, e.g. 'Precision@K', 'IoU', 'MAE'",
#    )

    ml_tools: List[str] = Field(
        default_factory=list,
        description="Libraries / platforms like 'PyTorch', 'Azure', 'Docker', 'FastAPI'",
    )

    # More specific Optics Engineer aspects

    optics_topics: List[str] = Field(
        default_factory=list,
        description="Concepts like 'system design', 'zemax', 'fiber optics'",
    )

    optics_tools: List[str] = Field(
        default_factory=list,
        description="Tools like 'Zemax', 'OpticStudio', 'CAD software'",
    )

    # Full text for RAG / reference
    raw_text: str

    # Housekeeping
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When this entry was created in your system.",
    )

    class Config:
        # In Pydantic v2 this is a bit different, but keep it simple
        arbitrary_types_allowed = True

class CandidateProfile(BaseModel):
    """
    Snapshot of your current skill set.
    We'll use this to compare against JobAd.must_have_skills, etc.
    """

    name: str = "David Becerril"

    # High-level tags
    domains: List[str] = Field(
        default_factory=lambda: [
            "Computer Vision",
            "Data Science",
            "Optics",
            "Opto-electronics",
            "Applied Machine Learning"

        ]
    )

    # Tools you already know to a comfortable level
    tools: List[str] = Field(
        default_factory=lambda: [
            "Python",
            "NumPy",
            "Pandas",
            "scikit-learn",
            "PyTorch",
            "OpenCV",
            "Matplotlib",
            "COMSOL",
            "MEEP",
            "Zemax",
            "R",
            "Git",
            "C++",
            "TensorFlow",          # if you’ve read / run models, even lightly
            "ONNX",   
        ]
    )

    # ML topics you have genuine hands-on experience with
    ml_topics: List[str] = Field(
        default_factory=lambda: [
            "classification",
            "segmentation",
            "feature extraction",
            "dimensionality reduction",
            "PCA",
            "clustering",
            "CNNs","object detection",
            "model fine-tuning",
            "data augmentation",
            "model evaluation",
        ]
    )
    # Optics topics you have genuine hands-on experience with
    optics_topics: List[str] = Field(
        default_factory=lambda: [
            "system design",
            "zemax",
            "fiber optics",
            "precision optics",
            "opto-electronics",
            "end-to-end simulations",
            "Simulation of optical systems",
            "laser systems",
        ]
    )   


from pydantic import BaseModel, Field
from typing import List, Optional


class LLMFitAssessment(BaseModel):
    fit_score_1to10: float = Field(..., ge=1, le=10)
    summary: str
    strengths: List[str]
    gaps: List[str]
    recommendation: str
