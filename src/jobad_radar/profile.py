from pydantic import BaseModel, Field
from typing import List


class CandidateProfile(BaseModel):
    """
    User-editable snapshot of your current skill set.
    This file is meant to be modified as your profile evolves.
    """

    name: str = "David Becerril"

    domains: List[str] = Field(
        default_factory=lambda: [
            "Computer Vision",
            "Data Science",
            "Optics",
            "Opto-electronics",
            "Applied Machine Learning",
        ]
    )

    tools: List[str] = Field(
        default_factory=lambda: [
            "Python",
            "NumPy",
            "Pandas",
            "scikit-learn",
            "PyTorch",
            "TensorFlow",
            "OpenCV",
            "ONNX",
            "Matplotlib",
            "Git",
            "C++",
            "COMSOL",
            "MEEP",
            "Zemax",
        ]
    )

    ml_topics: List[str] = Field(
        default_factory=lambda: [
            "classification",
            "segmentation",
            "object detection",
            "feature extraction",
            "data augmentation",
            "model fine-tuning",
            "model evaluation",
            "CNNs",
        ]
    )

    optics_topics: List[str] = Field(
        default_factory=lambda: [
            "system design",
            "zemax",
            "fiber optics",
            "precision optics",
            "laser systems",
            "opto-electronics",
        ]
    )
