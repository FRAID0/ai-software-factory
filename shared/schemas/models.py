from datetime import datetime, timezone
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class ChatRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class ProviderType(str, Enum):
    GEMINI = "gemini"
    GROQ = "groq"
    OPENROUTER = "openrouter"
    MOCK = "mock"


class ModelCapability(str, Enum):
    REASONING = "reasoning"
    CODE_GENERATION = "code_generation"
    FAST_INFERENCE = "fast_inference"
    LONG_CONTEXT = "long_context"


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ChatMessage(BaseModel):
    role: ChatRole
    content: str
    reasoning_details: Any | None = None
    name: str | None = None


class ModelRequest(BaseModel):
    messages: list[ChatMessage]
    model: str | None = None
    temperature: float = 0.2
    max_tokens: int | None = None
    enable_reasoning: bool = False
    timeout_seconds: float = 60.0
    metadata: dict[str, Any] = Field(default_factory=dict)


class TokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    reasoning_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_usd: float = 0.0


class ModelResponse(BaseModel):
    content: str
    model_name: str
    provider: ProviderType
    usage: TokenUsage = Field(default_factory=TokenUsage)
    reasoning_details: Any | None = None
    latency_ms: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AgentTask(BaseModel):
    task_id: str
    agent_role: str
    title: str
    description: str
    input_data: dict[str, Any] = Field(default_factory=dict)
    dependencies: list[str] = Field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AgentResult(BaseModel):
    task_id: str
    agent_role: str
    status: TaskStatus
    output_data: dict[str, Any] = Field(default_factory=dict)
    artifacts: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    execution_time_seconds: float = 0.0

