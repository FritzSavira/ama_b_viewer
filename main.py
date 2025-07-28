from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file, if available
load_dotenv()


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


