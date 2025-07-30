# Contributing to ama_b_viewer

Thank you for your interest in contributing to this project! Any help is welcome. To ensure smooth collaboration, we ask you to adhere to the following guidelines.

## Development Workflow

1.  **Fork & Branch**: Fork the repository and create a new branch for your feature or bug fix.
2.  **Implementation**: Make your changes, adhering to the existing code style.
3.  **Documentation**: If you make a significant change (e.g., adding a new feature or changing the architecture), please create a new **Architectural Decision Record (ADR)** in the `docs/adr/` directory.
4.  **Commits**: Write meaningful commit messages that follow our convention (see below).
5.  **Pull Request**: Create a pull request against the `main` branch of the main repository.

## Commit Message Convention

All commits in this project must follow the **Conventional Commits** specification. This ensures a clear and traceable Git history. Any commit related to a documented feature or task should include a ticket ID.

**Format:**
```
<type>(<scope>): <subject> (<ticket-id>)
```

*   **`<type>`:** Describes the type of change (e.g., `feat` for a new feature, `fix` for a bug fix, `docs` for documentation, `refactor` for code refactoring).
*   **`<scope>`:** Describes the part of the codebase affected (e.g., `backend`, `frontend`, `docs`, `db`).
*   **`<subject>`:** A short, concise description of the change in the present tense.
*   **`<ticket-id>`:** (Optional) A reference to an ADR (e.g., `ADR-001`) or a task ID (e.g., `TASK-3.2`).

**Example:**
```
feat(backend): Add 'show' URL parameter to view routes (ADR-001)
```