from datetime import datetime

from app.services.redis_service import RedisService


class WebhookService:
    def __init__(self):
        self.redis = RedisService()

    def normalize_payload(self, provider: str, payload: dict) -> dict:
        provider = provider.lower()
        converters = {
            "messenger": self._normalize_messenger,
            "instagram": self._normalize_instagram,
            "zalo": self._normalize_zalo,
            "tiktok": self._normalize_tiktok,
            "shopee": self._normalize_shopee,
        }
        if provider not in converters:
            raise ValueError(f"Provider '{provider}' không được hỗ trợ")

        event = converters[provider](payload)
        event["provider"] = provider
        event["received_at"] = datetime.utcnow().isoformat() + "Z"
        return event

    def process_incoming(self, provider: str, payload: dict) -> dict:
        event = self.normalize_payload(provider, payload)
        self.redis.enqueue_event(event)
        return event

    def _normalize_messenger(self, payload: dict) -> dict:
        return {
            "external_id": payload.get("sender_id") or payload.get("sender") or payload.get("from"),
            "thread_id": payload.get("thread_id") or payload.get("conversation_id"),
            "message": payload.get("message") or payload.get("text") or payload.get("body"),
            "metadata": payload.get("metadata", {}),
        }

    def _normalize_instagram(self, payload: dict) -> dict:
        return {
            "external_id": payload.get("sender_id") or payload.get("user_id") or payload.get("from"),
            "thread_id": payload.get("thread_id") or payload.get("conversation_id"),
            "message": payload.get("message") or payload.get("text") or payload.get("body"),
            "metadata": payload.get("metadata", {}),
        }

    def _normalize_zalo(self, payload: dict) -> dict:
        return {
            "external_id": payload.get("user_id") or payload.get("from"),
            "thread_id": payload.get("conversation_id") or payload.get("thread_id"),
            "message": payload.get("content") or payload.get("message") or payload.get("text"),
            "metadata": payload.get("metadata", {}),
        }

    def _normalize_tiktok(self, payload: dict) -> dict:
        return {
            "external_id": payload.get("user_id") or payload.get("from"),
            "thread_id": payload.get("conversation_id") or payload.get("thread_id"),
            "message": payload.get("message") or payload.get("text") or payload.get("body"),
            "metadata": payload.get("metadata", {}),
        }

    def _normalize_shopee(self, payload: dict) -> dict:
        return {
            "external_id": payload.get("user_id") or payload.get("sender_id") or payload.get("from"),
            "thread_id": payload.get("conversation_id") or payload.get("thread_id"),
            "message": payload.get("message") or payload.get("text") or payload.get("body"),
            "metadata": payload.get("metadata", {}),
        }
