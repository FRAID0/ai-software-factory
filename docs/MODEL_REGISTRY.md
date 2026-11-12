# Model Registry & Evaluation Framework

## 1. Supported Providers

The factory integrates with three initial providers, with extensibility for future additions:

1. **Google Gemini** (`google-genai` / REST)
   - Excellent for long-context architecture ingestion, multimodal specs, and structured outputs.
2. **Groq** (`groq` / REST)
   - Ultra-low latency inference powered by LPUs. Ideal for rapid code generation, quick iterations, and unit test generation.
3. **OpenRouter** (Unified REST API)
   - Broad model access (LFM, Claude, Llama, DeepSeek, Qwen), reasoning token extraction, and flexible fallback routing.

---

## 2. Evaluation Dimensions

Models registered in the factory are benchmarked across seven quantitative dimensions:

| Dimension | Description | Measurement Unit |
|---|---|---|
| **Code Generation Quality** | Syntactic validity, passing unit tests, adherence to instructions | Pass@1 (%) |
| **Reasoning Capability** | Complex logic breakdown, dependency resolution, edge-case anticipation | Multi-step score (0-100) |
| **Response Latency** | Time to first token (TTFT) and total round-trip time (RTT) | Milliseconds (ms) |
| **Throughput** | Token generation speed | Tokens / second |
| **API Reliability** | Uptime, rate-limit consistency, error rate | Success rate (%) |
| **Cost Efficiency** | Blended cost per million tokens (input vs. output) | USD / 1M tokens |
| **Effective Context Window** | Maximum prompt size before degradation of retrieval/instruction | Tokens |

---

## 3. Dynamic Routing Matrix

The `ModelRouter` inspects incoming task requirements and routes to the optimal provider:

```
[ Task Requirement ]
        │
        ├── High Reasoning / Planning ───────────> Tier 1 Reasoning (e.g. Gemini / DeepSeek / Claude via OpenRouter)
        ├── High-Speed Code Generation ─────────> Fast LPU Tier (e.g. Llama-3.3-70B on Groq)
        ├── Low-Cost / Free Verification Checks ──> Free Tier (e.g. OpenRouter Free Models)
        └── Fallback upon Rate Limit / Error ───> Secondary Provider
```
