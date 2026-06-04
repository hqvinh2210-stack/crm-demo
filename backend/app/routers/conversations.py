from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.conversation_schema import ConversationCreate, ConversationRead
from app.services.conversation_service import ConversationService

router = APIRouter()


@router.get("/", response_model=List[ConversationRead])
def list_conversations(db: Session = Depends(get_db)):
    return ConversationService(db).get_all()


@router.post("/", response_model=ConversationRead)
def create_conversation(conversation: ConversationCreate, db: Session = Depends(get_db)):
    return ConversationService(db).create(conversation)


@router.get("/{conversation_id}", response_model=ConversationRead)
def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conversation = ConversationService(db).get_by_id(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Không tìm thấy cuộc trò chuyện")
    return conversation
