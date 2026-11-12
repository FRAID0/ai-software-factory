# System Architecture & Design Principles

## 1. Architectural Philosophy

The AI Software Factory adheres to **Clean Architecture** and **SOLID** principles to ensure that system logic remains decoupled from specific AI providers, external frameworks, and runtime environments.

### Core Principles
- **Dependency Inversion**: High-level modules (Orchestrator, Agents) depend upon abstractions (`BaseLLMProvider`, `BaseAgent`), not on concrete provider implementations.
- **Single Responsibility**: Each agent owns one phase of software engineering; the Model Gateway owns only inference; the Orchestrator owns only state transitions.
- **Fail-Safe & Idempotency**: All agent tasks are atomic and idempotent. Failure at any point in the DAG allows retries without corrupting previous state.
- **Observability by Design**: Every prompt, completion, latency metric, and token count is tracked via structured logging.

---

## 2. Layered Architecture Diagram

```
┌──────────────────────────────────────────────────────────┐
│                   Presentation Layer                     │
│               (CLI, API Gateway, Webhooks)               │
└────────────────────────────┬─────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────┐
│                   Orchestration Layer                    │
│   • Task Dependency Graph (DAG)                          │
│   • State Store & Execution Engine                       │
│   • Failure Recovery & Retry Policies                    │
└──────────────┬────────────────────────────┬──────────────┘
               │                            │
┌──────────────▼─────────────┐┌─────────────▼──────────────┐
│        Agents Layer        ││       Sandbox Layer        │
│ • Architect   • Backend    ││ • Container Isolation      │
│ • Frontend    • DevOps     ││ • Resource Caps (CPU/RAM)  │
│ • QA          • Security   ││ • Network Isolation        │
│ • Documentation            ││ • Audit Trail              │
└──────────────┬─────────────┘└────────────────────────────┘
               │
┌──────────────▼───────────────────────────────────────────┐
│                    Model Gateway Layer                   │
│   • Provider Adapters (Gemini, Groq, OpenRouter)         │
│   • Task-to-Model Intelligent Router                     │
│   • Token Counter, Rate Limiting & Circuit Breakers      │
└──────────────────────────────────────────────────────────┘
```

---

## 3. Component Interactions

1. **User Request**: The user submits a specification.
2. **Orchestrator Initiation**: Initializes a workspace context and generates the execution DAG via the `ArchitectAgent`.
3. **Task Dispatching**: Tasks ready for execution (all dependencies resolved) are dispatched concurrently to worker agents (`BackendAgent`, `FrontendAgent`, etc.).
4. **Model Invocation**: Agents request LLM completions through the `ModelGateway.complete()` interface without needing to know which provider is serving the request.
5. **Execution Verification**: Artifacts generated (code, tests) are staged into the `Sandbox` for compilation and test execution.
6. **State Convergence**: Once all verification gates pass, the orchestrator packages the finalized project.

