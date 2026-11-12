from model_gateway.providers.base import AbstractProviderAdapter
from shared.schemas.models import ModelRequest, ModelResponse, ProviderType, TokenUsage


class MockProvider(AbstractProviderAdapter):
    """
    Deterministic provider adapter used for automated testing,
    CI pipelines, and local development without incurring API costs.
    """

    def __init__(self, canned_response: str = "Mock response content."):
        super().__init__(api_key="mock_key")
        self.canned_response = canned_response
        self.invocations: list[ModelRequest] = []

    @property
    def provider_type(self) -> ProviderType:
        return ProviderType.MOCK

    @property
    def default_model(self) -> str:
        return "mock-model-v1"

    async def _perform_completion(self, request: ModelRequest) -> ModelResponse:
        self.invocations.append(request)
        model_name = request.model or self.default_model

        return ModelResponse(
            content=self.canned_response,
            model_name=model_name,
            provider=self.provider_type,
            usage=TokenUsage(
                prompt_tokens=10,
                completion_tokens=20,
                total_tokens=30,
                estimated_cost_usd=0.0,
            ),
        )

