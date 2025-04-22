from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus .env-Datei, falls vorhanden
load_dotenv()

app = Flask(__name__)

# MongoDB Atlas Verbindung herstellen
# In einer .env-Datei oder als Umgebungsvariable bereitstellen
MONGODB_URI = os.environ.get('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client["ama_browser"]
collection = db["ama_log"]


def format_document(doc):
    # Konvertiere ObjectId zu String für JSON-Serialisierung
    if '_id' in doc and isinstance(doc['_id'], ObjectId):
        doc['_id'] = str(doc['_id'])
    return doc


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/latest')
def get_latest():
    # Den neuesten Datensatz abrufen
    latest_doc = collection.find_one(sort=[('_id', -1)])
    if latest_doc:
        return jsonify(format_document(latest_doc))
    return jsonify({"error": "Keine Datensätze gefunden"}), 404


@app.route('/api/previous/<id>')
def get_previous(id):
    # Den vorherigen Datensatz abrufen
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
        return jsonify({"error": str(e)}), 400


@app.route('/api/next/<id>')
def get_next(id):
    # Den nächsten Datensatz abrufen
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
        return jsonify({"error": str(e)}), 400


@app.route('/api/delete/<id>', methods=['DELETE'])
def delete_document(id):
    # Einen Datensatz löschen
    try:
        current_id = ObjectId(id)
        result = collection.delete_one({"_id": current_id})

        if result.deleted_count > 0:
            return jsonify({"success": True, "message": "Datensatz erfolgreich gelöscht"})
        return jsonify({"error": "Datensatz nicht gefunden"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)