import httpx
from model_gateway.exceptions import (
    AuthenticationError,
    ProviderUnavailableError,
    RateLimitError,
)
from model_gateway.providers.base import AbstractProviderAdapter
from shared.schemas.models import ModelRequest, ModelResponse, ProviderType, TokenUsage
from shared.utilities.logger import get_logger

logger = get_logger("model_gateway.providers.gemini")


class GeminiProvider(AbstractProviderAdapter):
    """
    Adapter for Google Gemini API.
    """

    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"

    def __init__(self, api_key: str | None = None):
        super().__init__(api_key=api_key)

    @property
    def provider_type(self) -> ProviderType:
        return ProviderType.GEMINI

    @property
    def default_model(self) -> str:
        return "gemini-2.5-flash"

    async def _perform_completion(self, request: ModelRequest) -> ModelResponse:
        if not self._api_key:
            raise AuthenticationError("Gemini API key is missing or not configured.")

        model = request.model or self.default_model
        url = f"{self.BASE_URL}/{model}:generateContent?key={self._api_key}"

        # Transform chat messages to Gemini's contents structure
        contents = []
        system_instruction = None

        for msg in request.messages:
            if msg.role.value == "system":
                system_instruction = {"parts": [{"text": msg.content}]}
            else:
                role = "user" if msg.role.value == "user" else "model"
                contents.append({"role": role, "parts": [{"text": msg.content}]})

        payload: dict = {
            "contents": contents,
            "generationConfig": {
                "temperature": request.temperature,
            },
        }
        if system_instruction:
            payload["systemInstruction"] = system_instruction
        if request.max_tokens:
            payload["generationConfig"]["maxOutputTokens"] = request.max_tokens

        try:
            async with httpx.AsyncClient(timeout=request.timeout_seconds) as client:
                res = await client.post(url, json=payload)

            if res.status_code == 400 and "API_KEY_INVALID" in res.text:
                raise AuthenticationError("Invalid Gemini API Key.")
            if res.status_code == 429:
                raise RateLimitError("Gemini rate limit exceeded.")
            if res.status_code >= 500:
                raise ProviderUnavailableError(f"Gemini server error: {res.status_code}")

            res.raise_for_status()
            data = res.json()

            candidates = data.get("candidates", [])
            content_text = ""
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    content_text = parts[0].get("text", "")

            usage_meta = data.get("usageMetadata", {})
            return ModelResponse(
                content=content_text,
                model_name=model,
                provider=self.provider_type,
                usage=TokenUsage(
                    prompt_tokens=usage_meta.get("promptTokenCount", 0),
                    completion_tokens=usage_meta.get("candidatesTokenCount", 0),
                    total_tokens=usage_meta.get("totalTokenCount", 0),
                ),
            )
        except httpx.TimeoutException as exc:
            raise ProviderUnavailableError(f"Gemini request timed out: {exc}") from exc
        except httpx.RequestError as exc:
            raise ProviderUnavailableError(f"Network error calling Gemini: {exc}") from exc

