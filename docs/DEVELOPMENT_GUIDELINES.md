# Development Guidelines: Coherent Documentation Management

This document outlines the strategy for managing documentation within the `ama_b_viewer` project to ensure consistency, clarity, and effective communication among developers. By adhering to these guidelines, we aim to provide a comprehensive understanding of the project's history, current state, and future direction.

## 1. Centralizing Documentation

To streamline access and maintain consistency, all project-relevant documentation will be centralized within the `docs/` directory.

**Proposed Directory Structure:**

```
your_project/
├── docs/
│   ├── adr/
│   │   ├── ADR-001-...md
│   │   ├── ADR-002-...md
│   │   └── ...
│   ├── CHANGELOG.md
│   ├── DEV_TASKS.md
│   ├── README.md (for the docs directory, optional)
│   ├── CONTRIBUTING.md
│   ├── DEVELOPMENT_GUIDELINES.md (this file)
│   └── guides/
│       └── ...
└── ... (rest of project code)
```

**Benefit:** All project documentation is consolidated in a single, easily discoverable location.

## 2. Clear Definition of Documentation Types

Each type of documentation serves a specific purpose and has a distinct focus:

### Architectural Decision Records (ADRs) - `docs/adr/`

*   **Focus:** The *why* behind significant architectural or design decisions.
*   **Content:** Context, the decision made, rationale, and consequences.
*   **Lifecycle:** Created *before* or *during* the implementation of a major change. Once a decision is made, ADRs are largely immutable (their status can be updated, but content should not change).
*   **Interlinking:** Should be referenced in `CHANGELOG.md` entries when a feature or change directly implements an ADR. Can be mentioned in `DEV_TASKS.md` if a task is part of an ADR's implementation.

### Change Log - `docs/CHANGELOG.md`

*   **Focus:** The *what* was changed and when. A chronological history of project development (features, bug fixes, refactorings).
*   **Content:** Overview of changes, brief rationale, list of modified files.
*   **Lifecycle:** Updated *after* a feature or fix is completed. Each entry should represent a logical unit of work.
*   **Interlinking:** Should reference relevant ADRs if the change implements an architectural decision. Can refer to completed tasks from `DEV_TASKS.md`.

### Development Tasks - `docs/DEV_TASKS.md`

*   **Focus:** The *what* needs to be done next. A dynamic list of current and upcoming development tasks.
*   **Content:** Specific tasks, their current status (e.g., TODO, In Progress, Done), optional assignees.
*   **Lifecycle:** Constantly updated. Tasks are added, their status changes, and completed tasks are either archived or removed once documented in `CHANGELOG.md`.
*   **Interlinking:** Can refer to relevant ADRs if a task is directly related to implementing a specific architectural decision.

## 3. Interlinking Strategy

To maximize coherence, documents should reference each other:

*   **ADR -> CHANGELOG:** When a feature or change documented in `CHANGELOG.md` is based on an ADR, the `CHANGELOG.md` entry should explicitly reference the corresponding ADR (e.g., "Implemented LLM-powered semantic aggregation (see ADR-003)").
*   **DEV_TASKS -> ADR:** If a task in `DEV_TASKS.md` is directly related to the implementation of an ADR, a link to the ADR can be added in the task description.
*   **CHANGELOG -> DEV_TASKS:** When tasks from `DEV_TASKS.md` are completed and documented in `CHANGELOG.md`, they should be marked as "Done" in `DEV_TASKS.md` and subsequently archived or removed. The `CHANGELOG.md` entry could briefly mention which tasks it covers.

## 4. Workflow Integration for Developers

To ensure synchronized work, developers should follow this workflow:

1.  **Before starting a major feature or change:**
    *   **Check for ADR necessity:** Determine if the change warrants an ADR (e.g., new technology, significant architectural shift). If so, create it first and get alignment.
    *   **Add to `DEV_TASKS.md`:** Create a new task entry in `DEV_TASKS.md` for the work, linking to any relevant ADRs.

2.  **During development:**
    *   **Update `DEV_TASKS.md`:** Keep the status of your tasks in `DEV_TASKS.md` up-to-date (e.g., "In Progress").

3.  **Before marking a task as complete:**
    *   **Perform Testing:** Thoroughly test the implemented feature or fix according to the guidelines below. Ensure all expected behaviors are met and no regressions are introduced.

4.  **Upon completion and merging of work:**
    *   **Update `CHANGELOG.md`:** Add a new entry to `CHANGELOG.md` detailing the completed work.
        *   Clearly describe the feature, bug fix, or refactoring.
        *   List the key changes and rationale.
        *   **Crucially, reference any relevant ADRs** that guided this work.
        *   List all modified files.
    *   **Update `DEV_TASKS.md`:** Mark the corresponding task(s) in `DEV_TASKS.md` as "Done" and consider archiving or removing them if they are fully covered by the `CHANGELOG.md` entry.

## 5. Testing Guidelines

Testing is an integral part of our development process, ensuring the quality, reliability, and correctness of the `ama_b_viewer` application. Adhering to these guidelines helps maintain a high standard of code and user experience.

### General Principles

*   **Test Early, Test Often:** Integrate testing throughout the development lifecycle, not just at the end.
*   **Reproducibility:** Tests should be deterministic and produce the same results given the same inputs.
*   **Clear Scope:** Each test should have a clear purpose and focus on a specific piece of functionality.
*   **Automate When Possible:** Prioritize automated tests (unit, integration, end-to-end) to ensure rapid feedback and prevent regressions.
*   **Manual Testing for UX/Edge Cases:** Supplement automated tests with manual testing, especially for user experience, complex interactions, and hard-to-automate edge cases.

### Types of Testing

1.  **Unit Tests:**
    *   **Purpose:** Verify the correctness of individual functions, methods, or components in isolation.
    *   **Scope:** Smallest testable parts of the codebase.
    *   **Best Practice:** Aim for high code coverage. Mock external dependencies (e.g., database calls, API requests) to ensure tests are fast and isolated.

2.  **Integration Tests:**
    *   **Purpose:** Verify that different modules or services work together correctly.
    *   **Scope:** Interactions between components (e.g., Flask routes interacting with MongoDB, LLM mapper interacting with external APIs).
    *   **Best Practice:** Use real dependencies where feasible, or realistic mocks. Focus on the interfaces between components.

3.  **End-to-End (E2E) / UI Tests:**
    *   **Purpose:** Simulate real user scenarios to ensure the entire application flow works as expected from the user's perspective.
    *   **Scope:** Full application stack, including frontend and backend interactions.
    *   **Best Practice:** Use tools like Selenium or Playwright for web applications. Focus on critical user journeys. These tests are typically slower and more brittle, so use them judiciously.

4.  **Manual / Exploratory Testing:**
    *   **Purpose:** Discover bugs or usability issues that automated tests might miss. Essential for validating UI/UX and complex workflows.
    *   **Scope:** Any part of the application, often guided by a test plan but allowing for improvisation.
    *   **Best Practice:** Document test cases and expected outcomes. Pay attention to edge cases, error handling, and user feedback.

### Test Plan Documentation

For significant features or bug fixes, a concise test plan should be outlined, either directly in the `DEV_TASKS.md` description or referenced from it. This plan should include:

*   **Test Objectives:** What is being tested and why.
*   **Preconditions:** Any setup required before testing.
*   **Test Steps:** Clear, reproducible steps to execute the test.
*   **Expected Results:** What the application should do or display.
*   **Verification Steps:** How to confirm the test passed (e.g., checking database state, UI elements, logs).
*   **Edge Cases:** Specific scenarios to test (e.g., empty data, invalid input, concurrent operations).

By integrating these testing guidelines into our development workflow, we ensure that new features are robust, existing functionality remains stable, and the `ama_b_viewer` project continues to deliver a high-quality experience.