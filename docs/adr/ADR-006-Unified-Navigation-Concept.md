# ADR-006: Unified Navigation Concept

**Date:** 2025-08-01

**Status:** Proposed

## Context

The application currently has two distinct navigation patterns:
1.  A rich, tab-based navigation bar at the top for the main document views (`base.html`).
2.  Simple, standalone "Back to Home" links at the bottom of each dashboard page (`questions_dashboard.html`, `tags_dashboard.html`, etc.).

This inconsistency creates a disjointed user experience, makes the application harder to maintain (requiring edits in multiple files for navigation changes), and provides poor feedback to the user about their current location within the app's structure.

## Decision

We will refactor the application to use a **single, unified navigation concept** for all primary views, including dashboards.

This will be achieved by:
1.  **Integrating all primary navigation links** (including those to dashboards) into the central tab-based navigation bar located in `templates/base.html`.
2.  **Removing all local navigation elements** (e.g., "Back to Home" links) from individual dashboard pages.
3.  **Implementing a consistent mechanism** where the backend routes pass `page_title` and `active_page` context variables to the base template.
4.  **Using the `active_page` variable** in `base.html` to dynamically apply a `.active` CSS class to the corresponding navigation tab, providing clear visual feedback of the user's current location.

## Rationale

*   **Improved User Experience (UX):** Provides a consistent, predictable, and seamless navigation flow across the entire application. Users always know where they are and how to get to other sections.
*   **Enhanced Maintainability:** Centralizes navigation logic in a single file (`base.html`). Future changes or additions to the navigation only need to be made in one place, adhering to the DRY (Don't Repeat Yourself) principle.
*   **Clearer Structure:** Reinforces a clear and logical information architecture. Dashboards are treated as integral parts of the application, not as separate, disconnected pages.
*   **Adherence to Design Principles:** Aligns with the core principles of a modern, robust, and clearly structured application.

## Consequences

*   **Positive:**
    *   Significantly improved UI/UX consistency.
    *   Reduced code duplication and improved maintainability.
    *   A clear, scalable pattern for adding new views in the future.
*   **Negative:**
    *   Requires a one-time refactoring effort across several backend routes and frontend templates.
