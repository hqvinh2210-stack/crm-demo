from typing import List

from app.config import settings
from app.services.redis_service import RedisService

try:
    import openai
except ImportError:  # pragma: no cover
    openai = None


class AIAgentService:
    def __init__(self):
        self.redis = RedisService()
        if settings.OPENAI_API_KEY and openai:
            openai.api_key = settings.OPENAI_API_KEY

    def summarize_conversation(self, messages: List[dict]) -> str:
        cached = self.redis.get_summary(messages[0].get("conversation_id") if messages else 0)
        if cached:
            return cached

        if settings.OPENAI_API_KEY and openai:
            prompt = self._build_summary_prompt(messages)
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": "Tóm tắt hội thoại CRM."}, {"role": "user", "content": prompt}],
                    max_tokens=256,
                )
                summary = response.choices[0].message.content.strip()
            except Exception:
                summary = self._simple_summary(messages)
        else:
            summary = self._simple_summary(messages)

        if messages:
            conversation_id = messages[0].get("conversation_id")
            self.redis.cache_summary(conversation_id, summary)

        return summary

    def suggest_reply(self, messages: List[dict]) -> str:
        cached = self.redis.get_suggestion(messages[0].get("conversation_id") if messages else 0)
        if cached:
            return cached

        if settings.OPENAI_API_KEY and openai:
            prompt = self._build_suggestion_prompt(messages)
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": "Gợi ý trả lời khách hàng chuyên nghiệp."}, {"role": "user", "content": prompt}],
                    max_tokens=256,
                )
                suggestion = response.choices[0].message.content.strip()
            except Exception:
                suggestion = self._simple_suggestion(messages)
        else:
            suggestion = self._simple_suggestion(messages)

        if messages:
            conversation_id = messages[0].get("conversation_id")
            self.redis.cache_suggestion(conversation_id, suggestion)

        return suggestion

    def classify_customer(self, customer: dict) -> str:
        if settings.OPENAI_API_KEY and openai:
            prompt = self._build_classification_prompt(customer)
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": "Phân loại khách hàng CRM."}, {"role": "user", "content": prompt}],
                    max_tokens=64,
                )
                return response.choices[0].message.content.strip()
            except Exception:
                return self._simple_classification(customer)
        return self._simple_classification(customer)

    def _simple_summary(self, messages: List[dict]) -> str:
        if not messages:
            return "Không có nội dung hội thoại." 
        latest = messages[-1]["content"]
        return f"Hội thoại có {len(messages)} tin nhắn. Tin nhắn cuối: {latest[:120]}"

    def _simple_suggestion(self, messages: List[dict]) -> str:
        if not messages:
            return "Chưa có tin nhắn nào để gợi ý trả lời."
        last = messages[-1]["content"]
        return f"Bạn có thể trả lời: Cảm ơn bạn đã liên hệ. Về vấn đề '{last[:80]}', chúng tôi sẽ hỗ trợ sớm nhất."

    def _simple_classification(self, customer: dict) -> str:
        if not customer:
            return "Khách hàng chưa xác định"
        if customer.get("notes"):
            return "Khách hàng tiềm năng"
        return "Khách hàng mới"

    def _build_summary_prompt(self, messages: List[dict]) -> str:
        return "\n".join(f"{m.get('direction', 'in')} - {m.get('content', '')}" for m in messages)

    def _build_suggestion_prompt(self, messages: List[dict]) -> str:
        return "\n".join(f"{m.get('direction', 'in')} - {m.get('content', '')}" for m in messages)

    def _build_classification_prompt(self, customer: dict) -> str:
        return f"Tên: {customer.get('name')}\nEmail: {customer.get('email')}\nSố điện thoại: {customer.get('phone')}\nGhi chú: {customer.get('notes')}"
