from shared.schemas.models import (
    AgentResult,
    AgentTask,
    ChatMessage,
    ChatRole,
    ModelRequest,
    ModelResponse,
    ProviderType,
    TaskStatus,
    TokenUsage,
)


def test_chat_message_creation() -> None:
    msg = ChatMessage(role=ChatRole.USER, content="Hello World")
    assert msg.role == ChatRole.USER
    assert msg.content == "Hello World"
    assert msg.reasoning_details is None


def test_model_request_defaults() -> None:
    req = ModelRequest(
        messages=[ChatMessage(role=ChatRole.SYSTEM, content="You are an architect")]
    )
    assert req.temperature == 0.2
    assert req.timeout_seconds == 60.0
    assert not req.enable_reasoning


def test_token_usage_aggregation() -> None:
    usage = TokenUsage(prompt_tokens=100, completion_tokens=50, total_tokens=150)
    assert usage.prompt_tokens == 100
    assert usage.completion_tokens == 50
    assert usage.total_tokens == 150


def test_agent_task_lifecycle() -> None:
    task = AgentTask(
        task_id="task-001",
        agent_role="architect",
        title="Design Database Schema",
        description="Create PostgreSQL tables for user authentication.",
    )
    assert task.status == TaskStatus.PENDING
    assert len(task.dependencies) == 0

    result = AgentResult(
        task_id=task.task_id,
        agent_role=task.agent_role,
        status=TaskStatus.COMPLETED,
        output_data={"tables": ["users", "sessions"]},
    )
    assert result.status == TaskStatus.COMPLETED
    assert "users" in result.output_data["tables"]

