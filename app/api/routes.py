from fastapi import APIRouter, HTTPException
from ..models.schemas import ChatRequest, ChatResponse
from ..models.enums import ConversationStep, CategoryType
from ..services.conversation import process_user_input, get_response_message, get_next_step
from langchain.memory import ConversationBufferMemory

router = APIRouter()

# Sessions storage - in production, use a database
sessions = {}

@router.post("/chat", response_model=ChatResponse)
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
        
    session = sessions[user_id]
    current_step = session["current_step"]
    collected_data = session["collected_data"]
    
    # Process user input based on current step
    if current_step != ConversationStep.GET_CATEGORY:
        new_data, is_valid = process_user_input(current_step, user_message, collected_data)
        
        if not is_valid:
            return ChatResponse(
                message="Sorry, that doesn't seem right. " + get_response_message(current_step, collected_data),
                current_step=current_step,
                collected_data=collected_data
            )
        
        # Update collected data
        collected_data.update(new_data)
        
        # Get next step
        category = collected_data.get('category')
        next_step = get_next_step(category, current_step)
        session["current_step"] = next_step
        
        # Generate response message
        response_message = get_response_message(next_step, collected_data)
        
        return ChatResponse(
            message=response_message,
            current_step=next_step,
            collected_data=collected_data
        )
    
    # Handle category selection step
    try:
        category = CategoryType(user_message)
        collected_data["category"] = category
        next_step = get_next_step(category, current_step)
        session["current_step"] = next_step
        
        response_message = get_response_message(next_step, collected_data)
        
        return ChatResponse(
            message=response_message,
            current_step=next_step,
            collected_data=collected_data
        )
    except ValueError:
        return ChatResponse(
            message="Please select a valid category: Booking Changes, Air Travel, Packages, Student Inquiry, Promotions, or Complaint.",
            current_step=current_step,
            collected_data=collected_data
        ) 