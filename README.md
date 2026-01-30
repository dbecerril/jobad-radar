# jobad-radar

jobad-radar is a small decision-support tool that analyzes job ads and evaluates
their fit against a candidate profile using a combination of deterministic
heuristics and LLM-based reasoning.

It is designed as a personal tool to make job searching more systematic,
traceable, and less emotion-driven.

---

## Motivation

I built this tool to bring structure to my own job search by:

- scoring job–profile compatibility in a consistent way  
- identifying recurring skill and tooling gaps across job ads  
- updating a personal learning plan only when roles are a strong fit  

Rather than reacting to every new posting, the goal is to focus effort where it
matters most.

---

## What it does

- Extracts structured information from raw job ads (LLM-based)
- Computes deterministic, keyword-based compatibility scores
- Uses an LLM to generate a qualitative fit assessment
- Combines both into a final fit score
- Updates a learning curriculum **only** for high-fit roles
- Tracks skill and tool demand across analyzed job ads
- Provides simple analytics and visualizations (e.g. ML vs optics demand)

---

## Design principles

- Deterministic logic where possible  
- LLMs used only for judgment, not for core logic  
- Explicit thresholds and traceable decisions  
- Clear separation between data, analytics, and orchestration  
- Simple CLI-based interface  

This is intentionally not a black-box recommender system.

---

## Setup

The tool maintains local, user-specific state (job history and learning plan)
outside the repository.

Before first use, create a `data/` folder at the project root and add an initial
study plan file.

Example structure:

```text
jobad-radar/
├── data/
│   └── study_plan.txt
The initial study_plan.txt can be simple free text, for example:

- Improve object detection fundamentals
- Review CNN architectures
- Practice PyTorch model fine-tuning
- Learn basic deployment concepts (ONNX, inference)
The study plan is updated over time only when job ads exceed a defined fit
threshold, based on aggregated market signals.

The data/ folder is intentionally ignored by Git and meant to remain local.

Example usage
python -m jobad_radar.cli add