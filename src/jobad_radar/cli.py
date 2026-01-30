import sys
from .workflows import add_job_workflow


def read_multiline_input() -> str:
    print(
        "Paste the job ad text below.\n"
        "Finish with Ctrl+D (Linux/macOS) or Ctrl+Z + Enter (Windows).\n"
    )
    return sys.stdin.read().strip()


def main():
    if len(sys.argv) < 2:
        print("Usage: jobad-radar add")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add":
        raw_text = read_multiline_input()
        if not raw_text:
            print("No text provided.")
            return

        result = add_job_workflow(raw_text)

        print("\n--- Job processed ---")
        print("Saved:", result["saved"])
        print("Heuristic score:", result["heuristic"])
        print("LLM score:", result["llm"].fit_score_1to10)
        print("Total score:", result["total"])
        print("Study plan updated:", result["study_plan_updated"])

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
