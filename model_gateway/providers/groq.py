import httpx
from model_gateway.exceptions import (
    AuthenticationError,
    ProviderUnavailableError,
    RateLimitError,
)
from model_gateway.providers.base import AbstractProviderAdapter
from shared.schemas.models import ModelRequest, ModelResponse, ProviderType, TokenUsage
from shared.utilities.logger import get_logger

logger = get_logger("model_gateway.providers.groq")


class GroqProvider(AbstractProviderAdapter):
    """
    Adapter for the Groq API (low-latency inference).
    """

    BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

    def __init__(self, api_key: str | None = None):
        super().__init__(api_key=api_key)

    @property
    def provider_type(self) -> ProviderType:
        return ProviderType.GROQ

    @property
    def default_model(self) -> str:
        return "llama-3.3-70b-versatile"

    async def _perform_completion(self, request: ModelRequest) -> ModelResponse:
        if not self._api_key:
            raise AuthenticationError("Groq API key is missing or not configured.")

        model = request.model or self.default_model
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model,
            "messages": [
                {"role": m.role.value, "content": m.content}
                for m in request.messages
            ],
            "temperature": request.temperature,
        }
        if request.max_tokens:
            payload["max_tokens"] = request.max_tokens

        try:
            async with httpx.AsyncClient(timeout=request.timeout_seconds) as client:
                res = await client.post(self.BASE_URL, headers=headers, json=payload)

            if res.status_code == 401:
                raise AuthenticationError("Invalid Groq API Key.")
            if res.status_code == 429:
                raise RateLimitError("Groq rate limit exceeded.")
            if res.status_code >= 500:
                raise ProviderUnavailableError(f"Groq server error: {res.status_code} - {res.text}")

            res.raise_for_status()
            data = res.json()
            choice = data["choices"][0]["message"]
            raw_usage = data.get("usage", {})

            return ModelResponse(
                content=choice.get("content", ""),
                model_name=model,
                provider=self.provider_type,
                usage=TokenUsage(
                    prompt_tokens=raw_usage.get("prompt_tokens", 0),
                    completion_tokens=raw_usage.get("completion_tokens", 0),
                    total_tokens=raw_usage.get("total_tokens", 0),
                ),
            )
        except httpx.TimeoutException as exc:
            raise ProviderUnavailableError(f"Groq request timed out: {exc}") from exc
        except httpx.RequestError as exc:
            raise ProviderUnavailableError(f"Network error calling Groq: {exc}") from exc
