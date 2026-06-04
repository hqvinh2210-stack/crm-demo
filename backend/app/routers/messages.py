from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.message_schema import MessageCreate, MessageRead
from app.services.message_service import MessageService

router = APIRouter()


@router.get("/conversation/{conversation_id}", response_model=List[MessageRead])
def get_messages(conversation_id: int, db: Session = Depends(get_db)):
    return MessageService(db).get_for_conversation(conversation_id)


@router.post("/conversation/{conversation_id}", response_model=MessageRead)
def send_message(conversation_id: int, message: MessageCreate, db: Session = Depends(get_db)):
    return MessageService(db).create(conversation_id, message)
