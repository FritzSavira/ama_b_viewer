import pytest
from bs4 import BeautifulSoup

# This uses the 'client' fixture from conftest.py

def test_dashboard_links_are_present_and_active(client):
    """
    Tests if the dashboard links are present in the navigation and that they become active when their page is visited.
    """
    dashboard_pages = [
        ("/questions_dashboard", "questions_dashboard"),
        ("/tags_dashboard", "tags_dashboard"),
        ("/network_graph_view", "network_graph_view"),
    ]

    for url, active_page_id in dashboard_pages:
        response = client.get(url)
        assert response.status_code == 200
        soup = BeautifulSoup(response.data, 'html.parser')

        all_nav_links = soup.select('.tab-nav a')
        assert len(all_nav_links) > 0, "Navigation links should be present."

        found_active_link = False
        for link in all_nav_links:
            href = link.get('href', '')
            classes = link.get('class', [])

            # Check if the current link is the one that should be active
            if href == url:
                assert 'active' in classes, f"Link to {url} should be active on its own page."
                found_active_link = True
            else:
                # Any other link should not be active
                assert 'active' not in classes, f"Link {href} should NOT be active on page {url}."
        
        assert found_active_link, f"An active link for the current page {url} was not found."
