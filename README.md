# AI Software Factory

[![CI](https://github.com/FRAID0/ai-software-factory/actions/workflows/ci.yml/badge.svg)](https://github.com/FRAID0/ai-software-factory/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

An autonomous, multi-agent software engineering framework engineered to coordinate specialized AI agents through every phase of the software development lifecycle (SDLC)—from requirements engineering to architecture, implementation, automated testing, security validation, and deployment.

---

## 1. Vision & Architecture

The AI Software Factory coordinates specialized agent roles via a decoupled orchestrator and a provider-agnostic Model Gateway:

```
[ User Request ] ──> [ Orchestrator Engine (DAG / State Machine) ]
                               │
       ┌───────────────┬───────┴───────┬───────────────┐
       ▼               ▼               ▼               ▼
[ Architect ]    [ Backend ]     [ Frontend ]     [ DevOps / QA / Sec ]
       │               │               │               │
       └───────────────┴───────┬───────┴───────────────┘
                               ▼
                   [ Model Gateway Router ]
                               │
            ┌──────────────────┼──────────────────┐
            ▼                  ▼                  ▼
     [ Google Gemini ]      [ Groq ]       [ OpenRouter ]
                               │
                               ▼
             [ Isolated Execution Sandbox ]
```

### Core Tenets
- **Provider Agnostic**: Agents interact with standard interfaces, decoupling business logic from concrete LLM APIs.
- **Resilient & Dynamic Routing**: Dynamic model selection based on cost, context window, latency, and reasoning requirements.
- **Safe Sandboxing**: Execution of generated code is isolated in monitored runtimes with restricted filesystem and network access.
- **Observable & Testable**: Structured JSON logs, token usage accounting, and automated regression benchmarking.

---

## 2. Directory Structure

```text
ai-software-factory/
├── docs/                   # Architectural blueprints and specifications
│   ├── AI_FACTORY_SPEC.md  # Comprehensive factory specification
│   ├── ARCHITECTURE.md     # Clean architecture and design principles
│   ├── AGENT_ROLES.md      # Detailed agent contracts and responsibilities
│   ├── MODEL_REGISTRY.md   # Model capabilities, pricing, and routing policy
│   ├── SECURITY.md         # Threat model and sandboxing guidelines
│   ├── DEVELOPMENT.md      # Contributor setup and coding standards
│   └── ROADMAP.md          # Implementation phases and milestones
├── orchestrator/           # Workflow orchestration, DAG execution & state tracking
├── agents/                 # Specialized domain agents
│   ├── architect/          # System design & component contracts
│   ├── backend/            # API, data model & business logic generation
│   ├── frontend/           # UI/UX & client application generation
│   ├── devops/             # Docker, CI/CD & infrastructure-as-code
│   ├── qa/                 # Test generation, execution & validation
│   ├── security/           # SAST, vulnerability scans & secret auditing
│   └── documentation/      # Technical docs, API references & guides
├── model_gateway/          # Unified LLM provider abstraction & routing
│   ├── providers/          # Gemini, Groq, OpenRouter adapters
│   └── routing/            # Capability & latency-based routing
├── shared/                 # Domain models, protocols & common utilities
│   ├── schemas/            # Pydantic data models
│   ├── interfaces/         # Protocol and abstract base classes
│   └── utilities/          # Structured logging & configuration
├── benchmark/              # Model performance & evaluation suite
├── sandbox/                # Isolated code execution interface
├── tests/                  # Unit, integration, and E2E test suites
└── scripts/                # Verification, setup, and maintenance tools
```

---

## 3. Quickstart

### Prerequisites
- Python 3.12+
- Docker (optional, for sandboxed execution)
- API key for at least one supported provider (Gemini, Groq, or OpenRouter)

### Installation
1. Clone the repository:
   ```bash
   git clone git@github.com:FRAID0/ai-software-factory.git
   cd ai-software-factory
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your provider credentials
   ```

5. Verify installation:
   ```bash
   python -m scripts.verify_setup
   ```

---

## 4. Running Tests

```bash
pytest tests/unit
```

---

## 5. Security & Isolation

Never run untrusted generated code directly on the host machine. The `sandbox/` module isolates code evaluation within constrained containers without host network access or environment secrets. Review [docs/SECURITY.md](docs/SECURITY.md) for full compliance guidelines.

---

## 6. License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.

