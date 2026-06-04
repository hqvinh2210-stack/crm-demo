class MessengerService:
    def send_message(self, recipient_id: str, text: str):
        return {
            "channel": "messenger",
            "recipient_id": recipient_id,
            "message": text,
            "status": "queued",
        }
