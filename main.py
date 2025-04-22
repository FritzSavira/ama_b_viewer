from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus .env-Datei, falls vorhanden
load_dotenv()

app = Flask(__name__)

# MongoDB-Verbindung initialisieren
def get_mongo_client():
    """Erstellt und gibt einen MongoDB-Client zurück."""
    mongodb_uri = os.environ.get('MONGODB_URI')
    if not mongodb_uri:
        raise ValueError("MONGODB_URI ist nicht gesetzt. Bitte Umgebungsvariable oder .env-Datei überprüfen.")
    return MongoClient(mongodb_uri)

try:
    client = get_mongo_client()
    db = client["ama_browser"]
    collection = db["ama_log"]
except Exception as e:
    raise RuntimeError(f"Fehler beim Verbinden mit MongoDB: {e}")

def format_document(doc):
    """Konvertiert ObjectId zu String für JSON-Serialisierung."""
    if '_id' in doc and isinstance(doc['_id'], ObjectId):
        doc['_id'] = str(doc['_id'])
    return doc

@app.route('/')
def index():
    """Rendert die Hauptseite."""
    return render_template('index.html')

@app.route('/api/latest')
def get_latest():
    """Gibt den neuesten Datensatz zurück."""
    try:
        latest_doc = collection.find_one(sort=[('_id', -1)])
        if latest_doc:
            return jsonify(format_document(latest_doc))
        return jsonify({"error": "Keine Datensätze gefunden"}), 404
    except Exception as e:
        return jsonify({"error": f"Fehler beim Abrufen des neuesten Datensatzes: {e}"}), 500

@app.route('/api/previous/<id>')
def get_previous(id):
    """Gibt den vorherigen Datensatz basierend auf der ID zurück."""
    try:
        current_id = ObjectId(id)
        prev_doc = collection.find_one(
            {"_id": {"$lt": current_id}},
            sort=[('_id', -1)]
        )
        if prev_doc:
            return jsonify(format_document(prev_doc))
        return jsonify({"error": "Kein vorheriger Datensatz gefunden"}), 404
    except Exception as e:
        return jsonify({"error": f"Fehler beim Abrufen des vorherigen Datensatzes: {e}"}), 400

@app.route('/api/next/<id>')
def get_next(id):
    """Gibt den nächsten Datensatz basierend auf der ID zurück."""
    try:
        current_id = ObjectId(id)
        next_doc = collection.find_one(
            {"_id": {"$gt": current_id}},
            sort=[('_id', 1)]
        )
        if next_doc:
            return jsonify(format_document(next_doc))
        return jsonify({"error": "Kein nächster Datensatz gefunden"}), 404
    except Exception as e:
        return jsonify({"error": f"Fehler beim Abrufen des nächsten Datensatzes: {e}"}), 400

@app.route('/api/delete/<id>', methods=['DELETE'])
def delete_document(id):
    """Löscht einen Datensatz basierend auf der ID."""
    try:
        current_id = ObjectId(id)
        result = collection.delete_one({"_id": current_id})

        if result.deleted_count > 0:
            return jsonify({"success": True, "message": "Datensatz erfolgreich gelöscht"})
        return jsonify({"error": "Datensatz nicht gefunden"}), 404
    except Exception as e:
        return jsonify({"error": f"Fehler beim Löschen des Datensatzes: {e}"}), 400

if __name__ == '__main__':
    # Debug-Modus nur in der Entwicklungsumgebung aktivieren
    app.run(debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true')