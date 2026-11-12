import unittest
from agents.base import GenericAgent
from model_gateway.gateway import ModelGateway
from model_gateway.providers.mock import MockProvider
from orchestrator.engine import OrchestratorEngine
from shared.schemas.models import AgentTask, TaskStatus
from shared.utilities.config import AppConfig


class TestOrchestrator(unittest.IsolatedAsyncioTestCase):
    async def test_orchestrator_resolves_and_runs_tasks_in_order(self) -> None:
        gateway = ModelGateway(auto_bootstrap=False)
        gateway.register_provider(MockProvider(canned_response="Generated output"))

        engine = OrchestratorEngine()

        architect = GenericAgent(
            role="architect",
            description="Software Architect",
            gateway=gateway,
            system_prompt="Design architectures.",
        )
        backend = GenericAgent(
            role="backend",
            description="Backend Developer",
            gateway=gateway,
            system_prompt="Write backend code.",
        )

        engine.register_agent(architect)
        engine.register_agent(backend)

        task1 = AgentTask(
            task_id="t1",
            agent_role="architect",
            title="Architecture Blueprint",
            description="Design system",
        )
        task2 = AgentTask(
            task_id="t2",
            agent_role="backend",
            title="Backend API",
            description="Implement API",
            dependencies=["t1"],
        )

        engine.register_task(task2)
        engine.register_task(task1)

        results = await engine.run()
        self.assertEqual(len(results), 2)
        self.assertEqual(results["t1"].status, TaskStatus.COMPLETED)
        self.assertEqual(results["t2"].status, TaskStatus.COMPLETED)

    async def test_orchestrator_detects_dependency_cycle(self) -> None:
        engine = OrchestratorEngine()

        t1 = AgentTask(task_id="t1", agent_role="a", title="1", description="", dependencies=["t2"])
        t2 = AgentTask(task_id="t2", agent_role="b", title="2", description="", dependencies=["t1"])

        engine.register_task(t1)
        engine.register_task(t2)

        with self.assertRaises(ValueError):
            await engine.run()


if __name__ == "__main__":
    unittest.main()
