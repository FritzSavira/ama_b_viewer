# ADR-001: Filtered Data Views

**Author:** Gemini  
**Date:** 2025-07-27  
**Status:** Implemented  
**Ticket:** VIEW-01

---

## 1. Summary

This document describes the implementation of filtered views in the MongoDB data viewer. The goal is to allow users to reduce the displayed dataset to specific, relevant sections to improve analysis and readability.

## 2. User Story

**As a** user analyzing MongoDB records,  
**I want to** be able to switch between a full data view and filtered views for "Question", "Answer", and "Tags",  
**so that I** can quickly focus on specific parts of a record without being distracted by irrelevant data.

## 3. Acceptance Criteria

- **AC-1: Tab Navigation:** A navigation bar with tabs for "All", "Question", "Answer", and "Tags" is visible in the frontend.
- **AC-2: Default View:** The "All" view is active by default on page load and displays the complete, nested document.
- **AC-3: "Question" View:** The "Question" view displays only the content of the `question` object. If it is not present, a corresponding message is shown.
- **AC-4: "Answer" View:** The "Answer" view displays only the content of the `answer` object. If it is not present, a corresponding message is shown.
- **AC-5: "Tags" View:** The "Tags" view extracts and displays a consolidated list of values from all fields that are lists/arrays (e.g., `tags`, `hauptthemen`, `bibelreferenzen`).
- **AC-6: Active State:** The currently selected tab is visually highlighted.
- **AC-7: Persistent Navigation:** The "Previous" and "Next" buttons maintain the currently selected view.

## 4. Technical Implementation Plan

The implementation is done without client-side JavaScript. The logic is handled server-side in Flask/Jinja2.

### 4.1. Backend (`main.py`)

#### Task 4.1.1: Adapt Routes

- The routes `@app.route('/')` and `@app.route('/view/<id>')` must accept an optional URL query parameter `show` (e.g., `/view/some_id?show=question`).
- The default value for `show` is `'all'`.
- The `show` parameter is passed to the `render_template()` function.

#### Task 4.1.2: Extend Navigation Logic

- The `get_previous(id)` and `get_next(id)` functions must read the `show` parameter from `request.args`.
- The `show` parameter must be passed in the `redirect(url_for(...))` calls to preserve the view state during navigation.

### 4.2. Frontend (`templates/index.html`)

#### Task 4.2.1: Implement Tab Navigation

- An HTML structure (e.g., `<nav>`) for the tabs is added.
- Each link points to the URL of the current document, appended with the appropriate `show` parameter.
  ```jinja
  <a href="{{ url_for('view_document', id=doc['_id'], show='question') }}">Question</a>
  ```

#### Task 4.2.2: Create CSS for Tabs

- The navigation tabs are styled with CSS.
- An `.active` class is defined to highlight the active tab. The `show` parameter is used to set this class dynamically.
  ```jinja
  <a href="..." class="{{ 'active' if show == 'question' else '' }}">Question</a>
  ```

#### Task 4.2.3: Conditional Rendering of Views

- The main display area is controlled by an `if/elif/else` block in Jinja2.
- `{% if show == 'all' %}`: Renders the existing recursive macro display.
- `{% elif show == 'question' %}`: Accesses `doc.question` and renders its content or a "Not Found" message.
- `{% elif show == 'answer' %}`: Accesses `doc.answer` and renders its content or a "Not Found" message.
- `{% elif show == 'tags' %}`: Implements a loop that iterates through the `doc` object, finds all list fields, and displays their contents.

## 5. Development Workflow & Traceability

To ensure the development process is transparent and traceable for all team members, the following conventions will be adhered to for this feature.

### 5.1. Status Tracking

The `Status` field in the header of this document will be kept up-to-date to reflect the overall progress of the feature. The possible states are:

- **Proposed:** The plan is defined, but implementation has not yet started.
- **In Progress:** Active development is underway.
- **Completed:** All acceptance criteria have been met and the feature is fully implemented.
- **Blocked:** Development is paused due to an external dependency or issue.

### 5.2. Commit Messages

All commits related to this feature will follow the **Conventional Commits** specification. This provides a clear and descriptive commit history. Each commit message will be linked to this feature specification via its Ticket ID (`VIEW-01`).

**Format:**
```
<type>(<scope>): <subject> (VIEW-01)
```

- **`<type>`:** Describes the kind of change (e.g., `feat` for a new feature, `fix` for a bug fix, `docs` for documentation).
- **`<scope>`:** Describes the part of the codebase affected (e.g., `backend`, `frontend`, `docs`).
- **`<subject>`:** A short, imperative-tense description of the change.

**Example:**
```
feat(backend): Add 'show' URL parameter to view routes (VIEW-01)
```