# llm_mapper.py
# This script will contain the logic for semantic category aggregation using an LLM.

import os
import json
from dotenv import load_dotenv
from pymongo import MongoClient
from aio_straico import straico_client

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
MONGO_URI = os.getenv("MONGODB_URI")
STRAICO_API_KEY = os.getenv("STRAICO_API_KEY")
DB_NAME = "ama_browser"  # Explicitly set the correct database name
SOURCE_COLLECTION = "ama_log"
MAPPINGS_COLLECTION = "category_mappings"
LLM_MODEL = 'anthropic/claude-3.5-sonnet'
#LLM_MODEL = 'google/gemini-2.5-flash'

# Fields to be analyzed for mapping
FIELDS_TO_MAP = [
    "question_abstraction.categorization.category",
    "question_abstraction.categorization.subcategory",
    "question_abstraction.categorization.type",
    "question_abstraction.semantic.domain",
    "tags.hauptthemen",
    "tags.theologische_konzepte"
]


# --- Database Connection ---
def get_db():
    """Establishes a connection to the MongoDB database."""
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]


def get_unmapped_terms(db, field_path):
    """Finds unique terms in the source collection that are not yet in the mappings collection."""
    print(f"\n--- Analyzing field: {field_path} ---")

    pipeline = [
        {'$match': {field_path: {'$exists': True, '$ne': None, '$ne': ""}}},
        {'$project': {field_path: 1}},
        {'$unwind': f'${field_path}'},
        {'$group': {'_id': f'${field_path}'}}
    ]
    try:
        source_terms = {doc['_id'] for doc in db[SOURCE_COLLECTION].aggregate(pipeline) if doc['_id']}
        print(f"Found {len(source_terms)} unique terms in source collection.")
    except Exception as e:
        print(f"Error fetching source terms for {field_path}: {e}")
        return []

    try:
        if MAPPINGS_COLLECTION not in db.list_collection_names():
            print(f"Mappings collection '{MAPPINGS_COLLECTION}' does not exist. Assuming 0 mappings.")
            mapped_terms = set()
        else:
            mapped_terms = {doc['_id'] for doc in db[MAPPINGS_COLLECTION].find({}, {'_id': 1})}
        print(f"Found {len(mapped_terms)} existing mappings.")
    except Exception as e:
        print(f"Error fetching mapped terms for {field_path}: {e}")
        mapped_terms = set()

    unmapped_terms = list(source_terms - mapped_terms)
    print(f"Found {len(unmapped_terms)} new, unmapped terms.")
    
    return unmapped_terms


def get_mappings_from_llm(terms_to_map, existing_canons=None, batch_size=500):
    """Sends a list of terms to an LLM in batches and requests mappings to a canonical form."""
    if not terms_to_map:
        print("No new terms to map. Skipping LLM call.")
        return {}

    print(f"\n--- Sending {len(terms_to_map)} terms to LLM for mapping in batches of {batch_size} ---")
    all_mappings = {}

    # Construct the base of the prompt with instructions
    prompt_base = f"""Analyze the following list of categories. Some are duplicates or variations of each other.
Your task is to create a JSON object that maps each of these terms to a single, consistent, canonical form.

**IMPORTANT INSTRUCTIONS:**
1. The canonical terms you generate MUST be in German.
2. You have been provided with a list of preferred canonical terms (also in German). You MUST prioritize using a term from this list if a suitable one exists.
3. Only create a brand new canonical term if none of the preferred terms are a good fit.
"""

    if existing_canons:
        prompt_base += f"""\n**PREFERRED CANONICAL TERMS (in German):**
{json.dumps(existing_canons, indent=2)}
"""

    for i in range(0, len(terms_to_map), batch_size):
        batch = terms_to_map[i:i + batch_size]
        print(f"Processing batch {i // batch_size + 1}/{(len(terms_to_map) + batch_size - 1) // batch_size}...")

        # Add the new terms to the prompt for the current batch
        prompt = prompt_base + f"""\n**NEW TERMS TO MAP:**
{json.dumps(batch, indent=2)}

Respond with ONLY the JSON object, like this: {{\"original_term_1\": \"canonical_term_1\", \"original_term_2\": \"canonical_term_1\", ...}}."""

        try:
            # Set a reasonable timeout for the client initialization
            with straico_client(API_KEY=STRAICO_API_KEY, timeout=120) as client: # 2-minute timeout
                print("Awaiting response from LLM for batch...")
                reply = client.prompt_completion(LLM_MODEL, prompt)
                response_content = reply['completion']['choices'][0]['message']['content']
                print("LLM response for batch received.")
                
                batch_mappings = json.loads(response_content)
                all_mappings.update(batch_mappings)

        except Exception as e:
            print(f"An error occurred during the LLM API call for a batch: {e}")
            # We can decide to either stop or continue with the next batch.
            # For now, we'll just print the error and continue.
            pass

    return all_mappings




def save_mappings_to_db(db, field_path, mappings):
    """Saves the LLM-generated mappings to the category_mappings collection."""
    if not mappings:
        print("No mappings to save.")
        return

    print(f"\n--- Saving {len(mappings)} mappings for field '{field_path}' to database ---")
    mappings_collection = db[MAPPINGS_COLLECTION]
    
    for original_term, canonical_term in mappings.items():
        # Use upsert=True to insert if not exists, or update if exists
        result = mappings_collection.update_one(
            {'_id': original_term},
            {'$set': {'target': canonical_term}},
            upsert=True
        )
        if result.upserted_id:
            print(f"Inserted new mapping: '{original_term}' -> '{canonical_term}'")
        elif result.modified_count:
            print(f"Updated existing mapping: '{original_term}' -> '{canonical_term}'")

    print("Mappings saved successfully.")


if __name__ == "__main__":
    print("LLM Mapper script initialized.")
    try:
        db = get_db()
        db.command('ping')
        print(f"Successfully connected to MongoDB database: {db.name}")

        # --- Functionality Test ---
        test_field = "question_abstraction.categorization.subcategory"
        new_terms = get_unmapped_terms(db, test_field)
        
        if new_terms:
            # For this test, we only send a small sample to the LLM to avoid costs/long waits
            sample_terms = new_terms[:]
            print(f"\nSending a sample of {len(sample_terms)} terms to the LLM:")
            print(sample_terms)

            llm_mappings = get_mappings_from_llm(sample_terms)

            if llm_mappings:
                print("\n--- LLM-Generated Mappings (Sample) ---")
                print(json.dumps(llm_mappings, indent=2))
                # Save the mappings to the database
                save_mappings_to_db(db, test_field, llm_mappings)
        else:
            print(f"\nNo new terms to map for '{test_field}'.")

    except Exception as e:
        print(f"An error occurred: {e}")