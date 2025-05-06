import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.enums import ConversationStep, CategoryType

client = TestClient(app)

def test_chat_initial_message():
    # Send initial message
    response = client.post("/api/v1/chat", json={
        "user_id": "test_user",
        "message": "Air Travel"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["current_step"] == ConversationStep.GET_NAME
    assert "message" in data
    assert "collected_data" in data
    assert data["collected_data"]["category"] == "Air Travel"

def test_invalid_category():
    # Send invalid category
    response = client.post("/api/v1/chat", json={
        "user_id": "test_user",
        "message": "Invalid Category"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["current_step"] == ConversationStep.GREETING
    assert "Please select a valid category" in data["message"]

def test_complete_booking_flow():
    # Step 1: Select category
    response = client.post("/api/v1/chat", json={
        "user_id": "test_user",
        "message": "Air Travel"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["current_step"] == ConversationStep.GET_NAME
    
    # Step 2: Provide name
    response = client.post("/api/v1/chat", json={
        "user_id": "test_user",
        "message": "John Doe"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["current_step"] == ConversationStep.GET_EMAIL
    
    # Step 3: Provide email
    response = client.post("/api/v1/chat", json={
        "user_id": "test_user",
        "message": "john.doe@example.com"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["current_step"] == ConversationStep.GET_DESTINATION
    
    # Step 4: Provide destination
    response = client.post("/api/v1/chat", json={
        "user_id": "test_user",
        "message": "Paris"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["current_step"] == ConversationStep.GET_DATES
    
    # Step 5: Provide dates
    response = client.post("/api/v1/chat", json={
        "user_id": "test_user",
        "message": "2024-06-15 to 2024-06-22"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["current_step"] == ConversationStep.GET_TICKETS_COUNT
    
    # Step 6: Provide tickets count
    response = client.post("/api/v1/chat", json={
        "user_id": "test_user",
        "message": "2"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["current_step"] == ConversationStep.CONFIRM_BOOKING
    
    # Step 7: Confirm booking
    response = client.post("/api/v1/chat", json={
        "user_id": "test_user",
        "message": "yes"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["current_step"] == ConversationStep.COMPLETED
    assert "Thank you for your booking" in data["message"] 