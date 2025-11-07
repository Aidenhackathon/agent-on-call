import pytest
from fastapi.testclient import TestClient
from main import app
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

client = TestClient(app)

def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_create_ticket():
    """Test creating a ticket."""
    ticket_data = {
        "title": "Test Ticket",
        "description": "Email service not working",
        "category": "Technical"
    }
    response = client.post("/tickets", json=ticket_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == ticket_data["title"]
    assert "id" in data
    return data["id"]

def test_list_tickets():
    """Test listing tickets."""
    response = client.get("/tickets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_and_triage_ticket():
    """Smoke test: Create a ticket and run triage."""
    # Create ticket
    ticket_data = {
        "title": "Website is down",
        "description": "Customer cannot access dashboard",
        "category": "Critical"
    }
    create_response = client.post("/tickets", json=ticket_data)
    assert create_response.status_code == 201
    ticket = create_response.json()
    ticket_id = ticket["id"]
    
    # Run triage
    triage_response = client.post(f"/tickets/{ticket_id}/triage")
    if triage_response.status_code != 200:
        print(f"Triage failed with status {triage_response.status_code}")
        print(f"Response: {triage_response.text}")
    assert triage_response.status_code == 200
    triage_data = triage_response.json()
    
    # Verify triage data
    assert "priority" in triage_data
    assert "confidence" in triage_data
    assert "assignee" in triage_data
    assert "rationale" in triage_data
    assert "reply_draft" in triage_data
    assert triage_data["priority"] in ["P0", "P1", "P2", "P3"]
    assert 0 <= triage_data["confidence"] <= 1
    
    # Verify ticket was updated
    get_response = client.get(f"/tickets/{ticket_id}")
    assert get_response.status_code == 200
    updated_ticket = get_response.json()
    assert updated_ticket["priority"] == triage_data["priority"]
    assert updated_ticket["assignee"] == triage_data["assignee"]
    
    print("Smoke test passed: Ticket created, triaged, and persisted successfully")

def test_update_ticket():
    """Test updating a ticket."""
    # Create ticket first
    ticket_data = {
        "title": "Test Update",
        "description": "Testing update functionality",
        "category": "Test"
    }
    create_response = client.post("/tickets", json=ticket_data)
    ticket_id = create_response.json()["id"]
    
    # Update ticket
    update_data = {
        "status": "in-progress",
        "ai_reply_draft": "Updated reply draft"
    }
    update_response = client.put(f"/tickets/{ticket_id}", json=update_data)
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["status"] == "in-progress"

def test_delete_ticket():
    """Test deleting a ticket."""
    # Create ticket first
    ticket_data = {
        "title": "Test Delete",
        "description": "Testing delete functionality",
        "category": "Test"
    }
    create_response = client.post("/tickets", json=ticket_data)
    ticket_id = create_response.json()["id"]
    
    # Delete ticket
    delete_response = client.delete(f"/tickets/{ticket_id}")
    assert delete_response.status_code == 204
    
    # Verify ticket is deleted
    get_response = client.get(f"/tickets/{ticket_id}")
    assert get_response.status_code == 404
