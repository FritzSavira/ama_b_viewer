# ADR-003: LLM-Powered Semantic Aggregation

**Status:** Accepted and Implemented
**Date:** 2025-07-30

## 1. Context

The `ama_log` collection contains various categorical fields (e.g., `subcategory`, `hauptthemen`) where semantically similar terms are represented by different spellings or variations (e.g., "Bibelexegese", "Biblische Exegese", "Bibelauslegung"). This leads to fragmented data in visualizations, making analysis difficult and misleading. Manually maintaining a comprehensive mapping for all variations is labor-intensive and not scalable as new terms emerge.

## 2. Decision

We will implement an LLM-powered semantic aggregation system to automatically normalize these varying terms into a single, canonical representation for visualization purposes. This system will involve:

1.  **A dedicated MongoDB `category_mappings` collection:** To store the `original_term` to `canonical_term` mappings, along with the `field` they apply to.
2.  **An `llm_mapper.py` script:** This script will:
    *   Identify new, unmapped terms from the `ama_log` collection.
    *   Send these terms to an LLM (Anthropic Claude 3.5 Sonnet via `aio_straico`) with a prompt to generate canonical mappings in JSON format.
    *   Persist these LLM-generated mappings into the `category_mappings` collection.
3.  **Modification of Flask API aggregation pipelines:** The existing MongoDB aggregation pipelines (`/api/questions_categorization`, `/api/tag_frequency`) will be updated to use a `$lookup` stage with the `category_mappings` collection. This will replace original terms with their canonical forms before final grouping and counting.

This process will be triggered periodically (e.g., via a cron job) to keep mappings up-to-date, and a manual trigger will be provided in the UI.

## 3. Consequences

### Positive
*   **Improved Data Quality in Visualizations:** Dashboards will display consolidated, accurate counts for semantically identical categories.
*   **Reduced Manual Effort:** Automates the process of identifying and mapping new term variations.
*   **Scalability:** The system can handle new term variations without requiring manual intervention for each one.
*   **Flexibility:** Mappings are stored in MongoDB, allowing for easy review, modification, or deletion if the LLM makes an incorrect mapping.
*   **Original Data Integrity:** The `ama_log` collection remains unchanged; normalization only occurs during aggregation for visualization.

### Negative
*   **LLM Dependency & Cost:** Relies on an external LLM service, incurring API costs and potential latency.
*   **LLM Accuracy:** The quality of mappings depends on the LLM's performance. Manual review of generated mappings might still be necessary, especially initially.
*   **Increased Backend Complexity:** Adds new components (`llm_mapper.py`, `category_mappings` collection) and modifies existing aggregation pipelines.

## 4. Alternatives Considered

*   **Manual Mapping in Code:** Rejected due to high maintenance effort and lack of scalability.
*   **Fuzzy Matching Algorithms (e.g., Levenshtein Distance):** Rejected due to potential for incorrect groupings and lack of semantic understanding, leading to less accurate normalization than an LLM.
*   **Direct Modification of `ama_log`:** Rejected to preserve original data integrity and avoid complex rollback scenarios if mappings need to be changed.
