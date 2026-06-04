import json

import redis

from app.config import settings

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


class RedisService:
    def __init__(self):
        self.client = redis_client

    def cache_summary(self, conversation_id: int, summary: str):
        return self.client.hset(f"conversation:{conversation_id}", "summary", summary)

    def get_summary(self, conversation_id: int):
        return self.client.hget(f"conversation:{conversation_id}", "summary")

    def cache_suggestion(self, conversation_id: int, suggestion: str):
        return self.client.hset(f"conversation:{conversation_id}", "suggestion", suggestion)

    def get_suggestion(self, conversation_id: int):
        return self.client.hget(f"conversation:{conversation_id}", "suggestion")

    def enqueue_event(self, event: dict):
        payload = json.dumps(event, default=str)
        return self.client.lpush("crm:events:incoming", payload)
