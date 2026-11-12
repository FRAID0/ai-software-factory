import time
from model_gateway.gateway import ModelGateway
from shared.interfaces.agent import BaseAgent
from shared.schemas.models import (
    AgentResult,
    AgentTask,
    ChatMessage,
    ChatRole,
    ModelCapability,
    ModelRequest,
    TaskStatus,
)
from shared.utilities.logger import get_logger

logger = get_logger("agents.base")


class GenericAgent(BaseAgent):
    """
    Standard agent implementation binding domain tasks to the ModelGateway.
    Subclasses customize prompts, required capabilities, and output parsers.
    """

    def __init__(
        self,
        role: str,
        description: str,
        gateway: ModelGateway,
        system_prompt: str,
        preferred_capability: ModelCapability = ModelCapability.CODE_GENERATION,
    ):
        self._role = role
        self._description = description
        self.gateway = gateway
        self.system_prompt = system_prompt
        self.preferred_capability = preferred_capability

    @property
    def role_name(self) -> str:
        return self._role

    @property
    def description(self) -> str:
        return self._description

    async def execute_task(self, task: AgentTask) -> AgentResult:
        start_time = time.perf_counter()
        logger.info("[%s] Executing task %s: %s", self.role_name, task.task_id, task.title)

        messages = [
            ChatMessage(role=ChatRole.SYSTEM, content=self.system_prompt),
            ChatMessage(
                role=ChatRole.USER,
                content=f"Task: {task.title}\nDescription: {task.description}\nData: {task.input_data}",
            ),
        ]

        request = ModelRequest(
            messages=messages,
            metadata={"task_id": task.task_id, "agent": self.role_name},
        )

        try:
            response = await self.gateway.complete(
                request,
                required_capability=self.preferred_capability,
            )
            elapsed = time.perf_counter() - start_time

            return AgentResult(
                task_id=task.task_id,
                agent_role=self.role_name,
                status=TaskStatus.COMPLETED,
                output_data={"raw_response": response.content},
                execution_time_seconds=round(elapsed, 3),
            )
        except Exception as exc:
            elapsed = time.perf_counter() - start_time
            logger.exception("[%s] Task execution failed: %s", self.role_name, exc)
            return AgentResult(
                task_id=task.task_id,
                agent_role=self.role_name,
                status=TaskStatus.FAILED,
                errors=[str(exc)],
                execution_time_seconds=round(elapsed, 3),
            )
