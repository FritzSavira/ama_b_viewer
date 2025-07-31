---
project: "ama_b_viewer"
title: "Development Task List: Analysis and Visualization"
version: 1.0.0
last_updated: "2025-07-30"
---

# Development Task List

This document tracks the development tasks for the `ama_b_viewer` project.

## Phase 1: Backend - Data Preparation (Completed)

- [x] **TASK-1.1:** MongoDB Aggregation for "Question Categorization and Intent"
  - **description:** Aggregation pipelines to determine the distribution of question metadata.
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [x] **TASK-1.2:** Flask API Endpoint for "Question Categorization and Intent"
  - **description:** API endpoint (`/api/questions_categorization`) to provide the data from TASK-1.1.
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [x] **TASK-1.3:** MongoDB Aggregation for "Tag Analysis"
  - **description:** Aggregation pipelines to determine the frequency of tags.
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [x] **TASK-1.4:** Flask API Endpoint for "Tag Analysis"
  - **description:** API endpoint (`/api/tag_frequency`) to provide the data from TASK-1.3.
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [x] **TASK-1.5:** MongoDB Aggregation for "Relationship Network" (Co-occurrence)
  - **description:** Aggregation to determine the co-occurrence of biblical references and main themes for caching.
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [x] **TASK-1.6:** Implement Caching Mechanism for Network Data
  - **description:** Function to save the network data into a cache collection (`ama_log_network_cache`).
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [x] **TASK-1.7:** Flask API Endpoint for "Relationship Network"
  - **description:** API endpoint (`/api/bible_theme_network`) to provide the cached network data.
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

## Phase 2: Frontend - Visualization (Completed)

- [x] **TASK-2.1:** Frontend Page and Visualization for "Question Categorization"
  - **description:** Creation of `questions_dashboard.html` and implementation of Chart.js diagrams.
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [x] **TASK-2.2:** Frontend Page and Visualization for "Tag Analysis"
  - **description:** Creation of `tags_dashboard.html` and implementation of tag clouds/bar charts.
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [x] **TASK-2.3:** Frontend Page and Visualization for "Relationship Network"
  - **description:** Creation of `bible_theme_network.html` and implementation of the D3.js Force-Directed Graph.
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

## Phase 3: Integration & Refinement

- [x] **TASK-3.1:** Integrate Visualizations into the UI
  - **description:** Add navigation links to the new dashboard pages.
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [x] **TASK-3.2:** Implement Error Handling and Loading States
  - **description:** Add robust error handling for API calls and loading indicators in the frontend.
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [ ] **TASK-3.3:** Performance Optimization
  - **description:** Review and optimize aggregation pipelines and frontend rendering performance.
  - **status:** pending
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [ ] **TASK-3.4:** Technical Documentation
  - **description:** Create technical documentation for backend endpoints and frontend components.
  - **status:** pending
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

## Phase 4: LLM-Powered Semantic Aggregation

- [x] **TASK-4.1:** Setup Environment and Infrastructure
  - **description:** Ensure `aio_straico` is in `requirements.txt` and `llm_mapper.py` exists. Verify MongoDB connection and collections.
  - **status:** completed
  - **reference:** `docs/adr/ADR-003-LLM-Powered-Semantic-Aggregation.md`

- [x] **TASK-4.2:** Implement Logic to Find Unmapped Terms
  - **description:** In `llm_mapper.py`, implement a function that gets all unique terms from the relevant fields in `ama_log` and compares them against the `_id`s in `category_mappings` to produce a list of new, unmapped terms.
  - **status:** completed
  - **reference:** `docs/adr/ADR-003-LLM-Powered-Semantic-Aggregation.md`

- [x] **TASK-4.3:** Implement LLM Prompting and API Call
  - **description:** In `llm_mapper.py`, create a function that takes the list of new terms, constructs a prompt asking the LLM to return a JSON object mapping each term to a canonical form, and calls the `straico_client` API with the model `anthropic/claude-3.5-sonnet`.
  - **status:** completed
  - **reference:** `docs/adr/ADR-003-LLM-Powered-Semantic-Aggregation.md`

- [x] **TASK-4.4:** Implement LLM Response Processing and DB Update
  - **description:** In `llm_mapper.py`, implement a function that parses the JSON response from the LLM. For each `original_term: canonical_term` pair, it should perform an `update_one` with `upsert=True` on the `category_mappings` collection.
  - **status:** completed
  - **reference:** `docs/adr/ADR-003-LLM-Powered-Semantic-Aggregation.md`

- [x] **TASK-4.5:** Refactor Aggregation Pipelines to Use Mappings
  - **description:** Modified the aggregation pipelines in the API endpoints (`/api/questions_categorization`, `/api/tag_frequency`) to use `$lookup` on the `category_mappings` collection and normalize the data before counting.
  - **status:** completed
  - **reference:** `docs/adr/ADR-003-LLM-Powered-Semantic-Aggregation.md`

- [x] **TASK-4.8-BE:** Implement Backend for Manual LLM Mapping Trigger
  - **description:** In `main.py`, create a `/api/trigger_llm_mapping` endpoint that imports and runs the mapping logic from `llm_mapper.py` in a background thread. Also create a `/api/llm_mapping_status` endpoint for the frontend to poll. Implement a locking mechanism to prevent concurrent runs.
  - **status:** completed
  - **reference:** `docs/adr/ADR-003-LLM-Powered-Semantic-Aggregation.md`

- [x] **TASK-4.8-FE:** Implement Frontend for Manual LLM Mapping Trigger
  - **description:** Add a button to a dashboard (e.g., `tags_dashboard.html`). Implement JavaScript to call the trigger endpoint, poll the status endpoint, and provide visual feedback to the user (e.g., loading indicators, success/error messages).
  - **status:** completed
  - **reference:** `docs/adr/ADR-003-LLM-Powered-Semantic-Aggregation.md`

- [x] **TASK-4.9:** Final Testing and Refinement
  - **description:** Thoroughly test the end-to-end mapping process. Refine error handling and user feedback.
  - **status:** completed
  - **reference:** `docs/adr/ADR-003-LLM-Powered-Semantic-Aggregation.md`

- [x] **TASK-4.7:** Create New ADR for this Feature
  - **description:** Document the problem, the chosen LLM-based solution, and the implementation details in a new file: `docs/adr/ADR-003-LLM-Powered-Semantic-Aggregation.md`.
  - **status:** completed
  - **reference:** `(self)`

## Phase 4: Semantic Category Aggregation

- [ ] **TASK-4.1:** Create MongoDB Infrastructure for Mappings
  - **description:** Set up a new, dedicated collection named `category_mappings` to store the normalization rules.
  - **status:** pending
  - **reference:** `docs/adr/ADR-003-Semantic-Category-Aggregation.md`

- [ ] **TASK-4.2:** Implement Analysis Script for Category Values
  - **description:** Create a script to extract all unique values and their frequencies for the relevant fields (`category`, `subcategory`, `type`, `domain`, `hauptthemen`, `theologische_konzepte`).
  - **status:** pending
  - **reference:** `docs/adr/ADR-003-Semantic-Category-Aggregation.md`

- [ ] **TASK-4.3:** Define and Populate Initial Mapping Rules
  - **description:** Based on the analysis from TASK-4.2, define the initial set of mapping rules and populate them into the `category_mappings` collection.
  - **status:** pending
  - **reference:** `docs/adr/ADR-003-Semantic-Category-Aggregation.md`

- [ ] **TASK-4.4:** Refactor Aggregation Pipelines to Use Mappings
  - **description:** Modify the aggregation pipelines in the API endpoints (`/api/questions_categorization`, `/api/tag_frequency`) to use `$lookup` on the `category_mappings` collection and normalize the data before counting.
  - **status:** pending
  - **reference:** `docs/adr/ADR-003-Semantic-Category-Aggregation.md`

- [ ] **TASK-4.5:** Create a New ADR for this Feature
  - **description:** Document the problem, the chosen solution (MongoDB collection + `$lookup`), and the implementation details in a new file: `docs/adr/ADR-003-Semantic-Category-Aggregation.md`.
  - **status:** pending
  - **reference:** `(self)`
