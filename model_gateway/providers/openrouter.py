import httpx
from model_gateway.exceptions import (
    AuthenticationError,
    ProviderUnavailableError,
    RateLimitError,
)
from model_gateway.providers.base import AbstractProviderAdapter
from shared.schemas.models import ModelRequest, ModelResponse, ProviderType, TokenUsage
from shared.utilities.logger import get_logger

logger = get_logger("model_gateway.providers.openrouter")


class OpenRouterProvider(AbstractProviderAdapter):
    """
    Adapter for the OpenRouter API (multi-model aggregation & reasoning support).
    """

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, api_key: str | None = None):
        super().__init__(api_key=api_key)

    @property
    def provider_type(self) -> ProviderType:
        return ProviderType.OPENROUTER

    @property
    def default_model(self) -> str:
        return "liquid/lfm-3-1.7b:free"

    async def _perform_completion(self, request: ModelRequest) -> ModelResponse:
        if not self._api_key:
            raise AuthenticationError("OpenRouter API key is missing or not configured.")

        model = request.model or self.default_model
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ai-software-factory.local",
            "X-Title": "AI Software Factory",
        }

        formatted_messages = []
        for m in request.messages:
            msg_dict = {"role": m.role.value, "content": m.content}
            if m.reasoning_details is not None:
                msg_dict["reasoning_details"] = m.reasoning_details
            formatted_messages.append(msg_dict)

        payload = {
            "model": model,
            "messages": formatted_messages,
            "temperature": request.temperature,
        }
        if request.enable_reasoning:
            payload["reasoning"] = {"enabled": True}
        if request.max_tokens:
            payload["max_tokens"] = request.max_tokens

        try:
            async with httpx.AsyncClient(timeout=request.timeout_seconds) as client:
                res = await client.post(self.BASE_URL, headers=headers, json=payload)

            if res.status_code == 401:
                raise AuthenticationError("Invalid OpenRouter API Key.")
            if res.status_code == 429:
                raise RateLimitError("OpenRouter rate limit exceeded or credit limit reached.")
            if res.status_code >= 500:
                raise ProviderUnavailableError(f"OpenRouter server error: {res.status_code}")

            res.raise_for_status()
            data = res.json()
            choice = data["choices"][0]["message"]
            raw_usage = data.get("usage", {})

            return ModelResponse(
                content=choice.get("content", ""),
                model_name=model,
                provider=self.provider_type,
                reasoning_details=choice.get("reasoning_details"),
                usage=TokenUsage(
                    prompt_tokens=raw_usage.get("prompt_tokens", 0),
                    completion_tokens=raw_usage.get("completion_tokens", 0),
                    reasoning_tokens=raw_usage.get("reasoning_tokens", 0),
                    total_tokens=raw_usage.get("total_tokens", 0),
                ),
            )
        except httpx.TimeoutException as exc:
            raise ProviderUnavailableError(f"OpenRouter request timed out: {exc}") from exc
        except httpx.RequestError as exc:
            raise ProviderUnavailableError(f"Network error calling OpenRouter: {exc}") from exc
