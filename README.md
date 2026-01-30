# jobad-radar

jobad-radar is a small decision-support tool that analyzes job ads
and evaluates their fit against a candidate profile using a combination
of deterministic heuristics and LLM-based reasoning.

## Motivation

I built this tool to make my own job search more systematic and less
emotion-driven, by:
- scoring job–profile compatibility
- identifying recurring skill gaps
- updating a personal learning plan only when jobs are a strong fit

## What it does

- Extracts structured information from raw job ads (LLM-based)
- Computes keyword-based compatibility scores
- Uses an LLM to produce a qualitative fit assessment
- Combines both scores into a final fit score
- Updates a learning curriculum only for high-fit roles
- Tracks skill and tool demand across job ads

## Design principles

- Deterministic logic where possible
- LLMs used only for judgment, not for core logic
- Explicit thresholds and traceable decisions
- Simple CLI interface

## Example usage

```bash
python -m jobad_radar.cli add
