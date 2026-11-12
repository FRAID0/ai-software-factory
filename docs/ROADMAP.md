# AI Software Factory Roadmap

This roadmap outlines the phased development from the initial bootstrap to full autonomous operation.

---

## Phase 0: Foundation & Bootstrap *(Current Phase)*
- [x] Repository scaffolding and directory structure
- [x] Comprehensive documentation and engineering specs
- [x] Shared data schemas and abstract interfaces (`Pydantic`, `ABC`)
- [x] Model Gateway abstraction architecture (Gemini, Groq, OpenRouter)
- [x] CI/CD pipeline definition with GitHub Actions
- [x] Unit test harness setup

---

## Phase 1: Model Gateway & Benchmarking Harness
- [ ] Implement concrete provider clients (`httpx` + SDKs)
- [ ] Add dynamic fallback circuit breaker
- [ ] Implement token accounting and budget enforcement
- [ ] Implement initial benchmark suite for code generation (HumanEval / MBPP style)

---

## Phase 2: Orchestration Engine & State Store
- [ ] Implement Task DAG engine with topological sorting
- [ ] Add async task queue and execution state persistence
- [ ] Implement retry policies with exponential backoff
- [ ] Add human-in-the-loop approval checkpoints

---

## Phase 3: Core Agents MVP
- [ ] Architect Agent: Requirements -> OpenAPI spec + Task DAG
- [ ] Backend Agent: OpenAPI spec -> Python/FastAPI implementation
- [ ] QA Agent: Implementation -> Automated Pytest suites
- [ ] DevOps Agent: Dockerfile and CI workflow generation

---

## Phase 4: Isolated Sandbox Runtime
- [ ] Docker-in-Docker / unprivileged container execution runtime
- [ ] Resource throttling (CPU, RAM, disk I/O)
- [ ] Ephemeral workspace creation and teardown
- [ ] Real-time stdout/stderr streaming and artifact collection

---

## Phase 5: Autonomous End-to-End Pipeline
- [ ] Full loop: User prompt -> Architecture -> Code -> Tests -> Sandbox verify -> Git release
- [ ] Feedback loops: Automated self-healing when tests fail in the sandbox
- [ ] Performance profiling and cost optimization dashboard

