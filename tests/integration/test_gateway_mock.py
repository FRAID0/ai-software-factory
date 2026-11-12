import unittest
from agents.base import GenericAgent
from model_gateway.gateway import ModelGateway
from model_gateway.providers.mock import MockProvider
from shared.schemas.models import AgentTask, ModelCapability, TaskStatus
from shared.utilities.config import AppConfig


class TestGatewayIntegration(unittest.IsolatedAsyncioTestCase):
    async def test_agent_gateway_mock_integration(self) -> None:
        gateway = ModelGateway(auto_bootstrap=False)

        mock_code = "class Calculator:\n    def add(self, a, b):\n        return a + b"
        gateway.register_provider(MockProvider(canned_response=mock_code))

        backend_agent = GenericAgent(
            role="backend",
            description="Generates backend code",
            gateway=gateway,
            system_prompt="You write clean Python classes.",
            preferred_capability=ModelCapability.CODE_GENERATION,
        )

        task = AgentTask(
            task_id="integ-task-1",
            agent_role="backend",
            title="Create Calculator Service",
            description="Write a Python class for a calculator.",
            input_data={"class_name": "Calculator"},
        )

        result = await backend_agent.execute_task(task)
        self.assertEqual(result.status, TaskStatus.COMPLETED)
        self.assertIn("class Calculator", result.output_data["raw_response"])
        self.assertGreaterEqual(result.execution_time_seconds, 0.0)


if __name__ == "__main__":
    unittest.main()
