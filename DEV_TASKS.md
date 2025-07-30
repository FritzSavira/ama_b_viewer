---
project: "ama_b_viewer"
title: "Entwicklungs-Aufgabenliste: Auswertung und Visualisierung"
version: 1.0.0
last_updated: "2025-07-30"
---

# Entwicklungs-Aufgabenliste

Dieses Dokument verfolgt die Entwicklungsaufgaben für das Projekt `ama_b_viewer`.

## Phase 1: Backend - Datenaufbereitung (Abgeschlossen)

- [x] **TASK-1.1:** MongoDB Aggregation für "Fragen-Kategorisierung und -Intention"
  - **description:** Aggregations-Pipelines zur Ermittlung der Verteilung von Fragen-Metadaten.
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [x] **TASK-1.2:** Flask API Endpoint für "Fragen-Kategorisierung und -Intention"
  - **description:** API-Endpunkt (`/api/questions_categorization`) zur Bereitstellung der Daten aus TASK-1.1.
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [x] **TASK-1.3:** MongoDB Aggregation für "Tag-Analyse"
  - **description:** Aggregations-Pipelines zur Ermittlung der Häufigkeit von Tags.
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [x] **TASK-1.4:** Flask API Endpoint für "Tag-Analyse"
  - **description:** API-Endpunkt (`/api/tag_frequency`) zur Bereitstellung der Daten aus TASK-1.3.
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [x] **TASK-1.5:** MongoDB Aggregation für "Beziehungs-Netzwerk" (Co-Occurrence)
  - **description:** Aggregation zur Ermittlung der Co-Occurrence von Bibelreferenzen und Hauptthemen für das Caching.
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [x] **TASK-1.6:** Implementierung des Caching-Mechanismus für Netzwerkdaten
  - **description:** Funktion zum Speichern der Netzwerkdaten in einer Cache-Collection (`ama_log_network_cache`).
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [x] **TASK-1.7:** Flask API Endpoint für "Beziehungs-Netzwerk"
  - **description:** API-Endpunkt (`/api/bible_theme_network`) zur Bereitstellung der gecachten Netzwerkdaten.
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

## Phase 2: Frontend - Visualisierung (Abgeschlossen)

- [x] **TASK-2.1:** Frontend-Seite und Visualisierung für "Fragen-Kategorisierung"
  - **description:** Erstellung von `questions_dashboard.html` und Implementierung von Chart.js-Diagrammen.
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [x] **TASK-2.2:** Frontend-Seite und Visualisierung für "Tag-Analyse"
  - **description:** Erstellung von `tags_dashboard.html` und Implementierung von Tag-Clouds/Balkendiagrammen.
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [x] **TASK-2.3:** Frontend-Seite und Visualisierung für "Beziehungs-Netzwerk"
  - **description:** Erstellung von `bible_theme_network.html` und Implementierung des D3.js Force-Directed Graph.
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

## Phase 3: Integration & Verfeinerung

- [x] **TASK-3.1:** Integration der Visualisierungen in die UI
  - **description:** Hinzufügen von Navigationslinks zu den neuen Dashboard-Seiten.
  - **status:** completed
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [ ] **TASK-3.2:** Implementiere Fehlerbehandlung und Ladezustände
  - **description:** Robuste Fehlerbehandlung für API-Aufrufe und Ladeindikatoren im Frontend hinzufügen.
  - **status:** pending
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [ ] **TASK-3.3:** Performance-Optimierung
  - **description:** Überprüfung und Optimierung der Aggregations-Pipelines und der Rendering-Performance.
  - **status:** pending
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`

- [ ] **TASK-3.4:** Technische Dokumentation
  - **description:** Erstellung der technischen Dokumentation für Backend-Endpunkte und Frontend-Komponenten.
  - **status:** pending
  - **reference:** `docs/adr/ADR-002-Data-Visualization-Suite.md`