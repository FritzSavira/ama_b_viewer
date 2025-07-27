from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import os
import json
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

def check_and_update_schema(collection):
    """Compares the current schema with the last known schema and returns new fields."""
    schema_file = 'schema.json'
    current_fields = get_collection_schema(collection)
    
    try:
        with open(schema_file, 'r') as f:
            known_fields = set(json.load(f))
    except FileNotFoundError:
        known_fields = set()

    new_fields = current_fields - known_fields

    if new_fields:
        print("\nNew fields detected in the collection:")
        for field in sorted(list(new_fields)):
            print(f"- {field}")
        print("\n")

    # Update the schema file with the latest set of fields
    with open(schema_file, 'w') as f:
        json.dump(sorted(list(current_fields)), f, indent=4)
    
    return new_fields

new_fields_on_startup = check_and_update_schema(collection)

@app.context_processor
def utility_processor():
    def get_nested_value(doc, key_path):
        keys = key_path.split('.')
        value = doc
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return "N/A"
        return value
    return dict(get_nested_value=get_nested_value)

def format_document(doc):
    """Converts ObjectId to string for JSON serialization."""
    if '_id' in doc and isinstance(doc['_id'], ObjectId):
        doc['_id'] = str(doc['_id'])
    return doc

@app.route('/')
def index():
    """Renders the main page with the latest document."""
    show_view = request.args.get('show', 'all')
    try:
        latest_doc = collection.find_one(sort=[('_id', -1)])
        if latest_doc:
            return render_template('index.html', doc=format_document(latest_doc), new_fields=new_fields_on_startup, show=show_view)
        return render_template('index.html', doc=None, error="No records found", new_fields=new_fields_on_startup, show=show_view)
    except Exception as e:
        return render_template('index.html', doc=None, error=f"Error retrieving the latest record: {e}", new_fields=new_fields_on_startup, show=show_view)

@app.route('/view/<id>')
def view_document(id):
    """Renders the page with a specific document."""
    show_view = request.args.get('show', 'all')
    try:
        doc = collection.find_one({'_id': ObjectId(id)})
        if doc:
            return render_template('index.html', doc=format_document(doc), new_fields=new_fields_on_startup, show=show_view)
        return render_template('index.html', doc=None, error="Record not found", new_fields=new_fields_on_startup, show=show_view)
    except Exception as e:
        return render_template('index.html', doc=None, error=f"Error retrieving the record: {e}", new_fields=new_fields_on_startup, show=show_view)

@app.route('/previous/<id>')
def get_previous(id):
    """Redirects to the previous record."""
    show_view = request.args.get('show', 'all')
    try:
        current_id = ObjectId(id)
        prev_doc = collection.find_one(
            {"_id": {"$lt": current_id}},
            sort=[('_id', -1)]
        )
        if prev_doc:
            return redirect(url_for('view_document', id=str(prev_doc['_id']), show=show_view))
        return redirect(url_for('view_document', id=id, show=show_view)) # Stay on the same page if no previous
    except Exception as e:
        return render_template('index.html', doc=None, error=f"Error finding previous record: {e}", new_fields=new_fields_on_startup, show=show_view)

@app.route('/next/<id>')
def get_next(id):
    """Redirects to the next record."""
    show_view = request.args.get('show', 'all')
    try:
        current_id = ObjectId(id)
        next_doc = collection.find_one(
            {"_id": {"$gt": current_id}},
            sort=[('_id', 1)]
        )
        if next_doc:
            return redirect(url_for('view_document', id=str(next_doc['_id']), show=show_view))
        return redirect(url_for('view_document', id=id, show=show_view)) # Stay on the same page if no next
    except Exception as e:
        return render_template('index.html', doc=None, error=f"Error finding next record: {e}", new_fields=new_fields_on_startup, show=show_view)

@app.route('/delete/<id>', methods=['POST'])
def delete_document(id):
    """Deletes a record and redirects to the latest one."""
    try:
        current_id = ObjectId(id)
        collection.delete_one({"_id": current_id})
        return redirect(url_for('index'))
    except Exception as e:
        return render_template('index.html', doc=None, error=f"Error deleting the record: {e}", new_fields=new_fields_on_startup)

if __name__ == '__main__':
    check_and_update_schema(collection)
    # Enable debug mode only in the development environment
    port = int(os.environ.get('PORT', 5000))  # Use PORT environment variable or default to 5000
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true')