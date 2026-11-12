from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from model_gateway.gateway import ModelGateway
from shared.schemas.models import ChatMessage, ChatRole, ModelRequest, ProviderType
from shared.utilities.logger import get_logger

logger = get_logger("benchmark.runner")


@dataclass
class BenchmarkMetric:
    test_case_id: str
    model_name: str
    provider: ProviderType
    latency_ms: float
    passed: bool
    prompt_tokens: int
    completion_tokens: int
    error: str | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class BenchmarkRunner:
    """
    Harness for evaluating models under real-world software engineering tasks.
    Captures latency, token counts, and test outcomes without synthetic inflation.
    """

    def __init__(self, gateway: ModelGateway):
        self.gateway = gateway
        self.results: list[BenchmarkMetric] = []

    async def run_single_evaluation(
        self,
        test_case_id: str,
        prompt: str,
        model: str,
        provider: ProviderType,
        expected_substring: str | None = None,
    ) -> BenchmarkMetric:
        request = ModelRequest(
            messages=[ChatMessage(role=ChatRole.USER, content=prompt)],
            model=model,
            temperature=0.0,
        )

        try:
            response = await self.gateway.complete(request, preferred_provider=provider)
            passed = True
            if expected_substring:
                passed = expected_substring.lower() in response.content.lower()

            metric = BenchmarkMetric(
                test_case_id=test_case_id,
                model_name=response.model_name,
                provider=response.provider,
                latency_ms=response.latency_ms,
                passed=passed,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
            )
            self.results.append(metric)
            return metric
        except Exception as exc:
            logger.error("Benchmark failed for %s on %s: %s", model, provider.value, exc)
            failed_metric = BenchmarkMetric(
                test_case_id=test_case_id,
                model_name=model,
                provider=provider,
                latency_ms=0.0,
                passed=False,
                prompt_tokens=0,
                completion_tokens=0,
                error=str(exc),
            )
            self.results.append(failed_metric)
            return failed_metric

