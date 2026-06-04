from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/incoming")
def incoming_webhook(payload: dict):
    if not payload:
        raise HTTPException(status_code=400, detail="Yêu cầu payload")
    return {"status": "đã nhận", "payload": payload}
