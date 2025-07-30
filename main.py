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

# Global constants for collection names
SOURCE_COLLECTION = "ama_log"
MAPPINGS_COLLECTION = "category_mappings"

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

    # Handle deprecated 'question' view by redirecting to 'all'
    if show_view == 'question':
        show_view = 'all'

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

def _aggregate_field(field_path, apply_mapping=False):
    pipeline = [
        {
            "$match": {
                field_path: {"$exists": True, "$ne": None, "$ne": ""}
            }
        }
    ]

    # Check if the field is an array (e.g., tags.hauptthemen) and needs unwinding
    # This is a heuristic; a more robust solution would involve schema analysis
    if field_path.startswith("tags."):
        pipeline.append({"$unwind": f"${field_path}"})
        # Ensure the unwound field is not empty after unwind
        pipeline.append({"$match": {field_path: {"$ne": None, "$ne": ""}}})

    if apply_mapping:
        # Add $lookup stage to join with the category_mappings collection
        pipeline.append({
            "$lookup": {
                "from": MAPPINGS_COLLECTION,
                "localField": field_path,
                "foreignField": "_id",
                "as": "mapping_data"
            }
        })
        # Add $addFields stage to use the mapped value if available, otherwise the original
        pipeline.append({
            "$addFields": {
                "_id_normalized": {
                    "$cond": {
                        "if": {"$gt": [{"$size": "$mapping_data"}, 0]},
                        "then": {"$arrayElemAt": ["$mapping_data.target", 0]},
                        "else": f"${field_path}"
                    }
                }
            }
        })
        # Group by the normalized field
        pipeline.append({
            "$group": {
                "_id": "$_id_normalized",
                "count": {"$sum": 1}
            }
        })
    else:
        # Group by the original field
        pipeline.append({
            "$group": {
                "_id": f"${field_path}",
                "count": {"$sum": 1}
            }
        })

    pipeline.append({
        "$sort": {
            "count": -1
        }
    })
    return list(db[SOURCE_COLLECTION].aggregate(pipeline))

@app.route('/api/questions_categorization')
def get_questions_categorization():
    data = {
        "category": _aggregate_field("question_abstraction.categorization.category", apply_mapping=True),
        "subcategory": _aggregate_field("question_abstraction.categorization.subcategory", apply_mapping=True),
        "type": _aggregate_field("question_abstraction.categorization.type", apply_mapping=True),
        "complexity": _aggregate_field("question_abstraction.categorization.complexity", apply_mapping=False), # No mapping for complexity
        "main_goal": _aggregate_field("question_abstraction.intent.main_goal", apply_mapping=True),
        "information_goal": _aggregate_field("question_abstraction.semantic.information_goal", apply_mapping=True),
        "domain": _aggregate_field("question_abstraction.semantic.domain", apply_mapping=True)
    }
    return jsonify(data)

@app.route('/api/tag_frequency/<tag_type>')
def get_tag_frequency(tag_type):
    valid_tag_types = ["bibelreferenzen", "hauptthemen", "theologische_konzepte"]
    if tag_type not in valid_tag_types:
        return jsonify({"error": "Invalid tag type. Valid types are: " + ", ".join(valid_tag_types)}), 400

    field_path = f"tags.{tag_type}"

    # Bibelreferenzen should not be mapped
    if tag_type == "bibelreferenzen":
        results = _aggregate_field(field_path, apply_mapping=False)
    else:
        results = _aggregate_field(field_path, apply_mapping=True)

    return jsonify(results)

def generate_network_data():
    # Aggregation to get the links (edges) and their counts
    links_pipeline = [
        {
            "$match": {
                "tags.bibelreferenzen": {"$exists": True, "$ne": []},
                "tags.hauptthemen": {"$exists": True, "$ne": []}
            }
        },
        {
            "$unwind": "$tags.bibelreferenzen"
        },
        {
            "$unwind": "$tags.hauptthemen"
        },
        {
            "$group": {
                "_id": {
                    "source": "$tags.bibelreferenzen",
                    "target": "$tags.hauptthemen"
                },
                "value": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "source": "$_id.source",
                "target": "$_id.target",
                "value": "$value"
            }
        }
    ]
    links_data = list(db[SOURCE_COLLECTION].aggregate(links_pipeline))

    # Extract unique nodes from the links data
    nodes_set = set()
    for link in links_data:
        nodes_set.add((link['source'], 'bibelreferenz'))
        nodes_set.add((link['target'], 'hauptthema'))

    nodes_data = []
    for node_id, node_type in nodes_set:
        nodes_data.append({"id": node_id, "type": node_type})

    return {"nodes": nodes_data, "links": links_data}

def update_network_cache():
    network_data = generate_network_data()
    cache_collection = db["ama_log_network_cache"]
    # Clear existing cache and insert new data
    cache_collection.delete_many({})
    cache_collection.insert_one({"_id": "network_data", "data": network_data})
    return True

@app.route('/api/update_network_cache')
def trigger_update_network_cache():
    update_network_cache()
    return jsonify({"message": "Network cache updated successfully."})

@app.route('/api/bible_theme_network')
def bible_theme_network():
    cache_collection = db["ama_log_network_cache"]
    cached_data = cache_collection.find_one({"_id": "network_data"})
    if cached_data and "data" in cached_data:
        return jsonify(cached_data["data"])
    else:
        return jsonify({"error": "Network data not found in cache. Please run /api/update_network_cache first."}), 404

@app.route('/questions_dashboard')
def questions_dashboard():
    return render_template('questions_dashboard.html')

@app.route('/tags_dashboard')
def tags_dashboard():
    return render_template('tags_dashboard.html')

@app.route('/network_graph_view')
def network_graph_view():
    return render_template('bible_theme_network.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)