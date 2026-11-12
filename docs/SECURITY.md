# Security Architecture & Threat Model

## 1. Principles of Security

The AI Software Factory generates and executes code. This requires strict security boundaries to prevent malicious actions, privilege escalation, or resource exhaustion.

### Non-Negotiable Guardrails:
1. **Never commit secrets**: No API keys, credentials, or production tokens in version control.
2. **Never expose host credentials to generated code**: Sandboxed environments must execute with isolated, ephemeral environment variables.
3. **No unrestricted host execution**: Generated code must run inside isolated containers or lightweight virtualization.
4. **Network isolation by default**: Sandboxed code runs with `--network none` unless explicit dependency fetching is required during a pre-vetted build phase.

---

## 2. Threat Model

| Threat | Vector | Mitigation |
|---|---|---|
| **Malicious Code Generation** | Prompt injection or LLM hallucination generating destructive commands (e.g., `rm -rf /`) | Unprivileged container users (`nobody` or dedicated user), read-only root filesystems, resource limits. |
| **Credential Exfiltration** | Generated code attempting to inspect environment variables or query local metadata services | Sanitized runtime environments, no access to host `os.environ` or `.env`. |
| **Denial of Service / Fork Bomb** | Generated infinite loops, excessive thread/process creation | Strict `ulimit`, CPU limits (e.g. 1 core), memory cap (e.g. 512MB), and hard timeouts (30s). |
| **Prompt Injection** | User input manipulating agent system prompts to override safety guidelines | Separation of system instructions and user inputs via structured chat schemas and message role validation. |

---

## 3. Sandbox Isolation Policy

- **Containerization**: Execution tasks occur within minimal runtime containers (e.g. `python:3.12-alpine`).
- **Filesystem**: Working directory mounted as temporary `tmpfs` volume or isolated workspace subpath.
- **Auditing**: All stdout, stderr, exit codes, and resource metrics are logged to immutable structured logs for audit review.

