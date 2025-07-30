### **Entwicklungs-Aufgabenliste: Auswertung und Visualisierung der ama_log Collection**

**Projekt:** ama_b_viewer - Auswertung und Visualisierung
**Konzept-Referenz:** `FEATURE_VISUAL.md`
**Stand:** 28. Juli 2025

---

#### **Phase 1: Backend - Datenaufbereitung (MongoDB Aggregation & Flask API Endpunkte)**

*   **Aufgabe 1.1: MongoDB Aggregation für "Fragen-Kategorisierung und -Intention"**
    *   **Beschreibung:** Definiere und teste MongoDB Aggregations-Pipelines zur Ermittlung der Verteilung von Fragen nach `question_abstraction.categorization.category`, `subcategory`, `type`, `complexity`, `question_abstraction.intent.main_goal`, `question_abstraction.semantic.information_goal` und `question_abstraction.semantic.domain`.
    *   **Referenz:** `FEATURE_VISUAL.md` -> 3.1. Fragen-Kategorisierung und -Intention -> Metriken
    *   **Status:** Erledigt
*   **Aufgabe 1.2: Flask API Endpoint für "Fragen-Kategorisierung und -Intention"**
    *   **Beschreibung:** Implementiere eine Flask-Route (z.B. `/api/questions_categorization`), die die aggregierten Daten aus Aufgabe 1.1 als JSON bereitstellt.
    *   **Referenz:** `FEATURE_VISUAL.md` -> 4. Technologischer Ansatz
    *   **Status:** Erledigt
*   **Aufgabe 1.3: MongoDB Aggregation für "Tag-Analyse" (Häufigkeit)**
    *   **Beschreibung:** Definiere und teste MongoDB Aggregations-Pipelines zur Ermittlung der Häufigkeit der einzelnen Tags in `tags.bibelreferenzen`, `tags.hauptthemen` und `tags.theologische_konzepte`.
    *   **Referenz:** `FEATURE_VISUAL.md` -> 3.2. Tag-Analyse -> Metriken
    *   **Status:** Erledigt
*   **Aufgabe 1.4: Flask API Endpoint für "Tag-Analyse" (Häufigkeit)**
    *   **Beschreibung:** Implementiere eine Flask-Route (z.B. `/api/tag_frequency`), die die aggregierten Daten aus Aufgabe 1.3 als JSON bereitstellt.
    *   **Referenz:** `FEATURE_VISUAL.md` -> 4. Technologischer Ansatz
    *   **Status:** Erledigt
*   **Aufgabe 1.5: MongoDB Aggregation für "Beziehung zwischen Bibelreferenzen und Hauptthemen" (Co-Occurrence für Caching)**
    *   **Beschreibung:** Definiere und teste MongoDB Aggregations-Pipelines zur Ermittlung der Co-Occurrence von `tags.bibelreferenzen` und `tags.hauptthemen`. Das Ergebnis sollte eine Liste von Knoten (Bibelreferenzen, Hauptthemen) und Kanten (Verbindungen mit Häufigkeit) sein, die für die Speicherung in einer Cache-Collection optimiert ist.
    *   **Referenz:** `FEATURE_VISUAL.md` -> 3.3. Beziehung zwischen Bibelreferenzen und Hauptthemen
    *   **Status:** Erledigt
*   **Aufgabe 1.5.1: Implementierung des Caching-Mechanismus für Netzwerkdaten**
    *   **Beschreibung:** Erstelle eine Funktion (oder ein separates Skript), die die Aggregations-Pipeline aus Aufgabe 1.5 ausführt und das Ergebnis (Knoten und Kanten) in einer neuen MongoDB Collection (z.B. `ama_log_network_cache`) speichert. Diese Funktion sollte bei Bedarf manuell oder periodisch aufrufbar sein.
    *   **Status:** Erledigt
*   **Aufgabe 1.6: Flask API Endpoint für "Beziehung zwischen Bibelreferenzen und Hauptthemen" (aus Cache)**
    *   **Beschreibung:** Implementiere eine Flask-Route (z.B. `/api/bible_theme_network`), die die vorbereiteten Netzwerkdaten (Knoten und Kanten) direkt aus der `ama_log_network_cache` Collection abruft und als JSON bereitstellt.
    *   **Referenz:** `FEATURE_VISUAL.md` -> 4. Technologischer Ansatz
    *   **Status:** Erledigt

#### **Phase 2: Frontend - Visualisierung**

*   **Aufgabe 2.1: Erstelle Frontend-Seite für "Fragen-Kategorisierung und -Intention"**
    *   **Beschreibung:** Erstelle ein neues HTML-Template (z.B. `questions_dashboard.html`) in Flask, das die Visualisierungen für Fragen-Kategorisierung und -Intention aufnimmt.
    *   **Referenz:** `FEATURE_VISUAL.md` -> 4. Technologischer Ansatz
    *   **Status:** Erledigt
*   **Aufgabe 2.2: Implementiere JavaScript-Visualisierungen für "Fragen-Kategorisierung und -Intention"**
    *   **Beschreibung:** Nutze Chart.js oder eine ähnliche Bibliothek, um interaktive Kreis- und Balkendiagramme für die Kategorisierungen sowie Listen/Wortwolken für Ziele und Intentionen zu erstellen. Datenabruf vom Flask API Endpoint (Aufgabe 1.2).
    *   **Referenz:** `FEATURE_VISUAL.md` -> 3.1. Fragen-Kategorisierung und -Intention -> Visualisierungen
    *   **Status:** Erledigt
*   **Aufgabe 2.3: Erstelle Frontend-Seite für "Tag-Analyse" (Häufigkeit)**
    *   **Beschreibung:** Erstelle ein neues HTML-Template (z.B. `tags_dashboard.html`) in Flask, das die Visualisierungen für die Tag-Analyse aufnimmt.
    *   **Referenz:** `FEATURE_VISUAL.md` -> 4. Technologischer Ansatz
    *   **Status:** Erledigt
*   **Aufgabe 2.4: Implementiere JavaScript-Visualisierungen für "Tag-Analyse" (Häufigkeit)**
    *   **Beschreibung:** Nutze Chart.js oder eine ähnliche Bibliothek, um Tag-Clouds und Balkendiagramme für die Top-N der häufigsten Tags zu erstellen. Datenabruf vom Flask API Endpoint (Aufgabe 1.4).
    *   **Referenz:** `FEATURE_VISUAL.md` -> 3.2. Tag-Analyse -> Visualisierungen
    *   **Status:** Erledigt
*   **Aufgabe 2.5: Erstelle Frontend-Seite für "Beziehung zwischen Bibelreferenzen und Hauptthemen"**
    *   **Beschreibung:** Erstelle ein neues HTML-Template (z.B. `bible_theme_network.html`) in Flask, das das Netzwerkdiagramm aufnimmt.
    *   **Referenz:** `FEATURE_VISUAL.md` -> 4. Technologischer Ansatz
    *   **Status:** Erledigt
*   **Aufgabe 2.6: Implementiere JavaScript-Visualisierung für "Beziehung zwischen Bibelreferenzen und Hauptthemen" (D3.js Force-Directed Graph)**
    *   **Beschreibung:** Nutze D3.js, um einen interaktiven Force-Directed Graph zu erstellen, der die Beziehungen zwischen Bibelreferenzen und Hauptthemen visualisiert. Implementiere Funktionen für Zoomen, Schwenken, Ziehen von Knoten und Detailanzeige. Datenabruf vom Flask API Endpoint (Aufgabe 1.6).
    *   **Referenz:** `FEATURE_VISUAL.md` -> 3.3. Beziehung zwischen Bibelreferenzen und Hauptthemen -> Technologie (Frontend)
    *   **Status:** Erledigt

#### **Phase 3: Integration & Verfeinerung**

*   **Aufgabe 3.1: Integriere Visualisierungen in die bestehende Benutzeroberfläche**
    *   **Beschreibung:** Füge Navigationslinks oder ein separates Dashboard in der `main.py` und den HTML-Templates hinzu, um auf die neuen Visualisierungsseiten zuzugreifen.
    *   **Referenz:** `FEATURE_VISUAL.md` -> 5. Nächste Schritte
    *   **Status:** Erledigt
*   **Aufgabe 3.2: Implementiere Fehlerbehandlung und Ladezustände**
    *   **Beschreibung:** Füge robuste Fehlerbehandlung für API-Aufrufe und Ladeindikatoren im Frontend hinzu, um eine bessere Nutzererfahrung zu gewährleisten.
    *   **Status:** Offen
*   **Aufgabe 3.3: Optimiere Performance der MongoDB-Queries und Frontend-Visualisierungen**
    *   **Beschreibung:** Überprüfe und optimiere die Aggregations-Pipelines und die Rendering-Performance der Frontend-Diagramme, insbesondere für große Datenmengen.
    *   **Status:** Offen
*   **Aufgabe 3.4: Dokumentation der Implementierung**
    *   **Beschreibung:** Erstelle technische Dokumentation für die neuen Backend-Endpunkte und Frontend-Komponenten, um die Wartbarkeit zu gewährleisten.
    *   **Status:** Offen
