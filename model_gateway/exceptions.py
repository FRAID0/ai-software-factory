class GatewayError(Exception):
    """Base exception for all Model Gateway errors."""
    pass


class AuthenticationError(GatewayError):
    """Raised when an API key is missing or rejected."""
    pass


class RateLimitError(GatewayError):
    """Raised when an upstream provider rate limit is exceeded."""
    def __init__(self, message: str, retry_after_seconds: float | None = None):
        super().__init__(message)
        self.retry_after_seconds = retry_after_seconds


class ProviderUnavailableError(GatewayError):
    """Raised when an upstream provider endpoint is unreachable or timing out."""
    pass


class ModelNotFoundError(GatewayError):
    """Raised when a requested model does not exist or is unsupported."""
    pass


class RoutingError(GatewayError):
    """Raised when no provider can be resolved for a specific task capability."""
    pass

