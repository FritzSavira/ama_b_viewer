from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file, if available
load_dotenv()

app = Flask(__name__)

# Custom Jinja2 filter to convert Python dict to JSON string
import json
from bson import ObjectId

@app.template_filter('tojson')
def tojson_filter(value, indent=None):
    class CustomEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, ObjectId):
                return str(obj)
            return json.JSONEncoder.default(self, obj)
    return json.dumps(value, indent=indent, cls=CustomEncoder)


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

def get_collection_schema(collection):
    """Analyzes the collection to get a set of all unique field paths."""
    fields = set()
    # Sample a number of documents to check for fields
    # Using a larger sample increases the chance of finding all fields in a varied collection
    for doc in collection.find().limit(200):
        # Recursively find all field paths
        def find_fields(document, prefix=''):
            if isinstance(document, dict):
                for key, value in document.items():
                    path = f"{prefix}.{key}" if prefix else key
                    fields.add(path)
                    find_fields(value, path)
            elif isinstance(document, list):
                for item in document:
                    find_fields(item, prefix)
        find_fields(doc)
    return fields

@app.route('/')
def index():
    return redirect(url_for('view_document', id=collection.find_one()['_id']))

@app.route('/view/<id>')
def view_document(id):
    doc = collection.find_one({'_id': ObjectId(id)})
    if not doc:
        return "Document not found", 404

    show_view = request.args.get('show', 'all')

    if show_view == 'question_abstraction':
        return render_template('question_abstraction_view.html', doc=doc, show=show_view)
    else:
        return render_template('index.html', doc=doc, show=show_view)

@app.route('/next/<id>')
def next_document(id):
    current_doc = collection.find_one({'_id': ObjectId(id)})
    if not current_doc:
        return "Document not found", 404

    next_doc = collection.find_one({'_id': {'$gt': ObjectId(id)}}, sort=[('_id', 1)])
    if next_doc:
        show_view = request.args.get('show', 'all')
        return redirect(url_for('view_document', id=next_doc['_id'], show=show_view))
    else:
        return "No next document", 404

@app.route('/previous/<id>')
def previous_document(id):
    current_doc = collection.find_one({'_id': ObjectId(id)})
    if not current_doc:
        return "Document not found", 404

    previous_doc = collection.find_one({'_id': {'$lt': ObjectId(id)}}, sort=[('_id', -1)])
    if previous_doc:
        show_view = request.args.get('show', 'all')
        return redirect(url_for('view_document', id=previous_doc['_id'], show=show_view))
    else:
        return "No previous document", 404

if __name__ == '__main__':
    app.run(debug=True)



