class ZaloService:
    def send_message(self, recipient_id: str, text: str):
        return {
            "channel": "zalo",
            "recipient_id": recipient_id,
            "message": text,
            "status": "queued",
        }
