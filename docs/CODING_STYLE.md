# Coding Style and Clean Code Principles

This document defines the binding code quality and style guidelines for this project. All code changes, especially those made by AI agents, MUST strictly follow these rules.

## 1. Language

- **Rule:** All code, comments, and docstrings MUST be written in **English**. This ensures international comprehensibility and consistency with most libraries.

## 2. Formatting

- **Rule:** All Python code MUST be formatted with the `black` formatter.
- **Instruction:** Run `black .` before each commit to ensure formatting. Code that is not `black`-compliant will not be accepted.

## 3. Linter / Static Analysis

- **Rule:** The code MUST pass the `ruff` linter check without errors.
- **Instruction:** Run `ruff check .` to check the code. Fix all reported errors before marking the task as complete.

## 4. Naming Conventions

- **Rule:** Names MUST be meaningful and unambiguous. They should clearly communicate their purpose.
- **Instruction:**
  - **Variables & functions:** snake_case (e.g., user_list, calculate_total_price).
  - **Classes:** PascalCase (e.g., DatabaseConnection, UserConfiguration).
  - **Constants:** `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`).
- **Examples:**
  - **BAD:** `ul`, `data`, `proc()`, `temp`
  - **GOOD:** `user_list`, `customer_data`, `process_payment()`, `temperature_in_celsius`

## 5. Functions and methods

- **Rule 1 (Single Responsibility Principle):** Each function/method SHOULD perform only one clearly defined task.
- **Rule 2 (Length):** Functions SHOULD be short, ideally less than 20 lines. Long functions must be split up.
- **Rule 3 (Arguments):** AVOID functions with more than 3 arguments. If more data is needed, combine it into a data object or class.

## 6. Comments

- **Rule:** Write code that is self-explanatory. AVOID comments that explain *what* the code does. The code should express this itself.
- **Instruction:** Only use comments to explain *why* a particular (complex or unusual) design decision was made.
  - **BAD:** `i = i + 1 # Increment i`
  - **GOOD:** `# We must use a direct API call here because the library's cache has a bug (see Ticket-123)`

## 7. DRY (Don't Repeat Yourself)

- **Rule:** Strictly AVOID code duplication.
- **Guidance:** If you find identical or very similar code in multiple places, abstract it into a reusable function or class.

## 8. The Boy Scout Rule

- **Rule:** When you edit a file, leave it in better condition than you found it.
- **Instruction:** Correct minor style errors, improve the readability of a name, or add a missing type annotation, even if it is not directly part of the main task.

## 9. Error Handling

- **Rule:** Use exceptions for error handling. AVOID returning error codes or `None` to signal an error condition.
- **Instruction:** Use `try...except` blocks and specific exception types.

## 10. Context-Aware Refactoring

**Problem:** Changes to a function, class, or variable can lead to errors (broken references) in other parts of the code.

**Rule:** To prevent this, the following workflow MUST be strictly adhered to for every change to existing code:

**Phase 1: Analysis**
1.  **Identification:** Identify the exact name of the element to be changed (e.g., function `get_user_data`, class `SessionManager`).
2.  **Global search:** Perform a project-wide search for all occurrences of this name.
- **Instruction:** Use the `search_file_content` tool to find all references. Example: `search_file_content(pattern=‘get_user_data’)`.
3.  **Analysis of references:** Analyze EVERY search result. Create a checklist of all files and code locations affected by the change (e.g., function calls that need to be adjusted, class instantiations, etc.).

**Phase 2: Implementation**
1.  **Atomic change:** Implement the planned change to the definition AND to all usage locations identified in the analysis phase.
2.  **Verification:** After implementation, run the entire test suite (e.g., with `pytest`) to ensure that the changes had no side effects and that all tests continue to be successful.

