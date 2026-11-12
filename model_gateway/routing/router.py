from shared.schemas.models import ModelCapability, ProviderType
from shared.utilities.logger import get_logger

logger = get_logger("model_gateway.routing")


class ModelRouter:
    """
    Intelligent routing engine that determines the optimal provider and model
    based on task capability requirements, availability, and cost/speed trade-offs.
    """

    # Routing preference table: capability -> ordered list of (provider, model)
    DEFAULT_ROUTES: dict[ModelCapability, list[tuple[ProviderType, str]]] = {
        ModelCapability.REASONING: [
            (ProviderType.OPENROUTER, "liquid/lfm-3-1.7b:free"),
            (ProviderType.GEMINI, "gemini-2.5-flash"),
            (ProviderType.GROQ, "llama-3.3-70b-versatile"),
        ],
        ModelCapability.CODE_GENERATION: [
            (ProviderType.GROQ, "llama-3.3-70b-versatile"),
            (ProviderType.GEMINI, "gemini-2.5-flash"),
            (ProviderType.OPENROUTER, "liquid/lfm-3-1.7b:free"),
        ],
        ModelCapability.FAST_INFERENCE: [
            (ProviderType.GROQ, "llama-3.1-8b-instant"),
            (ProviderType.GEMINI, "gemini-2.5-flash"),
        ],
        ModelCapability.LONG_CONTEXT: [
            (ProviderType.GEMINI, "gemini-2.5-flash"),
            (ProviderType.OPENROUTER, "liquid/lfm-3-1.7b:free"),
        ],
    }

    def resolve_route(
        self,
        capability: ModelCapability,
        available_providers: set[ProviderType],
    ) -> tuple[ProviderType, str] | None:
        """
        Resolves the preferred available provider and model for a given capability.
        """
        candidates = self.DEFAULT_ROUTES.get(capability, [])
        for provider, model in candidates:
            if provider in available_providers:
                logger.debug(
                    "Resolved route for capability %s -> %s (%s)",
                    capability.value,
                    provider.value,
                    model,
                )
                return provider, model

        logger.warning("No available provider found matching capability: %s", capability.value)
        return None

