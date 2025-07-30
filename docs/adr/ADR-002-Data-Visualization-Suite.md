# ADR-002: Data Visualization Suite

**Author:** Gemini
**Date:** 2025-07-28
**Status:** Implemented

---

## 1. Introduction

This document outlines the concept for the analysis and visualization of data from the `ama_log` MongoDB Atlas Collection. The goal is to gain insights into the application's usage, the quality of the generated responses, and the nature of the questions being asked.

## 2. Data Sources

The primary data source is the `ama_log` collection in MongoDB Atlas. The collection's schema is extensive, providing detailed information on:

-   User questions (`frage`)
-   Generated answers (`reply`)
-   User feedback (`feedback`)
-   Abstractions and categorizations of questions (`question_abstraction`)
-   Semantic tags (`tags`)
-   Usage data and API call costs (`reply.completion.usage`, `reply.price`)

## 3. Key Areas for Analysis and Visualization

### 3.1. Question Categorization and Intent

-   **Goal:** Analyze the types of questions asked and the underlying user intentions.
-   **Metrics:**
    -   Distribution of questions by `question_abstraction.categorization.category`, `subcategory`, `type`, `complexity`.
    -   Frequency of `question_abstraction.intent.main_goal` and `question_abstraction.semantic.information_goal`.
    -   Distribution of `question_abstraction.semantic.domain`.
-   **Visualizations:**
    -   Pie charts or bar charts for categorizations.
    -   Lists or word clouds for goals and intentions.

### 3.2. Tag Analysis

-   **Goal:** Identify the dominant themes and concepts in the questions and answers.
-   **Metrics:**
    -   Frequency of individual tags in `tags.bibelreferenzen`, `tags.hauptthemen`, `tags.theologische_konzepte`.
    -   Co-occurrence of tags (which tags frequently appear together).
-   **Visualizations:**
    -   Tag clouds for the main tag categories.
    -   Bar charts for the top-N most frequent tags.

### 3.3. Relationship between Biblical References and Main Themes

-   **Goal:** Visualize the semantic links between biblical references and main themes.
-   **Method:** Force-Directed Graph.
-   **Nodes:** Unique `tags.bibelreferenzen` and `tags.hauptthemen`.
-   **Edges:** Exist if a biblical reference and a main theme co-occur in the same document. The edge weight represents the frequency of co-occurrence.
-   **Interactivity:** Zooming, panning, dragging nodes, displaying details on hover/click, filtering options.
-   **Technology (Frontend):** D3.js for creating the dynamic network.

## 4. Technological Approach

The visualizations are implemented as new routes in the existing Flask application. MongoDB aggregation pipelines are used for data aggregation and preparation. The frontend rendering is done using JavaScript libraries like Chart.js or D3.js to create interactive and appealing diagrams.

## 5. Next Steps

1.  Detailed definition of the required MongoDB aggregation queries for each metric.
2.  Creation of Flask routes to provide the prepared data as a JSON API.
3.  Development of the frontend components (HTML, CSS, JavaScript) to visualize the data.
4.  Integration of the visualizations into the existing user interface or creation of a separate dashboard.
