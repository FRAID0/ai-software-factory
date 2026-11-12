# Orchestrator Subsystem

The **Orchestrator** is the central mission controller of the AI Software Factory.

## Core Responsibilities
1. **DAG Task Management**: Resolves dependencies between tasks (e.g. backend code cannot be generated until architecture specs exist).
2. **Execution Scheduling**: Coordinates parallel execution of non-blocking tasks.
3. **State Tracking**: Monitors task statuses (`PENDING`, `RUNNING`, `COMPLETED`, `FAILED`).
4. **Resilience & Recovery**: Manages task retries and handles graceful recovery from individual agent failures.
5. **Agent Communication**: Dispatches inputs and routes outputs/artifacts between agents.

## Implementation Architecture
- `engine.py`: Core `OrchestratorEngine` executing tasks according to topological order.
- Future phases will add distributed execution queues, state persistence (SQLite/PostgreSQL), and human-in-the-loop checkpoints.
