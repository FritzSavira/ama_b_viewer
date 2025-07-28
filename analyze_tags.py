from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_mongo_client():
    mongodb_uri = os.environ.get('MONGODB_URI')
    if not mongodb_uri:
        raise ValueError("MONGODB_URI is not set. Please check the environment variable or .env file.")
    return MongoClient(mongodb_uri)

try:
    client = get_mongo_client()
    db = client["ama_browser"]
    collection = db["ama_log"]
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit()

tag_categories = [
    "tags.bibelreferenzen",
    "tags.hauptthemen",
    "tags.historischer_kontext",
    "tags.konfession",
    "tags.pastorale_themen",
    "tags.theologische_konzepte"
]

tag_counts = {category: 0 for category in tag_categories}
total_tags_found = 0
documents_processed = 0

def get_nested_value(doc, path):
    parts = path.split('.')
    current = doc
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current

# Fetch last 100 documents (assuming _id is monotonically increasing or using a timestamp field)
# For simplicity, we'll just fetch the last 100 by _id descending
for doc in collection.find().sort('_id', -1).limit(100):
    documents_processed += 1
    for category_path in tag_categories:
        tags = get_nested_value(doc, category_path)
        if isinstance(tags, list):
            tag_counts[category_path] += len(tags)
            total_tags_found += len(tags)

print(f"\n--- Tag Analysis Results (Last {documents_processed} Documents) ---")
print("Total documents processed: {documents_processed}")
print("Total tags found across all specified categories: {total_tags_found}\n")

print("Tags per category:")
for category, count in tag_counts.items():
    print(f"- {category}: {count} tags")

print("\n--- End of Analysis ---")