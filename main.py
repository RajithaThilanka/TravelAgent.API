# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
import os
import uuid
from enum import Enum

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class CategoryType(str, Enum):
    BOOKING_CHANGES = "Booking Changes"
    AIR_TRAVEL = "Air Travel"
    PACKAGES = "Packages"
    STUDENT_INQUIRY = "Student Inquiry"
    PROMOTIONS = "Promotions"
    COMPLAINT = "Complaint"

class ConversationStep(str, Enum):
    GREETING = "greeting"
    GET_CATEGORY = "get_category"
    GET_NAME = "get_name"
    GET_EMAIL = "get_email"
    GET_DESTINATION = "get_destination"
    GET_DATES = "get_dates"
    GET_TICKETS_COUNT = "get_tickets_count"
    CONFIRM_BOOKING = "confirm_booking"
    COMPLETED = "completed"

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    message: str
    current_step: ConversationStep
    collected_data: Dict[str, Any]

# Sessions storage - in production, use a database
sessions = {}

# Step flow definition
step_flows = {
    CategoryType.BOOKING_CHANGES: [
        ConversationStep.GREETING,
        ConversationStep.GET_CATEGORY,
        ConversationStep.GET_NAME,
        ConversationStep.GET_EMAIL,
        ConversationStep.GET_DESTINATION,
        ConversationStep.GET_DATES,
        ConversationStep.CONFIRM_BOOKING,
        ConversationStep.COMPLETED
    ],
    CategoryType.AIR_TRAVEL: [
        ConversationStep.GREETING,
        ConversationStep.GET_CATEGORY,
        ConversationStep.GET_NAME,
        ConversationStep.GET_EMAIL,
        ConversationStep.GET_DESTINATION,
        ConversationStep.GET_DATES,
        ConversationStep.GET_TICKETS_COUNT,
        ConversationStep.CONFIRM_BOOKING,
        ConversationStep.COMPLETED
    ],
    CategoryType.PACKAGES: [
        ConversationStep.GREETING,
        ConversationStep.GET_CATEGORY,
        ConversationStep.GET_NAME,
        ConversationStep.GET_EMAIL,
        ConversationStep.GET_DESTINATION,
        ConversationStep.GET_DATES,
        ConversationStep.GET_TICKETS_COUNT,
        ConversationStep.CONFIRM_BOOKING,
        ConversationStep.COMPLETED
    ],
    CategoryType.STUDENT_INQUIRY: [
        ConversationStep.GREETING,
        ConversationStep.GET_CATEGORY,
        ConversationStep.GET_NAME,
        ConversationStep.GET_EMAIL,
        ConversationStep.GET_DESTINATION,
        ConversationStep.COMPLETED
    ],
    CategoryType.PROMOTIONS: [
        ConversationStep.GREETING,
        ConversationStep.GET_CATEGORY,
        ConversationStep.GET_EMAIL,
        ConversationStep.COMPLETED
    ],
    CategoryType.COMPLAINT: [
        ConversationStep.GREETING,
        ConversationStep.GET_CATEGORY,
        ConversationStep.GET_NAME,
        ConversationStep.GET_EMAIL,
        ConversationStep.COMPLETED
    ]
}

# Initialize LLM
llm = ChatOpenAI()

def get_next_step(category, current_step):
    if category not in step_flows:
        return ConversationStep.GREETING
    
    flow = step_flows[category]
    try:
        current_index = flow.index(current_step)
        if current_index + 1 < len(flow):
            return flow[current_index + 1]
        return ConversationStep.COMPLETED
    except ValueError:
        return flow[0]

def process_user_input(step, user_input, collected_data):
    """Process user input based on current conversation step"""
    if step == ConversationStep.GET_CATEGORY:
        try:
            category = CategoryType(user_input)
            return {"category": category}, True
        except ValueError:
            return {}, False
            
    elif step == ConversationStep.GET_NAME:
        if len(user_input) > 1:
            return {"name": user_input}, True
        return {}, False
        
    elif step == ConversationStep.GET_EMAIL:
        if "@" in user_input and "." in user_input:
            return {"email": user_input}, True
        return {}, False
        
    elif step == ConversationStep.GET_DESTINATION:
        if len(user_input) > 1:
            return {"destination": user_input}, True
        return {}, False
        
    elif step == ConversationStep.GET_DATES:
        return {"travel_dates": user_input}, True
        
    elif step == ConversationStep.GET_TICKETS_COUNT:
        try:
            tickets = int(user_input)
            return {"tickets_count": tickets}, True
        except ValueError:
            return {}, False
            
    elif step == ConversationStep.CONFIRM_BOOKING:
        if user_input.lower() in ["yes", "confirm", "ok", "sure"]:
            return {"confirmed": True}, True
        elif user_input.lower() in ["no", "cancel"]:
            return {"confirmed": False}, True
        return {}, False
        
    return {}, True

def get_response_message(step, collected_data):
    """Generate appropriate response message based on step"""
    if step == ConversationStep.GREETING:
        return "Welcome! How can I help you today? Choose from: Booking Changes, Air Travel, Packages, Student Inquiry, Promotions, or Complaint."
    
    elif step == ConversationStep.GET_CATEGORY:
        return f"Got it! What's your full name?"
    
    elif step == ConversationStep.GET_NAME:
        return f"Thank you, {collected_data.get('name')}. Could you provide your email address for contact purposes?"
    
    elif step == ConversationStep.GET_EMAIL:
        return "Got your email. What's your destination?"
    
    elif step == ConversationStep.GET_DESTINATION:
        return f"Great choice! When are you planning to travel?"
    
    elif step == ConversationStep.GET_DATES:
        return "How many tickets would you like to book?"
    
    elif step == ConversationStep.GET_TICKETS_COUNT:
        return f"Confirm your booking: \nName: {collected_data.get('name')}\nEmail: {collected_data.get('email')}\nDestination: {collected_data.get('destination')}\nDates: {collected_data.get('travel_dates')}\nTickets: {collected_data.get('tickets_count')}\n\nType 'yes' to confirm or 'no' to cancel."
    
    elif step == ConversationStep.CONFIRM_BOOKING:
        if collected_data.get('confirmed', False):
            return "Thank you for your booking! Your request has been processed successfully. You will receive a confirmation email shortly."
        else:
            return "Your booking has been cancelled. Please start a new chat if you'd like to make different arrangements."
    
    elif step == ConversationStep.COMPLETED:
        category = collected_data.get('category')
        if category == CategoryType.PROMOTIONS:
            return "Thank you! We'll send our latest promotions to your email address."
        elif category == CategoryType.STUDENT_INQUIRY:
            return f"Thank you for your student inquiry about {collected_data.get('destination')}. We'll send information about student packages to your email."
        elif category == CategoryType.COMPLAINT:
            return "We've received your complaint and will contact you soon to resolve the issue."
        else:
            return "Thank you for using our service! Is there anything else we can help you with?"
    
    return "I'm not sure how to proceed. Could you please restart the conversation?"

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    user_id = request.user_id
    user_message = request.message
    
 # Create new session if it doesn't exist
    if user_id not in sessions:
        sessions[user_id] = {
            "current_step": ConversationStep.GET_CATEGORY,  
            "collected_data": {},
            "memory": ConversationBufferMemory()
        }
        return ChatResponse(
            message="Welcome to our Travel Assistant! How can I help you today? Please select from: Booking Changes, Air Travel, Packages, Student Inquiry, Promotions, or Complaint.",
            current_step=ConversationStep.GET_CATEGORY,  
            collected_data={}
        )
    session = sessions[user_id]
    current_step = session["current_step"]
    collected_data = session["collected_data"]
    
    # Process user input based on current step
    if current_step != ConversationStep.GREETING:
        new_data, is_valid = process_user_input(current_step, user_message, collected_data)
        
        if not is_valid:
            return ChatResponse(
                message="Sorry, that doesn't seem right. " + get_response_message(current_step, collected_data),
                current_step=current_step,
                collected_data=collected_data
            )
        
        # Update collected data
        collected_data.update(new_data)
    
    # Determine next step
    category = collected_data.get("category")
    next_step = get_next_step(category, current_step)
    session["current_step"] = next_step
    
    # Generate response for the next step
    response_message = get_response_message(next_step, collected_data)
    
    return ChatResponse(
        message=response_message,
        current_step=next_step,
        collected_data=collected_data
    )

@app.post("/start_chat")
async def start_chat():
    """Endpoint to start a new chat session"""
    user_id = str(uuid.uuid4())
    sessions[user_id] = {
        "current_step": ConversationStep.GREETING,
        "collected_data": {},
        "memory": ConversationBufferMemory()
    }
    
    return {
        "user_id": user_id,
        "message": get_response_message(ConversationStep.GREETING, {}),
        "current_step": ConversationStep.GET_CATEGORY
    }

# Start the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)