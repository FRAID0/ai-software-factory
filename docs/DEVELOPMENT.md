# Developer Guide & Contribution Standards

## 1. Local Setup

### System Prerequisites
- Python 3.12+
- Git
- Docker (recommended for running tests against sandbox environments)

### Setup Steps
```bash
# Clone the repository
git clone git@github.com:FRAID0/ai-software-factory.git
cd ai-software-factory

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies in editable mode
pip install -e ".[dev]"

# Configure environment variables
cp .env.example .env
```

---

## 2. Engineering Standards

- **Typing**: Use standard Python type hints (`int`, `str`, `list[T]`, `dict[K, V]`). Avoid `Any` wherever possible.
- **Data Validation**: Use `pydantic.BaseModel` for all schemas transmitted across boundaries.
- **Formatting & Linting**: Ruff is the standard linter and formatter.
  ```bash
  ruff check .
  ruff format --check .
  ```
- **Type Checking**: Mypy must pass in strict mode.
  ```bash
  mypy shared orchestrator model_gateway agents
  ```
- **Testing**: Pytest for all tests.
  ```bash
  pytest
  ```

---

## 3. Git Workflow & Commits

We follow the **Conventional Commits** specification:
- `feat:` A new feature or capability.
- `fix:` A bug fix.
- `docs:` Documentation updates only.
- `refactor:` Code change that neither fixes a bug nor adds a feature.
- `test:` Adding missing tests or correcting existing tests.
- `chore:` Tooling, CI, dependencies, or repository configuration.

