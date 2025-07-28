# Feature Specification: Filtered Data Views

**Autor:** Gemini  
**Datum:** 2025-07-27  
**Status:** Completed  
**Ticket:** VIEW-01

---

## 1. Übersicht

Dieses Dokument beschreibt die Implementierung von gefilterten Sichten im MongoDB Datensatz Viewer. Ziel ist es, dem Benutzer zu ermöglichen, den angezeigten Datensatz auf bestimmte, relevante Abschnitte zu reduzieren, um die Analyse und Lesbarkeit zu verbessern.

## 2. User Story

**Als** Benutzer, der MongoDB-Datensätze analysiert,  
**möchte ich** zwischen einer vollständigen Datenansicht und gefilterten Ansichten für "Question", "Answer" und "Tags" wechseln können,  
**damit ich** mich schnell auf bestimmte Teile eines Datensatzes konzentrieren kann, ohne von irrelevanten Daten abgelenkt zu werden.

## 3. Akzeptanzkriterien

- **AC-1: Tab-Navigation:** Eine Navigationsleiste mit den Tabs "All", "Question", "Answer" und "Tags" ist im Frontend sichtbar.
- **AC-2: Standard-Sicht:** Die "All"-Sicht ist beim Laden der Seite standardmäßig aktiv und zeigt das vollständige, verschachtelte Dokument an.
- **AC-3: "Question"-Sicht:** Die "Question"-Sicht zeigt ausschließlich den Inhalt des `question`-Objekts an. Ist dieses nicht vorhanden, wird eine entsprechende Meldung angezeigt.
- **AC-4: "Answer"-Sicht:** Die "Answer"-Sicht zeigt ausschließlich den Inhalt des `answer`-Objekts an. Ist dieses nicht vorhanden, wird eine entsprechende Meldung angezeigt.
- **AC-5: "Tags"-Sicht:** Die "Tags"-Sicht extrahiert und zeigt eine konsolidierte Liste der Werte aus allen Feldern an, die Listen/Arrays sind (z.B. `tags`, `hauptthemen`, `bibelreferenzen`).
- **AC-6: Aktiver Zustand:** Der aktuell ausgewählte Tab ist visuell hervorgehoben.
- **AC-7: Persistente Navigation:** Die "Vorheriger"- und "Nächster"-Buttons behalten die aktuell ausgewählte Sicht bei.

## 4. Technischer Implementierungsplan

Die Umsetzung erfolgt ohne den Einsatz von clientseitigem JavaScript. Die Logik wird serverseitig in Flask/Jinja2 abgebildet.

### 4.1. Backend (`main.py`)

#### Task 4.1.1: Routen anpassen

- Die Routen `@app.route('/')` und `@app.route('/view/<id>')` müssen einen optionalen URL-Query-Parameter `show` akzeptieren (z.B. `/view/some_id?show=question`).
- Der Standardwert für `show` ist `'all'`.
- Der `show`-Parameter wird an die `render_template()`-Funktion durchgereicht.

#### Task 4.1.2: Navigationslogik erweitern

- Die Funktionen `get_previous(id)` und `get_next(id)` müssen den `show`-Parameter aus den `request.args` auslesen.
- Der `show`-Parameter muss in den `redirect(url_for(...))` Aufrufen weitergegeben werden, um den Zustand der Sicht bei der Navigation zu erhalten.

### 4.2. Frontend (`templates/index.html`)

#### Task 4.2.1: Tab-Navigation implementieren

- Eine HTML-Struktur (z.B. `<nav>`) für die Tabs wird hinzugefügt.
- Jeder Link verweist auf die URL des aktuellen Dokuments, ergänzt um den passenden `show`-Parameter.
  ```jinja
  <a href="{{ url_for('view_document', id=doc['_id'], show='question') }}">Question</a>
  ```

#### Task 4.2.2: CSS für Tabs erstellen

- Die Navigations-Tabs werden mit CSS formatiert.
- Eine `.active`-Klasse wird definiert, um den aktiven Tab hervorzuheben. Der `show`-Parameter wird genutzt, um diese Klasse dynamisch zu setzen.
  ```jinja
  <a href="..." class="{{ 'active' if show == 'question' else '' }}">Question</a>
  ```

#### Task 4.2.3: Bedingtes Rendern der Sichten

- Der Haupt-Anzeigebereich wird durch einen `if/elif/else`-Block in Jinja2 gesteuert.
- `{% if show == 'all' %}`: Rendert die bestehende rekursive Makro-Anzeige.
- `{% elif show == 'question' %}`: Greift auf `doc.question` zu und rendert dessen Inhalt oder eine "Nicht gefunden"-Meldung.
- `{% elif show == 'answer' %}`: Greift auf `doc.answer` zu und rendert dessen Inhalt oder eine "Nicht gefunden"-Meldung.
- `{% elif show == 'tags' %}`: Implementiert eine Schleife, die durch das `doc`-Objekt iteriert, alle Listen-Felder findet und deren Inhalte anzeigt.

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
