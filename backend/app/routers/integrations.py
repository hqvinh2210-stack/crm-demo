from fastapi import APIRouter, HTTPException

from app.services.webhook_service import WebhookService

router = APIRouter(prefix="/integrations", tags=["integrations"])


@router.post("/{provider}/incoming")
def incoming_provider_webhook(provider: str, payload: dict):
    try:
        event = WebhookService().process_incoming(provider, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"status": "đã nhận", "event": event}
