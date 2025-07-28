# Konzept für Auswertung und Visualisierung der ama_log Collection

## 1. Einleitung
Dieses Dokument beschreibt das Konzept für die Auswertung und Visualisierung der Daten aus der MongoDB Atlas Collection `ama_log`. Ziel ist es, Einblicke in die Nutzung der Anwendung, die Qualität der generierten Antworten und die Art der gestellten Fragen zu gewinnen.

## 2. Datenquellen
Die primäre Datenquelle ist die `ama_log` Collection in MongoDB Atlas. Das Schema der Collection ist umfangreich und bietet detaillierte Informationen zu:
- Gestellten Fragen (`frage`)
- Generierten Antworten (`reply`)
- Nutzer-Feedback (`feedback`)
- Abstraktionen und Kategorisierungen der Fragen (`question_abstraction`)
- Semantischen Tags (`tags`)
- Nutzungsdaten und Kosten der API-Aufrufe (`reply.completion.usage`, `reply.price`)

## 3. Schlüsselbereiche für Auswertung und Visualisierung

### 3.1. Fragen-Kategorisierung und -Intention
- **Ziel:** Analyse der Art der gestellten Fragen und der dahinterliegenden Nutzerintentionen.
- **Metriken:**
    - Verteilung der Fragen nach `question_abstraction.categorization.category`, `subcategory`, `type`, `complexity`.
    - Häufigkeit der `question_abstraction.intent.main_goal` und `question_abstraction.semantic.information_goal`.
    - Verteilung der `question_abstraction.semantic.domain`.
- **Visualisierungen:**
    - Kreisdiagramme oder Balkendiagramme für Kategorisierungen.
    - Listen oder Wortwolken für Ziele und Intentionen.

### 3.2. Tag-Analyse
- **Ziel:** Identifizierung der dominanten Themen und Konzepte in den Fragen und Antworten.
- **Metriken:**
    - Häufigkeit der einzelnen Tags in `tags.bibelreferenzen`, `tags.hauptthemen`, `tags.theologische_konzepte`.
    - Co-Occurrence von Tags (welche Tags treten häufig zusammen auf).
- **Visualisierungen:**
    - Tag-Clouds für die wichtigsten Tag-Kategorien.
    - Balkendiagramme für die Top-N der häufigsten Tags.

### 3.3. Beziehung zwischen Bibelreferenzen und Hauptthemen
- **Ziel:** Visualisierung der semantischen Verknüpfungen zwischen Bibelreferenzen und Hauptthemen.
- **Methode:** Force-Directed Graph (Kräftebasiertes Diagramm).
- **Knoten:** Eindeutige `tags.bibelreferenzen` und `tags.hauptthemen`.
- **Kanten:** Existieren, wenn eine Bibelreferenz und ein Hauptthema im selben Dokument vorkommen. Die Kantenstärke repräsentiert die Häufigkeit der Co-Occurrence.
- **Interaktivität:** Zoomen, Schwenken, Ziehen von Knoten, Anzeigen von Details beim Hovern/Klicken, Filteroptionen.
- **Technologie (Frontend):** D3.js für die Erstellung des dynamischen Netzwerks.

## 4. Technologischer Ansatz
Die Visualisierungen werden als neue Routen in der bestehenden Flask-Anwendung implementiert. Für die Datenaggregation und -aufbereitung werden MongoDB-Aggregations-Pipelines verwendet. Die Darstellung im Frontend erfolgt mittels JavaScript-Bibliotheken wie Chart.js oder D3.js, um interaktive und ansprechende Diagramme zu erstellen.

## 5. Nächste Schritte
1.  Detaillierte Definition der benötigten MongoDB-Aggregations-Queries für jede Metrik.
2.  Erstellung der Flask-Routen zur Bereitstellung der aufbereiteten Daten als JSON-API.
3.  Entwicklung der Frontend-Komponenten (HTML, CSS, JavaScript) zur Visualisierung der Daten.
4.  Integration der Visualisierungen in die bestehende Benutzeroberfläche oder Erstellung eines separaten Dashboards.