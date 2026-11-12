from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class IsolationLevel(str, Enum):
    PROCESS_RESTRICTED = "process_restricted"
    CONTAINER = "container"
    VIRTUAL_MACHINE = "virtual_machine"


@dataclass
class ExecutionLimits:
    timeout_seconds: float = 30.0
    max_memory_mb: int = 512
    max_cpu_cores: float = 1.0
    allow_network: bool = False
    read_only_root: bool = True


@dataclass
class ExecutionResult:
    exit_code: int
    stdout: str
    stderr: str
    execution_time_seconds: float
    timed_out: bool = False
    memory_peak_mb: float = 0.0


@dataclass
class SandboxPolicy:
    """
    Security contract that must be validated prior to launching any
    generated code inside the sandbox.
    """
    isolation_level: IsolationLevel = IsolationLevel.CONTAINER
    limits: ExecutionLimits = field(default_factory=ExecutionLimits)
    allowed_write_paths: list[Path] = field(default_factory=list)

    def validate_environment(self, env_vars: dict[str, str]) -> dict[str, str]:
        """
        Sanitizes environment variables before injection into the sandbox.
        Strips out all sensitive API keys and host credentials.
        """
        forbidden_substrings = ("KEY", "SECRET", "TOKEN", "PASSWORD", "CREDENTIAL", "AUTH")
        sanitized = {}
        for k, v in env_vars.items():
            if any(forbidden in k.upper() for forbidden in forbidden_substrings):
                continue
            sanitized[k] = v
        return sanitized
