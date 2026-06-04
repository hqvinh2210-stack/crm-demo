from datetime import datetime
from pydantic import BaseModel


class MessageBase(BaseModel):
    sender_id: int | None = None
    direction: str
    content: str


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: int
    conversation_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
