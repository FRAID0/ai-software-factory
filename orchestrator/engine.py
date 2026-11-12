import asyncio
from collections import defaultdict, deque
from shared.interfaces.agent import BaseAgent
from shared.interfaces.orchestrator import BaseOrchestrator
from shared.schemas.models import AgentResult, AgentTask, TaskStatus
from shared.utilities.logger import get_logger

logger = get_logger("orchestrator.engine")


class OrchestratorEngine(BaseOrchestrator):
    """
    DAG-based task execution engine that schedules, coordinates,
    and runs multi-agent workflows.
    """

    def __init__(self) -> None:
        self._tasks: dict[str, AgentTask] = {}
        self._agents: dict[str, BaseAgent] = {}
        self._results: dict[str, AgentResult] = {}

    def register_agent(self, agent: BaseAgent) -> None:
        """Registers a worker agent by its role name."""
        self._agents[agent.role_name] = agent
        logger.info("Registered agent: %s (%s)", agent.role_name, agent.description)

    def register_task(self, task: AgentTask) -> None:
        """Adds a task to the execution graph."""
        self._tasks[task.task_id] = task
        logger.info(
            "Registered task: [%s] '%s' assigned to '%s' (deps: %s)",
            task.task_id,
            task.title,
            task.agent_role,
            task.dependencies,
        )

    def get_task_status(self, task_id: str) -> TaskStatus:
        if task_id not in self._tasks:
            raise KeyError(f"Task not found: {task_id}")
        return self._tasks[task_id].status

    def _resolve_topological_order(self) -> list[str]:
        """
        Calculates topological execution order and detects dependency cycles.
        """
        in_degree: dict[str, int] = {t_id: 0 for t_id in self._tasks}
        graph: dict[str, list[str]] = defaultdict(list)

        for t_id, task in self._tasks.items():
            for dep in task.dependencies:
                if dep not in self._tasks:
                    raise ValueError(f"Task {t_id} depends on nonexistent task {dep}")
                graph[dep].append(t_id)
                in_degree[t_id] += 1

        queue = deque([t_id for t_id, deg in in_degree.items() if deg == 0])
        ordered: list[str] = []

        while queue:
            current = queue.popleft()
            ordered.append(current)
            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(ordered) != len(self._tasks):
            raise ValueError("Cyclic dependency detected in task graph!")

        return ordered

    async def run(self) -> dict[str, AgentResult]:
        """
        Executes all registered tasks in dependency order.
        """
        execution_order = self._resolve_topological_order()
        logger.info("Executing %d tasks in order: %s", len(execution_order), execution_order)

        for task_id in execution_order:
            task = self._tasks[task_id]
            agent = self._agents.get(task.agent_role)

            if not agent:
                task.status = TaskStatus.FAILED
                error_msg = f"No agent registered for role: '{task.agent_role}'"
                logger.error(error_msg)
                self._results[task_id] = AgentResult(
                    task_id=task_id,
                    agent_role=task.agent_role,
                    status=TaskStatus.FAILED,
                    errors=[error_msg],
                )
                continue

            # Check if any dependencies failed
            failed_deps = [
                dep for dep in task.dependencies
                if self._results.get(dep) and self._results[dep].status != TaskStatus.COMPLETED
            ]
            if failed_deps:
                task.status = TaskStatus.CANCELLED
                error_msg = f"Task cancelled due to failed upstream dependencies: {failed_deps}"
                logger.warning(error_msg)
                self._results[task_id] = AgentResult(
                    task_id=task_id,
                    agent_role=task.agent_role,
                    status=TaskStatus.CANCELLED,
                    errors=[error_msg],
                )
                continue

            # Execute task
            task.status = TaskStatus.RUNNING
            logger.info("Starting execution for task [%s] via %s", task_id, task.agent_role)

            try:
                result = await agent.execute_task(task)
                task.status = result.status
                self._results[task_id] = result
                logger.info("Completed task [%s] with status: %s", task_id, result.status.value)
            except Exception as exc:
                task.status = TaskStatus.FAILED
                logger.exception("Task [%s] execution failed: %s", task_id, exc)
                self._results[task_id] = AgentResult(
                    task_id=task_id,
                    agent_role=task.agent_role,
                    status=TaskStatus.FAILED,
                    errors=[str(exc)],
                )

        return self._results
