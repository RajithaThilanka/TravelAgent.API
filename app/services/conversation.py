from typing import Dict, Any, Tuple
from ..models.enums import ConversationStep, CategoryType
from langchain.memory import ConversationBufferMemory

# Step flow definition
step_flows = {
    CategoryType.BOOKING_CHANGES: [
        ConversationStep.GET_CATEGORY,
        ConversationStep.GET_NAME,
        ConversationStep.GET_EMAIL,
        ConversationStep.GET_DESTINATION,
        ConversationStep.GET_DATES,
        ConversationStep.CONFIRM_BOOKING,
        ConversationStep.COMPLETED
    ],
    CategoryType.AIR_TRAVEL: [
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
        ConversationStep.GET_CATEGORY,
        ConversationStep.GET_NAME,
        ConversationStep.GET_EMAIL,
        ConversationStep.GET_DESTINATION,
        ConversationStep.COMPLETED
    ],
    CategoryType.PROMOTIONS: [
        ConversationStep.GET_CATEGORY,
        ConversationStep.GET_EMAIL,
        ConversationStep.COMPLETED
    ],
    CategoryType.COMPLAINT: [
        ConversationStep.GET_CATEGORY,
        ConversationStep.GET_NAME,
        ConversationStep.GET_EMAIL,
        ConversationStep.COMPLETED
    ]
}

def get_next_step(category: CategoryType, current_step: ConversationStep) -> ConversationStep:
    if category not in step_flows:
        return ConversationStep.GET_CATEGORY
    
    flow = step_flows[category]
    try:
        current_index = flow.index(current_step)
        if current_index + 1 < len(flow):
            return flow[current_index + 1]
        return ConversationStep.COMPLETED
    except ValueError:
        return flow[0]

def process_user_input(step: ConversationStep, user_input: str, collected_data: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
    """Process user input based on current conversation step"""
    if step == ConversationStep.GET_CATEGORY:
        try:
            category = CategoryType(user_input)
            return {"category": category}, True
        except ValueError:
            return {}, False
            
    elif step == ConversationStep.GET_NAME:
        # Do not accept emails as names
        if len(user_input) > 1 and ("@" not in user_input and ".com" not in user_input and ".net" not in user_input and ".org" not in user_input):
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

def get_response_message(step: ConversationStep, collected_data: Dict[str, Any]) -> str:
    """Generate appropriate response message based on step"""
    if step == ConversationStep.GET_CATEGORY:
        return "Welcome! How can I help you today? Choose from: Booking Changes, Air Travel, Packages, Student Inquiry, Promotions, or Complaint."
    
    elif step == ConversationStep.GET_NAME:
        return "Could you please provide your full name?"
    
    elif step == ConversationStep.GET_EMAIL:
        return "Got your name! Now, could you provide your email address for contact purposes?"
    
    elif step == ConversationStep.GET_DESTINATION:
         return f"Great! What is your destination?"
    
    elif step == ConversationStep.GET_DATES:
        return "When are you planning to travel?"
    
    elif step == ConversationStep.GET_TICKETS_COUNT:
        return "How many tickets would you like to book?"
    
    elif step == ConversationStep.CONFIRM_BOOKING:
        return f"Confirm your booking details: \nName: {collected_data.get('name')}\nEmail: {collected_data.get('email')}\nDestination: {collected_data.get('destination')}\nDates: {collected_data.get('travel_dates')}\nTickets: {collected_data.get('tickets_count')}\n\nType 'yes' to confirm or 'no' to cancel."

    
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