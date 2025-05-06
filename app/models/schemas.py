from pydantic import BaseModel
from typing import Dict, Any
from .enums import ConversationStep

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    message: str
    current_step: ConversationStep
    collected_data: Dict[str, Any] 