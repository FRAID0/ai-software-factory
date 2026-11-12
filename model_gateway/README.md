# Model Gateway

The **Model Gateway** is the unified access layer for all LLM inference in the AI Software Factory.

## Responsibilities
1. **Provider Isolation**: Agents never import provider-specific client libraries (`groq`, `google-genai`, etc.). They communicate exclusively with `ModelGateway`.
2. **Capability-Based Routing**: Dispatches requests based on task requirements (reasoning, high-speed code generation, or cost-conscious verification).
3. **Resilience & Fallbacks**: Automatically retries on transient errors and switches to a fallback provider if a primary provider hits rate limits or network issues.
4. **Token & Cost Accounting**: Tracks prompt, completion, and reasoning token consumption across every agent invocation.

## Structure
- `providers/`: Concrete adapters for Gemini, Groq, OpenRouter, and Mock (for unit testing).
- `routing/`: Dynamic task-to-model selection logic.
- `exceptions.py`: Standardized domain exceptions (`RateLimitError`, `ProviderError`, `AuthenticationError`).
- `gateway.py`: The orchestrating entry point managing adapters and retries.

