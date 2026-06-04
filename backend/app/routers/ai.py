from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.ai_agent_service import AIAgentService
from app.services.conversation_service import ConversationService
from app.services.customer_service import CustomerService
from app.services.message_service import MessageService

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/summary/{conversation_id}")
def conversation_summary(conversation_id: int, db: Session = Depends(get_db)):
    conversation = ConversationService(db).get_by_id(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Không tìm thấy cuộc trò chuyện")

    messages = MessageService(db).get_for_conversation(conversation_id)
    payload = [
        {
            "conversation_id": conversation_id,
            "direction": message.direction,
            "content": message.content,
        }
        for message in messages
    ]
    summary = AIAgentService().summarize_conversation(payload)
    return {"conversation_id": conversation_id, "summary": summary}


@router.get("/suggest/{conversation_id}")
def suggest_reply(conversation_id: int, db: Session = Depends(get_db)):
    conversation = ConversationService(db).get_by_id(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Không tìm thấy cuộc trò chuyện")

    messages = MessageService(db).get_for_conversation(conversation_id)
    payload = [
        {
            "conversation_id": conversation_id,
            "direction": message.direction,
            "content": message.content,
        }
        for message in messages
    ]
    suggestion = AIAgentService().suggest_reply(payload)
    return {"conversation_id": conversation_id, "suggestion": suggestion}


@router.get("/classify-customer/{customer_id}")
def classify_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = CustomerService(db).get_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Không tìm thấy khách hàng")

    data = {
        "name": customer.name,
        "email": customer.email,
        "phone": customer.phone,
        "notes": customer.notes,
    }
    classification = AIAgentService().classify_customer(data)
    return {"customer_id": customer_id, "classification": classification}
