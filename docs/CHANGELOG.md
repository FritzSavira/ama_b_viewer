# Development Log

## 2025-08-01 - Refactor: Unified Navigation and UI Consistency

### Overview
Implemented a unified navigation concept to create a consistent and seamless user experience across the entire application, as documented in `ADR-006`. This refactoring eliminates navigation dead ends and improves code maintainability.

### Key Changes & Rationale

1.  **Unified Tab Navigation (`base.html`):**
    *   The main tab-based navigation is now the single source of truth and is displayed on all pages, including dashboards.
    *   The navigation logic was decoupled from requiring a `doc` object, making it globally available.
    *   Removed hardcoded "Back to Home" links and redundant `<h1>` titles from all dashboard templates (`questions_dashboard.html`, `tags_dashboard.html`, `bible_theme_network.html`).

2.  **Active Page Highlighting:**
    *   Backend routes (`main.py`) now consistently pass a `page_title` and an `active_page` identifier to the base template.
    *   The `base.html` template uses the `active_page` variable to dynamically apply a `.active` class to the correct tab, providing clear visual feedback of the user's location.

3.  **Robust Navigation Logic:**
    *   **Fixed a critical bug** where navigating from a dashboard back to a document view was impossible.
    *   Dashboard routes now pass the `last_doc_id` to the template.
    *   The navigation links in `base.html` now intelligently use the current `doc._id` if available, or fall back to the `last_doc_id` when on a dashboard page, ensuring navigation is always possible.

4.  **Extended Test Coverage (`tests/test_ui_consistency.py`):**
    *   Added a new test suite to programmatically verify that the correct navigation tab is marked as active on each respective dashboard page, preventing future regressions.

### Files Modified
*   `main.py`
*   `templates/base.html`
*   `templates/questions_dashboard.html`
*   `templates/tags_dashboard.html`
*   `templates/bible_theme_network.html`
*   `docs/DEV_TASKS.md` (updated status)
*   `docs/adr/ADR-006-Unified-Navigation-Concept.md` (new)
*   `tests/test_ui_consistency.py` (new)

## 2025-08-01 - Refactor: Page Layout Adjustment

### Overview
Adjusted the position of the page title for a more logical and intuitive visual hierarchy on the document view page.

### Key Changes & Rationale

1.  **Frontend (`templates/base.html`):**
    *   The page title element (`<h2>{{ page_title }}</h2>`) was moved from the top of the body to a position below the main navigation buttons and the tab navigation bar.
    *   This change ensures that the primary navigation controls remain consistently at the top, with the title for the specific content appearing directly above that content.

### Files Modified
*   `templates/base.html`
*   `docs/DEV_TASKS.md` (updated status)

## 2025-08-01 - Feature: Robust Navigation & Test Framework Setup

### Overview
This update introduces two major improvements: it prevents users from navigating into dead ends and establishes a foundational automated testing framework to ensure future code quality.

### Key Changes & Rationale

1.  **Feature: Prevent Navigation Dead Ends:**
    *   **Backend (`main.py`):** The `view_document` route now detects if the user is on the first or last document and passes boolean flags (`is_on_first_document`, `is_on_last_document`) to the template.
    *   **Frontend (`templates/base.html`):**
        *   Added a `.disabled` CSS class to visually grey out and disable pointer events for navigation buttons.
        *   Used Jinja2 logic to conditionally apply the `disabled` class and set `href="#"` for the `[First]`/`[Previous]` or `[Next]`/`[Last]` buttons, preventing navigation to error pages.
        *   The keyboard shortcut script now checks for the `.disabled` class and will not trigger actions for disabled buttons.

2.  **Feature: Automated Testing Framework (`pytest`):**
    *   **Dependencies (`requirements.txt`):** Added `pytest`, `pytest-flask`, `beautifulsoup4`, and pinned `Werkzeug<3.0` to ensure compatibility with Flask 2.x.
    *   **Configuration (`pytest.ini`, `tests/conftest.py`):**
        *   Created `pytest.ini` to add the project root to the `pythonpath`, fixing module import errors during testing.
        *   Created `tests/conftest.py` to define reusable test fixtures (`app`, `client`) for the Flask application.
    *   **Initial Tests (`tests/test_navigation.py`):**
        *   Wrote two automated tests that verify the navigation buttons are correctly disabled on the first and last documents.
        *   These tests serve as a blueprint for future test development.

### Files Modified
*   `main.py`
*   `templates/base.html`
*   `requirements.txt`
*   `docs/DEV_TASKS.md` (updated status)
*   `tests/test_navigation.py` (new)
*   `tests/conftest.py` (new)
*   `pytest.ini` (new)

## 2025-08-01 - Feature: Keyboard Shortcuts for Navigation

### Overview
Implemented keyboard shortcuts to enhance user experience and navigation efficiency. Users can now use keyboard keys to navigate between documents and trigger actions.

### Key Changes & Rationale

1.  **Frontend (`templates/base.html`):**
    *   Added unique IDs (`first-button`, `previous-button`, `next-button`, `last-button`) to all navigation buttons for robust selection via JavaScript.
    *   Implemented a JavaScript event listener for `keydown` events.
    *   Mapped the following keys to actions:
        *   `ArrowLeft`: Clicks the [Previous] button.
        *   `ArrowRight`: Clicks the [Next] button.
        *   `Home`: Clicks the [First] button.
        *   `End`: Clicks the [Last] button.
        *   `Delete`: Clicks the [Delete] button.
    *   Added `event.preventDefault()` to stop default browser actions (like scrolling or history navigation).
    *   The script is disabled when a user is typing in an input field or textarea.

### Files Modified
*   `templates/base.html`
*   `docs/DEV_TASKS.md` (updated status)

## 2025-08-01 - Feature: Default View on Startup

### Overview
Changed the application's startup behavior to directly display the "Answer" view of the most recent document, streamlining the user's entry into the application.

### Key Changes & Rationale

1.  **Backend (`main.py`):**
    *   Modified the `index()` route (`@app.route('/')`).
    *   Instead of redirecting to the first document, it now finds the last document in the collection (sorted by `_id` descending).
    *   It then redirects to the `view_document` endpoint for that document, explicitly setting `show='answer'`.
    *   Includes a fallback to handle cases where the collection is empty.

### Files Modified
*   `main.py`

## 2025-08-01 - Feature: Document Deletion Functionality

### Overview
Implemented the ability to delete individual documents from the MongoDB Atlas collection directly from the UI, enhancing data management capabilities.

### Key Changes & Rationale

1.  **Backend (`main.py`):**
    *   Added a new POST endpoint `/delete/<id>` to handle document deletion requests.
    *   Implemented logic to delete the document by its `_id`.
    *   After successful deletion, the user is redirected to the next available document (if any), or to the previous document, or to the home page if no other documents exist.
    *   Includes basic error handling for deletion failures.

2.  **Frontend (`templates/base.html`):**
    *   Added a `[Delete]` button to the document navigation bar.
    *   Implemented client-side JavaScript with a confirmation dialog to prevent accidental deletions.
    *   The JavaScript sends a POST request to the backend endpoint and handles redirection based on the backend's response.

### Files Modified
*   `main.py`
*   `templates/base.html`
*   `docs/adr/ADR-005-Document-Deletion-Functionality.md` (referenced)
*   `docs/DEV_TASKS.md` (updated status)

## 2025-07-31 - Feature: LLM-Powered Semantic Aggregation

### Overview
Implemented a robust LLM-powered system to automatically normalize varying categorical terms (tags, categories) into consistent, canonical forms. This significantly improves data quality and consistency in visualizations.

### Key Changes & Rationale

1.  **Backend (`main.py`, `llm_mapper.py`):**
    *   Introduced new API endpoints: `/api/trigger_llm_mapping` (POST) to initiate the process and `/api/llm_mapping_status` (GET) to monitor its progress.
    *   The mapping process now runs in a background thread, ensuring the UI remains responsive.
    *   `llm_mapper.py` was enhanced to process terms in batches, significantly improving reliability and preventing timeouts for large datasets.
    *   The LLM prompt was refined to include existing canonical terms, guiding the LLM towards higher consistency and ensuring canonical terms are generated in German.
    *   Robust error handling and status reporting were implemented to provide clear feedback on the process state.
    *   A dedicated `category_mappings` MongoDB collection stores the `original_term` to `canonical_term` mappings.

2.  **Frontend (`tags_dashboard.html`):**
    *   Added a "Update Tag Mappings" button to the Tags Dashboard.
    *   Implemented JavaScript logic to trigger the backend process, poll its status, and display real-time progress and messages (including success/error states) to the user.

### Files Modified
*   `main.py`
*   `llm_mapper.py`
*   `tags_dashboard.html`
*   `docs/DEV_TASKS.md` (updated status)
*   `docs/adr/ADR-003-LLM-Powered-Semantic-Aggregation.md` (updated status)

## 2025-07-28 - Refactor: Menu Order and Question View Removal

### Overview
Reordered the main navigation tabs for improved user flow and removed the redundant "Question" view, streamlining the interface.

### Key Changes & Rationale

1.  **Frontend (`templates/base.html`):**
    *   The order of navigation tabs was changed to: "Question Abstraction", "Answer", "Tags", "All".
    *   The "Question" tab was removed from the navigation.

2.  **Backend (`main.py`):**
    *   Added logic to the `view_document` function to handle requests for the deprecated "Question" view. If `show='question'` is received, it now gracefully redirects to the "All" view to prevent errors and ensure a smooth user experience.

### Files Modified
*   `main.py`
*   `templates/base.html`

## 2025-07-28 - Feature: Enhanced Tags View

### Overview
Redesigned the `[Tags]` view to display categorized tags in a visually appealing and structured format, improving readability and user experience. Categories with no tags are now automatically hidden.

### Key Changes & Rationale

1.  **Backend (`main.py`):**
    *   Introduced `get_categorized_tags(doc)` function to extract and organize tags into predefined categories.
    *   This function now dynamically filters out categories that contain no tags for a given document, ensuring a cleaner display.
    *   The `categorized_tags` data is passed to the template context.

2.  **Frontend (`templates/index.html`):**
    *   The `[Tags]` view block was refactored to iterate over the `categorized_tags` and render each category with its respective tags.
    *   Tags are displayed as visually distinct "pills" within each category section.

3.  **Styling (`templates/base.html`):**
    *   Added new CSS classes (`.tag-categories-container`, `.tag-category-section`, `.tag-list`, `.tag-pill`) to `base.html`.
    *   These styles provide a clean, two-column layout for categories (where space allows) and a clear, subtle design for individual tag pills, aligning with the established UI/UX.

### Files Modified
*   `main.py`
*   `templates/index.html`
*   `templates/base.html`

## 2025-07-28 - Feature: Dynamic Page Title

### Overview
Changed the page title displayed on each document view from the generic Document ID to a more descriptive "Fragestellung: [Information Goal]" from the `question_abstraction` field. This enhances user context and navigation.

### Key Changes & Rationale

1.  **`main.py` Modifications:**
    *   The `view_document` function now safely attempts to extract `doc.question_abstraction.semantic.information_goal`.
    *   If found, the `page_title` is set to "Question: " followed by the information goal. Otherwise, it defaults back to "Document ID: [ID]".
    *   This `page_title` is passed to the template context.

2.  **`templates/base.html` Modifications:**
    *   The `<h1>` tag was updated to display the `page_title` variable, ensuring the dynamic title is rendered.

### Files Modified
*   `main.py`
*   `templates/base.html`

## 2025-07-28 - Feature: Render Markdown in Answer View

### Overview
Implemented Markdown rendering for the "Answer" view to display formatted text instead of raw source. This provides a more readable and user-friendly experience, consistent with the rest of the application's UI/UX.

### Key Changes & Rationale

1.  **Dependency Management (`requirements.txt`):**
    *   Added the `Markdown` library to `requirements.txt` to formally include it as a project dependency.

2.  **Backend Refactoring (`main.py`):**
    *   The `get_answer_content` helper function was updated to use the `markdown` library. It now converts the Markdown text from the database into an HTML string before passing it to the template. This follows the "Separation of Concerns" principle, keeping data processing in the backend.

3.  **Frontend Template Update (`index.html`):**
    *   The "Answer" view block now uses a `<div>` and the `|safe` Jinja2 filter (`{{ answer_content | safe }}`). This ensures the pre-formatted HTML from the backend is rendered correctly instead of being escaped.

4.  **Centralized Styling (`base.html`):**
    *   Added a `.rendered-markdown` CSS class with styles for common HTML elements (headings, lists, code blocks). This ensures that any Markdown content rendered across the application will have a consistent and polished look, improving the overall UI/UX.

### Files Modified
*   `requirements.txt`
*   `main.py`
*   `templates/index.html`
*   `templates/base.html`

## 2025-07-28 - Fix: Prevent Server Shutdown Error on Windows

### Overview
Fixed a `[WinError 10038]` crash that occurred when stopping the Flask development server on Windows. This error is caused by a race condition in the server's auto-reloader.

### Key Changes & Rationale

1.  **`main.py` Modifications:**
    *   The `app.run()` call was modified to `app.run(debug=True, use_reloader=False)`.
    *   **Reasoning:** Disabling the auto-reloader (`use_reloader=False`) is the most direct way to prevent the race condition that leads to the socket error on shutdown. While this requires manual server restarts during development, it provides a stable and error-free exit, which is preferable to the confusing crash log.

### Files Modified
*   `main.py`

## 2025-07-28 - Refactor: Improved Answer View Logic

### Overview
Refactored the logic for the "Answer" view to robustly display content from a deeply nested field (`reply.completion.choices[0].message.content`). This change improves code quality and prevents potential runtime errors if the data structure varies.

### Key Changes & Rationale

1.  **`main.py` Modifications (Good Practice):**
    *   **Helper Function:** Introduced a new helper function, `get_answer_content(doc)`, to encapsulate the logic for safely accessing the nested answer field.
    *   **Robust Error Handling:** The function uses a `try...except` block to gracefully handle `KeyError`, `IndexError`, or `TypeError` if the expected path does not exist in the document, returning a user-friendly message instead of crashing.
    *   **Separation of Concerns:** The main route `view_document` is now cleaner, as it delegates the complex data extraction to the helper function, improving readability and maintainability.

2.  **`templates/index.html` Simplification:**
    *   The template logic for the "Answer" view was simplified to directly render the `answer_content` variable passed from the backend.
    *   This removes complex data access logic from the template, adhering to the principle of keeping templates focused on presentation.

### Files Modified
*   `main.py`
*   `templates/index.html`

## 2025-07-28 - Feature: "First" and "Last" Navigation Buttons

### Overview
Added "First" and "Last" buttons to the document navigation, allowing users to jump directly to the first and last documents in the MongoDB collection. This improves navigation efficiency, especially in large datasets.

### Key Changes & Rationale

1.  **`main.py` Modifications:**
    *   The `view_document` function was updated to retrieve the `_id` of the first and last documents from the collection.
    *   These IDs (`first_doc_id`, `last_doc_id`) are now passed to the template context, making them available for the navigation links.

2.  **`templates/base.html` Modifications:**
    *   Added "First" and "Last" buttons to the navigation bar.
    *   The buttons are logically arranged as `[First] [Previous] [Next] [Last]` for an intuitive user experience.
    *   The links correctly use the `first_doc_id` and `last_doc_id` passed from the backend.

### Files Modified
*   `main.py`
*   `templates/base.html`

## 2025-07-28 - Feature: Filtered Data Views (VIEW-01)

### Overview
Implemented filtered data views for the MongoDB document viewer as per `FEATURE_VIEWS.md` specification. This includes "All", "Question", "Answer", "Tags", and "Question Abstraction" views. The frontend now uses a base template for consistent styling and structure.

### Key Changes & Rationale

1.  **`main.py` Modifications:**
    *   **Flask App Initialization:** Moved `app = Flask(__name__)` to an earlier point for better structure.
    *   **`show` URL Parameter:** Modified `@app.route('/')` and `@app.route('/view/<id>')` to accept an optional `show` query parameter, defaulting to `'all'`. This parameter is propagated through "Previous" and "Next" navigation links.
    *   **`ObjectId` JSON Serialization:** Added a custom Jinja2 filter `tojson` with a `CustomEncoder` to handle `bson.ObjectId` serialization to string, resolving `TypeError: Object of type ObjectId is not JSON serializable`. This ensures all document data can be rendered as JSON in templates.
    *   **Conditional Template Rendering:** Updated `view_document` function to render different templates (`index.html` or `question_abstraction_view.html`) based on the `show` parameter, promoting modularity and separation of concerns for different view types.

2.  **Frontend Template Refactoring (`templates/` directory):**
    *   **`base.html` Creation:** Introduced `base.html` to serve as a base template for all views. It contains common HTML structure, CSS styles, and the main navigation (Previous/Next buttons and tab navigation). This ensures a consistent look and feel across different views and simplifies future UI modifications.
    *   **`index.html` Adaptation:** Modified `index.html` to extend `base.html` and now only contains the specific content block for "All", "Question", "Answer", and "Tags" views.
    *   **`question_abstraction_view.html` Creation:** Created a new template file specifically for the "Question Abstraction" view. This template also extends `base.html` and implements the detailed, structured display of the `question_abstraction` field using `dl`, `dt`, `dd`, and `ul` elements, along with dedicated CSS for better readability.

### Files Modified
*   `main.py`
*   `templates/index.html` (modified)
*   `templates/base.html` (new)
*   `templates/question_abstraction_view.html` (new)

### Outstanding Issues / Next Steps
*   **Error Handling:** Enhance error handling for cases where sub-fields within `question_abstraction` might be missing or have unexpected types. Currently, `default('N/A')` is used, which is basic.
*   **Styling Refinement:** The current CSS is basic. Further styling could be applied for a more polished look, especially for the `question_abstraction` view.
*   **Test Coverage:** Add unit/integration tests for the new routes and template rendering logic to ensure stability and prevent regressions.
*   **Data Validation:** Consider adding data validation on the backend for incoming `show` parameters to prevent invalid view requests.
*   **Performance Optimization:** For very large documents, consider lazy loading or pagination within the views, though not critical for current scope.