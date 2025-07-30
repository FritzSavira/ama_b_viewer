# Contributing to ama_b_viewer

Vielen Dank für dein Interesse, an diesem Projekt mitzuwirken! Jede Hilfe ist willkommen. Um eine reibungslose Zusammenarbeit zu gewährleisten, bitten wir dich, die folgenden Richtlinien zu beachten.

## Entwicklungs-Workflow

1.  **Fork & Branch**: Erstelle einen Fork des Repositories und erstelle einen neuen Branch für dein Feature oder deinen Bugfix.
2.  **Implementierung**: Nimm deine Änderungen vor und halte dich dabei an den bestehenden Code-Stil.
3.  **Dokumentation**: Wenn du eine wesentliche Änderung vornimmst (z.B. ein neues Feature hinzufügst oder die Architektur änderst), erstelle bitte einen neuen **Architectural Decision Record (ADR)** im Verzeichnis `docs/adr/`.
4.  **Commits**: Schreibe aussagekräftige Commit-Nachrichten, die unserer Konvention entsprechen (siehe unten).
5.  **Pull Request**: Erstelle einen Pull Request gegen den `main`-Branch des Haupt-Repositories.

## Commit-Message-Konvention

Alle Commits in diesem Projekt müssen der **Conventional Commits** Spezifikation folgen. Dies sorgt für einen klaren und nachvollziehbaren Git-Verlauf. Jeder Commit, der sich auf ein dokumentiertes Feature oder eine Aufgabe bezieht, sollte eine Ticket-ID enthalten.

**Format:**
```
<type>(<scope>): <subject> (<ticket-id>)
```

*   **`<type>`:** Beschreibt die Art der Änderung (z.B. `feat` für ein neues Feature, `fix` für einen Bugfix, `docs` für Dokumentation, `refactor` für Code-Überarbeitung).
*   **`<scope>`:** Beschreibt den betroffenen Teil der Codebase (z.B. `backend`, `frontend`, `docs`, `db`).
*   **`<subject>`:** Eine kurze, prägnante Beschreibung der Änderung in der Gegenwartsform.
*   **`<ticket-id>`:** (Optional) Eine Referenz auf ein ADR (z.B. `ADR-001`) oder eine Aufgaben-ID (z.B. `TASK-3.2`).

**Beispiel:**
```
feat(backend): Add 'show' URL parameter to view routes (ADR-001)
```
