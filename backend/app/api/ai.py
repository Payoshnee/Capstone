from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from app.schemas.common import APIResponse, APIError
from app.services.ai_service import ai_service

router = APIRouter()

class ChatMessage(BaseModel):
    sender: str
    content: str
    sender_name: Optional[str] = None

class InterviewChatRequest(BaseModel):
    messages: List[ChatMessage]
    target_role: Optional[str] = "Software Engineer"
    job_description: Optional[str] = None

class InterviewChatResponse(BaseModel):
    reply: str
    sender: str = "ai"
    sender_name: str = "AI Proctor (AURA)"

@router.post("/interview/chat", response_model=APIResponse[InterviewChatResponse])
async def interview_chat(payload: InterviewChatRequest):
    try:
        dict_messages = [
            {"role": "assistant" if m.sender == "ai" else "user", "content": m.content, "sender": m.sender}
            for m in payload.messages
        ]
        reply = ai_service.generate_interview_reply(
            messages=dict_messages,
            target_role=payload.target_role or "Software Engineer",
            job_description=payload.job_description
        )
        return APIResponse(data=InterviewChatResponse(reply=reply))
    except Exception as e:
        return APIResponse(error=APIError(message=str(e)))
