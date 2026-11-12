import os
from functools import lru_cache
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env if present
load_dotenv()


class AppConfig(BaseModel):
    # LLM API Keys
    gemini_api_key: str | None = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY"))
    groq_api_key: str | None = Field(default_factory=lambda: os.getenv("GROQ_API_KEY"))
    openrouter_api_key: str | None = Field(
        default_factory=lambda: os.getenv("OPENROUTER_API_KEY")
    )

    # Defaults
    default_llm_provider: str = Field(
        default_factory=lambda: os.getenv("DEFAULT_LLM_PROVIDER", "groq")
    )
    default_fallback_provider: str = Field(
        default_factory=lambda: os.getenv("DEFAULT_FALLBACK_PROVIDER", "openrouter")
    )

    # Environment
    factory_env: str = Field(default_factory=lambda: os.getenv("FACTORY_ENV", "development"))
    log_level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    # Gateway options
    gateway_request_timeout: float = Field(
        default_factory=lambda: float(os.getenv("GATEWAY_REQUEST_TIMEOUT_SECONDS", "60.0"))
    )
    gateway_max_retries: int = Field(
        default_factory=lambda: int(os.getenv("GATEWAY_MAX_RETRIES", "3"))
    )

    # Sandbox
    sandbox_enabled: bool = Field(
        default_factory=lambda: os.getenv("SANDBOX_ENABLED", "true").lower() == "true"
    )
    sandbox_timeout_seconds: float = Field(
        default_factory=lambda: float(os.getenv("SANDBOX_TIMEOUT_SECONDS", "30.0"))
    )


@lru_cache
def get_config() -> AppConfig:
    """Returns a cached singleton configuration instance."""
    return AppConfig()
