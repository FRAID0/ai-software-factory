import asyncio
from model_gateway.exceptions import (
    AuthenticationError,
    GatewayError,
    ProviderUnavailableError,
    RateLimitError,
    RoutingError,
)
from model_gateway.providers.base import AbstractProviderAdapter
from model_gateway.providers.gemini import GeminiProvider
from model_gateway.providers.groq import GroqProvider
from model_gateway.providers.mock import MockProvider
from model_gateway.providers.openrouter import OpenRouterProvider
from model_gateway.routing.router import ModelRouter
from shared.schemas.models import (
    ModelCapability,
    ModelRequest,
    ModelResponse,
    ProviderType,
    TokenUsage,
)
from shared.utilities.config import AppConfig, get_config
from shared.utilities.logger import get_logger

logger = get_logger("model_gateway")


class ModelGateway:
    """
    Unified entry point for LLM access across the AI Software Factory.
    Provides provider abstraction, automatic fallback, retry policies, and accounting.
    """

    def __init__(
        self,
        config: AppConfig | None = None,
        router: ModelRouter | None = None,
        auto_bootstrap: bool = True,
    ):
        self.config = config or get_config()
        self.router = router or ModelRouter()
        self._providers: dict[ProviderType, AbstractProviderAdapter] = {}
        self._total_usage = TokenUsage()

        if auto_bootstrap:
            self._bootstrap_providers()

    def _bootstrap_providers(self) -> None:
        if self.config.gemini_api_key:
            self.register_provider(GeminiProvider(api_key=self.config.gemini_api_key))
        if self.config.groq_api_key:
            self.register_provider(GroqProvider(api_key=self.config.groq_api_key))
        if self.config.openrouter_api_key:
            self.register_provider(OpenRouterProvider(api_key=self.config.openrouter_api_key))

    def register_provider(self, provider: AbstractProviderAdapter) -> None:
        """Registers a provider adapter into the gateway."""
        self._providers[provider.provider_type] = provider
        logger.info("Registered provider adapter: %s", provider.provider_type.value)

    def get_available_providers(self) -> set[ProviderType]:
        """Returns all registered providers that have active credentials."""
        return {pt for pt, p in self._providers.items() if p.is_available()}

    @property
    def total_usage(self) -> TokenUsage:
        """Accumulated token usage across all gateway calls."""
        return self._total_usage

    async def complete(
        self,
        request: ModelRequest,
        preferred_provider: ProviderType | None = None,
        required_capability: ModelCapability | None = None,
    ) -> ModelResponse:
        """
        Executes a completion request with fallback and retry logic.
        """
        available = self.get_available_providers()
        if not available:
            raise AuthenticationError(
                "No LLM providers are available. Check your .env file or register a MockProvider."
            )

        target_provider: ProviderType | None = preferred_provider

        # If not specified, route via capability or default config
        if not target_provider and required_capability:
            resolved = self.router.resolve_route(required_capability, available)
            if resolved:
                target_provider, default_model = resolved
                if not request.model:
                    request.model = default_model

        if not target_provider or target_provider not in available:
            # Fallback to any available provider
            target_provider = next(iter(available))

        # Attempt execution with retries and fallback
        last_error: Exception | None = None
        providers_to_try = [target_provider] + [p for p in available if p != target_provider]

        for p_type in providers_to_try:
            adapter = self._providers[p_type]
            for attempt in range(1, self.config.gateway_max_retries + 1):
                try:
                    logger.debug(
                        "Attempt %d/%d calling provider %s...",
                        attempt,
                        self.config.gateway_max_retries,
                        p_type.value,
                    )
                    response = await adapter.complete(request)

                    # Update cumulative token accounting
                    self._total_usage.prompt_tokens += response.usage.prompt_tokens
                    self._total_usage.completion_tokens += response.usage.completion_tokens
                    self._total_usage.total_tokens += response.usage.total_tokens

                    return response

                except (RateLimitError, ProviderUnavailableError) as err:
                    last_error = err
                    logger.warning(
                        "Provider %s attempt %d failed (%s). Retrying...",
                        p_type.value,
                        attempt,
                        str(err),
                    )
                    if attempt < self.config.gateway_max_retries:
                        await asyncio.sleep(0.5 * attempt)
                    else:
                        logger.warning(
                            "Max retries exhausted for provider %s. Falling back to next available provider...",
                            p_type.value,
                        )
                except AuthenticationError:
                    # Do not retry auth errors on the same provider
                    raise

        raise GatewayError(f"All providers exhausted. Last error: {last_error}")
