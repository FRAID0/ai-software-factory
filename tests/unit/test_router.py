from model_gateway.routing.router import ModelRouter
from shared.schemas.models import ModelCapability, ProviderType


def test_router_resolves_reasoning_capability() -> None:
    router = ModelRouter()
    available = {ProviderType.OPENROUTER, ProviderType.GROQ}

    route = router.resolve_route(ModelCapability.REASONING, available)
    assert route is not None
    provider, model = route
    assert provider == ProviderType.OPENROUTER


def test_router_resolves_fast_inference() -> None:
    router = ModelRouter()
    available = {ProviderType.GROQ, ProviderType.GEMINI}

    route = router.resolve_route(ModelCapability.FAST_INFERENCE, available)
    assert route is not None
    provider, model = route
    assert provider == ProviderType.GROQ
    assert "llama" in model


def test_router_returns_none_when_no_match() -> None:
    router = ModelRouter()
    available: set[ProviderType] = set()

    route = router.resolve_route(ModelCapability.CODE_GENERATION, available)
    assert route is None
