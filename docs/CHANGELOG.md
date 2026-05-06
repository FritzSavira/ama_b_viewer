# Development Log

## 2026-05-06 - Anzeige von Erstellungsdatum und Uhrzeit hinzugefügt

### Overview
In den Ansichten "Question Abstraction", "Answer" und "Tags" wird nun das Datum und die Uhrzeit der Erstellung des Dokuments angezeigt.

### Key Changes & Rationale
- Ein Jinja2-Filter `datetimeformat` wurde in `main.py` hinzugefügt, um Zeitstempel konsistent zu formatieren.
- Das `creation_time` (extrahiert aus der MongoDB `ObjectId`) wird nun an die Templates übergeben.
- Die Templates `index.html` und `question_abstraction_view.html` wurden aktualisiert, um die Informationen anzuzeigen.
- Ein neuer Test `tests/test_creation_time.py` wurde hinzugefügt, um die korrekte Anzeige zu verifizieren.

### Files Modified
- main.py
- templates/index.html
- templates/question_abstraction_view.html
- tests/test_creation_time.py
- docs/CHANGELOG.md
