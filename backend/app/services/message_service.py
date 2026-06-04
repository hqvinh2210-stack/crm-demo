from datetime import datetime
from sqlalchemy.orm import Session

from app import models
from app.schemas.message_schema import MessageCreate


class MessageService:
    def __init__(self, db: Session):
        self.db = db

    def get_for_conversation(self, conversation_id: int):
        return (
            self.db.query(models.Message)
            .filter(models.Message.conversation_id == conversation_id)
            .order_by(models.Message.created_at)
            .all()
        )

    def create(self, conversation_id: int, message: MessageCreate):
        db_message = models.Message(
            conversation_id=conversation_id,
            sender_id=message.sender_id,
            direction=message.direction,
            content=message.content,
            created_at=datetime.utcnow(),
        )
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message
