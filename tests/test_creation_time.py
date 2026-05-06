import pytest
from bs4 import BeautifulSoup
from pymongo import MongoClient
import os

def get_db_collection():
    """Helper to connect to the test DB."""
    mongodb_uri = os.environ.get('MONGODB_URI')
    client = MongoClient(mongodb_uri)
    db = client["ama_browser"]
    collection = db["ama_log"]
    return collection

def test_creation_time_display_in_views(client):
    """
    Tests if the creation time is correctly displayed in the 'Question Abstraction', 'Answer', and 'Tags' views.
    """
    collection = get_db_collection()
    doc = collection.find_one()
    assert doc is not None, "Database must have at least one document for this test."

    views = ['question_abstraction', 'answer', 'tags']

    for view in views:
        response = client.get(f'/view/{doc["_id"]}?show={view}')
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Look for the string "Erstellt am:"
        content = soup.get_text()
        assert "Erstellt am:" in content, f"Creation time label 'Erstellt am:' missing in {view} view."
        
        # Verify the date format (very basic check for DD.MM.YYYY)
        import re
        date_pattern = re.compile(r'\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}')
        assert date_pattern.search(content), f"Creation time date/time format missing or incorrect in {view} view."
