from sqlalchemy.orm import Session

from app import models
from app.schemas.conversation_schema import ConversationCreate


class ConversationService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(models.Conversation).all()

    def get_by_id(self, conversation_id: int):
        return self.db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()

    def create(self, conversation: ConversationCreate):
        db_conversation = models.Conversation(**conversation.model_dump())
        self.db.add(db_conversation)
        self.db.commit()
        self.db.refresh(db_conversation)
        return db_conversation
