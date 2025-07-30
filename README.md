# AMA-B Viewer

## 1. Overview

The **AMA-B Viewer** is a web-based application for analyzing and visualizing data from the `ama_log` MongoDB collection. It provides a **Data Viewer** for browsing individual documents and a suite of **Visualization Dashboards** for aggregated insights into question types, tag frequencies, and semantic relationships.

The primary goal is to offer developers and analysts a clear window into the application's usage patterns, content quality, and the nature of user inquiries.

## 2. Features

*   **Document Viewer**: Navigate documents with filtered views for raw JSON, Question Abstraction, formatted Answers, and categorized Tags.
*   **Visualization Dashboards**: Interactive charts and graphs for question analysis, tag frequency, and a network graph visualizing the co-occurrence of biblical references and theological themes.

## 3. Technical Stack

*   **Backend**: Flask, MongoDB (via `pymongo`)
*   **Frontend**: Jinja2, Chart.js, D3.js
*   **Deployment**: Docker

## 4. Setup and Installation

1.  **Clone & Setup Environment**:
    ```bash
    git clone <repository-url>
    cd ama_b_viewer
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure MongoDB**: Create a `.env` file with `MONGODB_URI="your_connection_string"`.
4.  **Run**: `python main.py`

For Docker deployment, see the `Dockerfile`.

## 5. Documentation

This project uses a structured documentation approach to ensure clarity and maintainability. 

*   **`README.md` (This file)**: High-level project overview.
*   **`CONTRIBUTING.md`**: Guidelines for developers, including workflow and commit conventions.
*   **`CHANGELOG.md`**: A chronological log of all significant changes.
*   **`docs/adr/`**: **Architectural Decision Records (ADRs)** that document *why* key technical decisions were made.
*   **`DEV_TASKS.md`**: A structured list of current and future development tasks.

## 6. API Endpoints

The application exposes several API endpoints to feed data to the frontend visualizations, including:

*   `/api/questions_categorization`
*   `/api/tag_frequency/<tag_type>`
*   `/api/bible_theme_network`
*   `/api/update_network_cache`