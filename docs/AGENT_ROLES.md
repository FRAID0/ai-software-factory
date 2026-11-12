# Agent Roles & Responsibilities

This document defines the contracts, inputs, outputs, and scope for each specialized agent in the AI Software Factory.

---

## 1. Summary Matrix

| Agent | Core Responsibility | Primary Input | Primary Output | Recommended Model Tier |
|---|---|---|---|---|
| **Architect** | Requirements decomposition, system design, data modeling, DAG generation | User project brief | Architecture spec, API schema, WBS task DAG | High reasoning & large context |
| **Backend** | API development, business logic, persistence layers | Architecture spec, OpenAPI contracts | Source code, migrations, configs | High code generation & accuracy |
| **Frontend** | UI/UX implementation, component design, client state | Wireframes, API schemas | Frontend code, component styles | High code generation |
| **DevOps** | Containerization, CI/CD pipelines, runtime configurations | Tech stack definition | Dockerfile, compose, GitHub Actions | Moderate code generation |
| **QA** | Unit, integration & E2E test generation, execution analysis | Source code, API contracts | Test suites, test reports | High code generation & precision |
| **Security** | Static analysis (SAST), vulnerability audit, secret detection | Source code, dependencies | Security audit report, remediations | High reasoning & analysis |
| **Documentation** | API docs, user guides, setup instructions, architecture summaries | Codebase, specs | README, API docs, release notes | Fast generation & clear prose |

---

## 2. Detailed Agent Specifications

### 2.1 Architect Agent (`agents/architect`)
- **Mission**: Ingest raw user requirements and formulate an actionable technical blueprint.
- **Inputs**: User prompt, domain constraints, target platforms.
- **Outputs**:
  - `docs/ARCHITECTURE.md`
  - OpenAPI / JSON schema definitions
  - Task Dependency Graph (`DAG`) for the orchestrator

### 2.2 Backend Agent (`agents/backend`)
- **Mission**: Implement server-side logic following SOLID and Clean Architecture standards.
- **Inputs**: Architecture blueprint, schema definitions.
- **Outputs**:
  - Cleanly structured backend source files
  - Database migration scripts
  - Package dependency manifests

### 2.3 Frontend Agent (`agents/frontend`)
- **Mission**: Build client interfaces conforming to design specs and API contracts.
- **Inputs**: API contracts, UI guidelines.
- **Outputs**:
  - Frontend components, styling, and state management logic.

### 2.4 DevOps Agent (`agents/devops`)
- **Mission**: Package and automate lifecycle operations.
- **Inputs**: Target environment definitions and runtime requirements.
- **Outputs**:
  - `Dockerfile`, `docker-compose.yml`, CI/CD pipelines (`.github/workflows/ci.yml`).

### 2.5 QA Agent (`agents/qa`)
- **Mission**: Ensure 100% test coverage of critical paths and verify edge cases.
- **Inputs**: Source code files and interface specifications.
- **Outputs**:
  - Executable test files (`tests/unit`, `tests/integration`).
  - Analysis of test execution runs inside the sandbox.

### 2.6 Security Agent (`agents/security`)
- **Mission**: Detect code smells, hardcoded secrets, injection vectors, and outdated libraries.
- **Inputs**: Full codebase and configuration files.
- **Outputs**:
  - Security audit report and patch recommendations.

### 2.7 Documentation Agent (`agents/documentation`)
- **Mission**: Keep all developer and user documentation synchronized with code changes.
- **Inputs**: Project specifications, codebase, deployment files.
- **Outputs**:
  - `README.md`, setup guides, API reference docs.
