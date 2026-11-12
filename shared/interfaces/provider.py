from abc import ABC, abstractmethod
from shared.schemas.models import ModelRequest, ModelResponse, ProviderType


class BaseLLMProvider(ABC):
    """
    Abstract interface for all LLM providers in the AI Software Factory.
    Ensures that adding or swapping a provider never requires changing agent logic.
    """

    @property
    @abstractmethod
    def provider_type(self) -> ProviderType:
        """Returns the specific provider type."""
        pass

    @property
    @abstractmethod
    def default_model(self) -> str:
        """Returns the default model identifier for this provider."""
        pass

    @abstractmethod
    async def complete(self, request: ModelRequest) -> ModelResponse:
        """
        Asynchronously sends a completion request to the provider.
        Must handle authentication, formatting, response parsing, and error wrapping.
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Checks whether credentials and connectivity for this provider are configured.
        """
        pass
