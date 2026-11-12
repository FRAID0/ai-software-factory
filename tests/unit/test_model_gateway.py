import unittest
from model_gateway.exceptions import AuthenticationError
from model_gateway.gateway import ModelGateway
from model_gateway.providers.mock import MockProvider
from shared.schemas.models import (
    ChatMessage,
    ChatRole,
    ModelRequest,
    ProviderType,
)
from shared.utilities.config import AppConfig


class TestModelGateway(unittest.IsolatedAsyncioTestCase):
    async def test_gateway_with_mock_provider(self) -> None:
        gateway = ModelGateway(auto_bootstrap=False)

        mock = MockProvider(canned_response="def add(a, b): return a + b")
        gateway.register_provider(mock)

        req = ModelRequest(
            messages=[ChatMessage(role=ChatRole.USER, content="Write an add function")],
            model="mock-model",
        )

        response = await gateway.complete(req, preferred_provider=ProviderType.MOCK)
        self.assertEqual(response.content, "def add(a, b): return a + b")
        self.assertEqual(response.provider, ProviderType.MOCK)
        self.assertEqual(response.usage.total_tokens, 30)
        self.assertEqual(gateway.total_usage.total_tokens, 30)

    async def test_gateway_raises_auth_error_when_no_providers(self) -> None:
        gateway = ModelGateway(auto_bootstrap=False)

        req = ModelRequest(messages=[ChatMessage(role=ChatRole.USER, content="test")])
        with self.assertRaises(AuthenticationError):
            await gateway.complete(req)


if __name__ == "__main__":
    unittest.main()
