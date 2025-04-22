let currentDocumentId = null;

// Tastatursteuerung hinzufügen
document.addEventListener('keydown', function(event) {
    if (event.key === 'ArrowLeft') {
        loadPreviousDocument();
    } else if (event.key === 'ArrowRight') {
        loadNextDocument();
    } else if (event.key === 'Delete') {
        // Löschen mit der Entf-Taste
        deleteCurrentDocument();
    }
});

// Button-Eventlistener
document.getElementById('prevBtn').addEventListener('click', loadPreviousDocument);
document.getElementById('nextBtn').addEventListener('click', loadNextDocument);
document.getElementById('deleteBtn').addEventListener('click', deleteCurrentDocument);

// Beim Laden der Seite den neuesten Datensatz abrufen
window.addEventListener('DOMContentLoaded', loadLatestDocument);

function loadLatestDocument() {
    fetch('/api/latest')
        .then(response => {
            if (!response.ok) {
                throw new Error('Netzwerkantwort war nicht ok');
            }
            return response.json();
        })
        .then(data => {
            displayDocument(data);
            currentDocumentId = data._id;
        })
        .catch(error => {
            console.error('Fehler beim Laden des neuesten Dokuments:', error);
            alert('Fehler beim Laden des neuesten Dokuments');
        });
}

function loadPreviousDocument() {
    if (!currentDocumentId) return;

    fetch(`/api/previous/${currentDocumentId}`)
        .then(response => {
            if (!response.ok) {
                if (response.status === 404) {
                    alert('Kein vorheriger Datensatz vorhanden');
                    return null;
                }
                throw new Error('Netzwerkantwort war nicht ok');
            }
            return response.json();
        })
        .then(data => {
            if (data) {
                displayDocument(data);
                currentDocumentId = data._id;
            }
        })
        .catch(error => {
            console.error('Fehler beim Laden des vorherigen Dokuments:', error);
            alert('Fehler beim Laden des vorherigen Dokuments');
        });
}

function loadNextDocument() {
    if (!currentDocumentId) return;

    fetch(`/api/next/${currentDocumentId}`)
        .then(response => {
            if (!response.ok) {
                if (response.status === 404) {
                    alert('Kein nächster Datensatz vorhanden');
                    return null;
                }
                throw new Error('Netzwerkantwort war nicht ok');
            }
            return response.json();
        })
        .then(data => {
            if (data) {
                displayDocument(data);
                currentDocumentId = data._id;
            }
        })
        .catch(error => {
            console.error('Fehler beim Laden des nächsten Dokuments:', error);
            alert('Fehler beim Laden des nächsten Dokuments');
        });
}

// Neue Funktion zum Löschen des aktuellen Dokuments
function deleteCurrentDocument() {
    if (!currentDocumentId) return;

    // Sicherheitsabfrage
    if (!confirm('Möchten Sie diesen Datensatz wirklich löschen? Diese Aktion kann nicht rückgängig gemacht werden.')) {
        return; // Abbrechen, wenn der Benutzer auf "Abbrechen" klickt
    }

    // Speichere die aktuelle ID, um später den nächsten Datensatz zu laden
    const deletedId = currentDocumentId;

    // DELETE-Anfrage an die API senden
    fetch(`/api/delete/${currentDocumentId}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Netzwerkantwort war nicht ok');
        }
        return response.json();
    })
    .then(data => {
        // Erfolgsmeldung anzeigen
        alert('Datensatz erfolgreich gelöscht');

        // Versuche zuerst, den nächsten Datensatz zu laden
        fetch(`/api/next/${deletedId}`)
            .then(response => {
                if (!response.ok) {
                    if (response.status === 404) {
                        // Wenn kein nächster Datensatz existiert, versuche den vorherigen zu laden
                        return fetch(`/api/previous/${deletedId}`);
                    }
                    throw new Error('Netzwerkantwort war nicht ok');
                }
                return response;
            })
            .then(response => {
                if (!response.ok) {
                    if (response.status === 404) {
                        // Wenn auch kein vorheriger Datensatz existiert, lade den neuesten
                        return fetch('/api/latest');
                    }
                    throw new Error('Netzwerkantwort war nicht ok');
                }
                return response.json();
            })
            .then(data => {
                if (data) {
                    displayDocument(data);
                    currentDocumentId = data._id;
                } else {
                    // Fallback, wenn keine Daten zurückgegeben wurden
                    alert('Keine weiteren Datensätze vorhanden');
                    // Leere die Anzeige
                    clearDocument();
                    currentDocumentId = null;
                }
            })
            .catch(error => {
                console.error('Fehler beim Laden des nächsten Dokuments nach dem Löschen:', error);
                alert('Fehler beim Laden des nächsten Dokuments nach dem Löschen');
            });
    })
    .catch(error => {
        console.error('Fehler beim Löschen des Dokuments:', error);
        alert('Fehler beim Löschen des Dokuments: ' + error.message);
    });
}

// Funktion zum Leeren der Anzeige
function clearDocument() {
    document.getElementById('created').textContent = '';
    document.getElementById('model').textContent = '';
    document.getElementById('prompt').textContent = '';

    document.getElementById('category').textContent = '';
    document.getElementById('subcategory').textContent = '';
    document.getElementById('type').textContent = '';
    document.getElementById('complexity').textContent = '';
    document.getElementById('tags').textContent = '';
    document.getElementById('relation').textContent = '';
    document.getElementById('abstraction_level').textContent = '';
    document.getElementById('main_goal').textContent = '';
    document.getElementById('context').textContent = '';
    document.getElementById('expected_output').textContent = '';
    document.getElementById('generic_query').textContent = '';

    document.getElementById('message_content').innerHTML = '';
    document.getElementById('hauptthemen').textContent = '';
    document.getElementById('theologische_konzepte').textContent = '';
    document.getElementById('bibelreferenzen').textContent = '';
    document.getElementById('historischer_kontext').textContent = '';
    document.getElementById('zentrale_personen').textContent = '';

    document.getElementById('rating').textContent = '';
    document.getElementById('free_text').textContent = '';
}

function formatDate(timestamp) {
    if (!timestamp) return '';
    const date = new Date(timestamp * 1000);
    return date.toLocaleString('de-DE', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

function formatArray(arr) {
    if (!arr || !Array.isArray(arr)) return '';
    return arr.join(', ');
}

function formatObject(obj) {
    if (!obj) return '';
    if (Array.isArray(obj)) {
        return obj.map(item => {
            if (typeof item === 'object') {
                return Object.entries(item).map(([key, value]) => `${key}: ${value}`).join(', ');
            }
            return item;
        }).join('; ');
    }
    if (typeof obj === 'object') {
        return Object.entries(obj).map(([key, value]) => `${key}: ${value}`).join(', ');
    }
    return obj.toString();
}

// Diese Funktion wandelt Markdown-Text in HTML um
function renderMarkdown(text) {
    if (!text) return '';
    // Mit marked.js Markdown zu HTML konvertieren
    return marked.parse(text);
}

function displayDocument(doc) {
    // Header section
    if (doc.reply && doc.reply.completion) {
        document.getElementById('created').textContent = formatDate(doc.reply.completion.created);
        document.getElementById('model').textContent = doc.reply.completion.model || '';
    }
    document.getElementById('prompt').textContent = doc.prompt || '';

    // Question section
    if (doc.question_abstraction) {
        const qa = doc.question_abstraction;

        if (qa.categorization) {
            document.getElementById('category').textContent = qa.categorization.category || '';
            document.getElementById('subcategory').textContent = qa.categorization.subcategory || '';
            document.getElementById('type').textContent = qa.categorization.type || '';
            document.getElementById('complexity').textContent = qa.categorization.complexity || '';
        }

        if (qa.tagging) {
            document.getElementById('tags').textContent = formatArray(qa.tagging.tags);
            document.getElementById('relation').textContent = qa.tagging.relation || '';
            document.getElementById('abstraction_level').textContent = qa.tagging.abstraction_level || '';
        }

        if (qa.intent) {
            document.getElementById('main_goal').textContent = qa.intent.main_goal || '';
            document.getElementById('context').textContent = qa.intent.context || '';
            document.getElementById('expected_output').textContent = qa.intent.expected_output || '';
        }

        if (qa.semantic) {
            document.getElementById('generic_query').textContent = qa.semantic.generic_query || '';
        }
    }

    // Answer section - Hier wird Markdown zu HTML konvertiert
    if (doc.reply && doc.reply.completion && doc.reply.completion.choices && doc.reply.completion.choices.length > 0) {
        const message = doc.reply.completion.choices[0].message;
        if (message) {
            // Hier konvertieren wir Markdown zu HTML mit renderMarkdown
            document.getElementById('message_content').innerHTML = renderMarkdown(message.content || '');
        }
    }

    if (doc.tags) {
        document.getElementById('hauptthemen').textContent = formatArray(doc.tags.hauptthemen);
        document.getElementById('theologische_konzepte').textContent = formatArray(doc.tags.theologische_konzepte);
        document.getElementById('bibelreferenzen').textContent = formatArray(doc.tags.bibelreferenzen);
        document.getElementById('historischer_kontext').textContent = doc.tags.historischer_kontext || '';
        document.getElementById('zentrale_personen').textContent = formatObject(doc.tags.zentrale_personen);
    }

    // Feedback section - Auch hier könnte Markdown sein
    if (doc.feedback) {
        document.getElementById('rating').textContent = doc.feedback.rating || '';
        document.getElementById('free_text').textContent = doc.feedback.free_text || '';
    }
}