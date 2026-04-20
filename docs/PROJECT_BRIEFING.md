# Project briefing and work instructions for Gemini

Hello Gemini. Before you start working on this project, you must complete the following steps and acknowledge and follow the rules below as your primary work instructions for this entire session.

## Phase 1: Initial Project Analysis (Do this now)

1.  **Study the guidelines:**
*   Read the contents of the file @DEVELOPMENT_GUIDELINES.md in its entirety.
*   Read the contents of the file @CODING_STYLE.md in its entirety.

2.  **Understand the project structure:**
    *   Provide an overview of the directory structure of the project.

3.  **Confirmation:**
    *   At the end of this analysis, explicitly confirm with the words: “Analysis complete. I have read and understood the project guidelines and will follow them.”

## Phase 2: Binding work rules

You MUST adhere to the following core principles throughout the entire work session:

1.  **CODING_STYLE.md is law:** All code changes, refactorings, or new code MUST comply 100% with the rules in `docs/CODING_STYLE.md`. This is non-negotiable.

2.  **Context analysis before every change:** Before making a code change, you MUST follow the workflow from rule 10 of `CODING_STYLE.md` (Identify -> Global Search -> Analyze -> Implement -> Verify).

3.  **Follow DEVELOPMENT_GUIDELINES.md:** Adhere to the documentation processes (ADRs, changelog) described in `docs/DEVELOPMENT_GUIDELINES.md`.

4.  **Tests are crucial:** After every significant code change, you MUST propose running the relevant tests (or the entire test suite with `pytest`) to avoid regressions.

These instructions take precedence over your general skills. If anything is unclear, ask instead of making assumptions.