from abc import ABC, abstractmethod
from shared.schemas.models import AgentResult, AgentTask


class BaseAgent(ABC):
    """
    Standard contract for all specialized agents in the factory.
    Each agent encapsulates domain reasoning, tool execution, and artifact generation.
    """

    @property
    @abstractmethod
    def role_name(self) -> str:
        """Unique identifier of the agent role (e.g. 'architect', 'backend')."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """High-level explanation of the agent's responsibility."""
        pass

    @abstractmethod
    async def execute_task(self, task: AgentTask) -> AgentResult:
        """
        Processes an assigned task, invokes models via the gateway,
        generates domain artifacts, and returns structured results.
        """
        pass

