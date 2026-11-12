from abc import ABC, abstractmethod
from typing import Any
from shared.schemas.models import AgentResult, AgentTask, TaskStatus


class BaseOrchestrator(ABC):
    """
    Contract for the execution engine managing tasks, DAG dependencies,
    agent scheduling, and system state transitions.
    """

    @abstractmethod
    def register_task(self, task: AgentTask) -> None:
        """Registers a new task into the orchestrator execution graph."""
        pass

    @abstractmethod
    def get_task_status(self, task_id: str) -> TaskStatus:
        """Queries the current status of a task."""
        pass

    @abstractmethod
    async def run(self) -> dict[str, AgentResult]:
        """
        Executes the registered tasks according to their dependency graph (DAG)
        and returns the consolidated execution results.
        """
        pass

