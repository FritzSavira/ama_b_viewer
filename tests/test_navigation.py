import pytest
from bs4 import BeautifulSoup
from pymongo import MongoClient
import os

# This uses the 'client' fixture from conftest.py

def get_db_collection():
    """Helper to connect to the test DB. Assumes MongoDB is running."""
    mongodb_uri = os.environ.get('MONGODB_URI')
    client = MongoClient(mongodb_uri)
    db = client["ama_browser"]
    collection = db["ama_log"]
    return collection

def test_navigation_buttons_on_last_document(client):
    """
    Tests if the 'Next' and 'Last' buttons are disabled on the last document page.
    """
    collection = get_db_collection()
    # Find the last document
    last_doc = collection.find_one(sort=[('_id', -1)])
    assert last_doc is not None, "Database must have at least one document for this test to run."

    # Request the page for the last document
    response = client.get(f'/view/{last_doc["_id"]}')
    assert response.status_code == 200

    # Parse the HTML
    soup = BeautifulSoup(response.data, 'html.parser')

    # Find the navigation buttons
    next_button = soup.find('a', {'id': 'next-button'})
    last_button = soup.find('a', {'id': 'last-button'})
    previous_button = soup.find('a', {'id': 'previous-button'})

    # Assert that 'Next' and 'Last' are disabled
    assert 'disabled' in next_button.get('class', []), "Next button should be disabled on the last page."
    assert 'disabled' in last_button.get('class', []), "Last button should be disabled on the last page."

    # Assert that 'Previous' is not disabled (assuming more than one doc)
    if collection.count_documents({}) > 1:
        assert 'disabled' not in previous_button.get('class', []), "Previous button should be enabled on the last page if it's not the only document."

def test_navigation_buttons_on_first_document(client):
    """
    Tests if the 'First' and 'Previous' buttons are disabled on the first document page.
    """
    collection = get_db_collection()
    # Find the first document
    first_doc = collection.find_one(sort=[('_id', 1)])
    assert first_doc is not None, "Database must have at least one document for this test to run."

    # Request the page for the first document
    response = client.get(f'/view/{first_doc["_id"]}')
    assert response.status_code == 200

    # Parse the HTML
    soup = BeautifulSoup(response.data, 'html.parser')

    # Find the navigation buttons
    first_button = soup.find('a', {'id': 'first-button'})
    previous_button = soup.find('a', {'id': 'previous-button'})
    next_button = soup.find('a', {'id': 'next-button'})

    # Assert that 'First' and 'Previous' are disabled
    assert 'disabled' in first_button.get('class', []), "First button should be disabled on the first page."
    assert 'disabled' in previous_button.get('class', []), "Previous button should be disabled on the first page."

    # Assert that 'Next' is not disabled (assuming more than one doc)
    if collection.count_documents({}) > 1:
        assert 'disabled' not in next_button.get('class', []), "Next button should be enabled on the first page if it's not the only document."

