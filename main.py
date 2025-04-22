from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

# Load environment variables from .env file, if available
load_dotenv()

app = Flask(__name__)

# Initialize MongoDB connection
def get_mongo_client():
    """Creates and returns a MongoDB client."""
    mongodb_uri = os.environ.get('MONGODB_URI')
    if not mongodb_uri:
        raise ValueError("MONGODB_URI is not set. Please check the environment variable or .env file.")
    return MongoClient(mongodb_uri)

try:
    client = get_mongo_client()
    db = client["ama_browser"]
    collection = db["ama_log"]
except Exception as e:
    raise RuntimeError(f"Error connecting to MongoDB: {e}")

def format_document(doc):
    """Converts ObjectId to string for JSON serialization."""
    if '_id' in doc and isinstance(doc['_id'], ObjectId):
        doc['_id'] = str(doc['_id'])
    return doc

@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/api/latest')
def get_latest():
    """Returns the latest record."""
    try:
        latest_doc = collection.find_one(sort=[('_id', -1)])
        if latest_doc:
            return jsonify(format_document(latest_doc))
        return jsonify({"error": "No records found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error retrieving the latest record: {e}"}), 500

@app.route('/api/previous/<id>')
def get_previous(id):
    """Returns the previous record based on the ID."""
    try:
        current_id = ObjectId(id)
        prev_doc = collection.find_one(
            {"_id": {"$lt": current_id}},
            sort=[('_id', -1)]
        )
        if prev_doc:
            return jsonify(format_document(prev_doc))
        return jsonify({"error": "No previous record found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error retrieving the previous record: {e}"}), 400

@app.route('/api/next/<id>')
def get_next(id):
    """Returns the next record based on the ID."""
    try:
        current_id = ObjectId(id)
        next_doc = collection.find_one(
            {"_id": {"$gt": current_id}},
            sort=[('_id', 1)]
        )
        if next_doc:
            return jsonify(format_document(next_doc))
        return jsonify({"error": "No next record found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error retrieving the next record: {e}"}), 400

@app.route('/api/delete/<id>', methods=['DELETE'])
def delete_document(id):
    """Deletes a record based on the ID."""
    try:
        current_id = ObjectId(id)
        result = collection.delete_one({"_id": current_id})

        if result.deleted_count > 0:
            return jsonify({"success": True, "message": "Record successfully deleted"})
        return jsonify({"error": "Record not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error deleting the record: {e}"}), 400

if __name__ == '__main__':
    # Enable debug mode only in the development environment
    port = int(os.environ.get('PORT', 5000))  # Use PORT environment variable or default to 5000
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true')