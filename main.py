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

import markdown

def get_answer_content(doc):
    """Safely retrieves the answer content and converts it from Markdown to HTML."""
    try:
        markdown_content = doc['reply']['completion']['choices'][0]['message']['content']
        return markdown.markdown(markdown_content, extensions=['fenced_code', 'tables'])
    except (KeyError, IndexError, TypeError):
        return "<p>Answer content not found at the expected path (reply.completion.choices[0].message.content).</p>"

def get_categorized_tags(doc):
    """Extracts and categorizes tags from the document, excluding empty categories."""
    categorized_tags = {}

    # Only include categories that are expected to have tags based on analysis
    tag_paths = {
        "Bibelreferenzen": "tags.bibelreferenzen",
        "Hauptthemen": "tags.hauptthemen",
        "Theologische Konzepte": "tags.theologische_konzepte"
    }

    for category_name, path in tag_paths.items():
        parts = path.split('.')
        current_level = doc
        found_tags = []
        try:
            for part in parts:
                if isinstance(current_level, dict) and part in current_level:
                    current_level = current_level[part]
                else:
                    raise KeyError # Path not found
            if isinstance(current_level, list):
                found_tags = [tag for tag in current_level if isinstance(tag, str)] # Ensure tags are strings
        except (KeyError, TypeError):
            found_tags = [] # No tags or invalid path

        if found_tags: # Only add category if tags are found
            categorized_tags[category_name] = found_tags

    return categorized_tags

@app.route('/view/<id>')
def view_document(id):
    doc = collection.find_one({'_id': ObjectId(id)})
    if not doc:
        return "Document not found", 404

    show_view = request.args.get('show', 'all')

    # Get the first and last document IDs for navigation
    first_doc = collection.find_one(sort=[('_id', 1)])
    last_doc = collection.find_one(sort=[('_id', -1)])
    first_doc_id = first_doc['_id'] if first_doc else None
    last_doc_id = last_doc['_id'] if last_doc else None

    # --- Prepare Page Title --- #
    # Safely get the information_goal for a more descriptive page title.
    page_title = "Document ID: " + str(doc.get('_id')) # Default title
    try:
        # Attempt to get the more descriptive title
        info_goal = doc['question_abstraction']['semantic']['information_goal']
        if info_goal:
            page_title = "Fragestellung: " + info_goal
    except (KeyError, TypeError):
        # If the path doesn't exist or is not a dict, the default title is used.
        pass

    # Prepare template context
    template_context = {
        'doc': doc,
        'show': show_view,
        'first_doc_id': first_doc_id,
        'last_doc_id': last_doc_id,
        'answer_content': None,  # Default to None
        'page_title': page_title,
        'categorized_tags': None # Default to None
    }

    # Populate specific view content
    if show_view == 'answer':
        template_context['answer_content'] = get_answer_content(doc)
    elif show_view == 'tags':
        template_context['categorized_tags'] = get_categorized_tags(doc)

    if show_view == 'question_abstraction':
        return render_template('question_abstraction_view.html', **template_context)
    else:
        return render_template('index.html', **template_context)

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
    app.run(debug=True, use_reloader=False)



