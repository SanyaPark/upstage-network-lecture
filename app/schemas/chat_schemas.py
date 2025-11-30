from pydantic import BaseModel
from typing import List
from datetime import datetime


class MessageCreateRequest(BaseModel):
    user_id: int
    message: str


class ChatTransactionRequest(BaseModel):
    user_id: int
    user_message: str
    assistant_message: str


class ConversationResponse(BaseModel):
    id: int
    user_id: int
    role: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    message: str