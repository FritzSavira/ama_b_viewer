from flask import Flask, render_template, jsonify, request, redirect, url_for
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
    """Renders the main page with the latest document."""
    try:
        latest_doc = collection.find_one(sort=[('_id', -1)])
        if latest_doc:
            return render_template('index.html', doc=format_document(latest_doc))
        return render_template('index.html', doc=None, error="No records found")
    except Exception as e:
        return render_template('index.html', doc=None, error=f"Error retrieving the latest record: {e}")

@app.route('/view/<id>')
def view_document(id):
    """Renders the page with a specific document."""
    try:
        doc = collection.find_one({'_id': ObjectId(id)})
        if doc:
            return render_template('index.html', doc=format_document(doc))
        return render_template('index.html', doc=None, error="Record not found")
    except Exception as e:
        return render_template('index.html', doc=None, error=f"Error retrieving the record: {e}")

@app.route('/previous/<id>')
def get_previous(id):
    """Redirects to the previous record."""
    try:
        current_id = ObjectId(id)
        prev_doc = collection.find_one(
            {"_id": {"$lt": current_id}},
            sort=[('_id', -1)]
        )
        if prev_doc:
            return redirect(url_for('view_document', id=str(prev_doc['_id'])))
        return redirect(url_for('view_document', id=id)) # Stay on the same page if no previous
    except Exception as e:
        return render_template('index.html', doc=None, error=f"Error finding previous record: {e}")

@app.route('/next/<id>')
def get_next(id):
    """Redirects to the next record."""
    try:
        current_id = ObjectId(id)
        next_doc = collection.find_one(
            {"_id": {"$gt": current_id}},
            sort=[('_id', 1)]
        )
        if next_doc:
            return redirect(url_for('view_document', id=str(next_doc['_id'])))
        return redirect(url_for('view_document', id=id)) # Stay on the same page if no next
    except Exception as e:
        return render_template('index.html', doc=None, error=f"Error finding next record: {e}")

@app.route('/delete/<id>', methods=['POST'])
def delete_document(id):
    """Deletes a record and redirects to the latest one."""
    try:
        current_id = ObjectId(id)
        collection.delete_one({"_id": current_id})
        return redirect(url_for('index'))
    except Exception as e:
        return render_template('index.html', doc=None, error=f"Error deleting the record: {e}")

if __name__ == '__main__':
    # Enable debug mode only in the development environment
    port = int(os.environ.get('PORT', 5000))  # Use PORT environment variable or default to 5000
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true')