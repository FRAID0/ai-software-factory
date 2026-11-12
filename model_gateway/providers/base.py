import time
from abc import abstractmethod
from shared.interfaces.provider import BaseLLMProvider
from shared.schemas.models import ModelRequest, ModelResponse
from shared.utilities.logger import get_logger

logger = get_logger("model_gateway.providers")


class AbstractProviderAdapter(BaseLLMProvider):
    """
    Base implementation providing shared metrics, validation,
    and timing functionality for concrete provider adapters.
    """

    def __init__(self, api_key: str | None = None):
        self._api_key = api_key

    def is_available(self) -> bool:
        return bool(self._api_key and self._api_key.strip())

    async def execute_with_timing(self, request: ModelRequest) -> ModelResponse:
        start_time = time.perf_counter()
        response = await self._perform_completion(request)
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        response.latency_ms = round(elapsed_ms, 2)
        return response

    @abstractmethod
    async def _perform_completion(self, request: ModelRequest) -> ModelResponse:
        """Internal completion implementation specific to the provider."""
        pass

    async def complete(self, request: ModelRequest) -> ModelResponse:
        return await self.execute_with_timing(request)
