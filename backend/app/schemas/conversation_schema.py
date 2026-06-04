from pydantic import BaseModel


class ConversationBase(BaseModel):
    customer_id: int
    channel_id: int | None = None
    assigned_to: int | None = None
    subject: str | None = None


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: int

    model_config = {
        "from_attributes": True,
    }
