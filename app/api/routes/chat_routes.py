from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.service.chat_service import ChatService
from app.dependencies import get_chat_service
from app.schemas.chat_schemas import (
    MessageCreateRequest,
    ChatTransactionRequest,
    ConversationResponse,
    ChatResponse
)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/user-message", response_model=ChatResponse)
async def add_user_message_api(
    message_data: MessageCreateRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    try:
        chat_service.add_user_message(message_data.user_id, message_data.message)
        return ChatResponse(message="User message added successfully")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/assistant-message", response_model=ChatResponse)
async def add_assistant_message_api(
    message_data: MessageCreateRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    try:
        chat_service.add_assistant_message(message_data.user_id, message_data.message)
        return ChatResponse(message="Assistant message added successfully")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{user_id}/conversations", response_model=List[ConversationResponse])
async def get_conversations_api(
    user_id: int, 
    limit: int = 20,
    chat_service: ChatService = Depends(get_chat_service)
):
    try:
        conversations = chat_service.get_recent_conversations(user_id, limit)
        return conversations or []
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/transaction", response_model=ChatResponse)
async def save_chat_transaction_api(
    transaction: ChatTransactionRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    try:
        chat_service.save_chat_transaction(
            transaction.user_id,
            transaction.user_message,
            transaction.assistant_message
        )
        return ChatResponse(message="Chat transaction saved successfully")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")