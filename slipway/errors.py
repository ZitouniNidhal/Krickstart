from __future__ import annotations


class SlipwayError(Exception):
    """Base class for all Slipway exceptions."""

    def __init__(self, message: str, hint: str | None = None, exit_code: int = 1):
        self.message = message
        self.hint = hint
        self.exit_code = exit_code
        super().__init__(self.message)


class ConfigNotFoundError(SlipwayError):
    """Raised when slipway.yaml is missing."""

    def __init__(self, message: str = "slipway.yaml not found", hint: str | None = None):
        super().__init__(message, hint, exit_code=1)


class ConfigValidationError(SlipwayError):
    """Raised when slipway.yaml contains invalid data."""

    def __init__(self, message: str, key_path: str | None = None, hint: str | None = None):
        self.key_path = key_path
        super().__init__(message, hint, exit_code=1)


class UnknownStackError(SlipwayError):
    """Raised when the requested stack is not found."""

    def __init__(self, message: str, hint: str | None = None):
        super().__init__(message, hint, exit_code=1)


class DockerNotFoundError(SlipwayError):
    """Raised when the Docker CLI is not installed."""

    def __init__(self, message: str, hint: str | None = None):
        super().__init__(message, hint, exit_code=2)


class DockerNotRunningError(SlipwayError):
    """Raised when the Docker daemon is not responding."""

    def __init__(self, message: str, hint: str | None = None):
        super().__init__(message, hint, exit_code=2)


class ComposeNotFoundError(SlipwayError):
    """Raised when Docker Compose v2 is not available."""

    def __init__(self, message: str, hint: str | None = None):
        super().__init__(message, hint, exit_code=2)


class PortConflictError(SlipwayError):
    """Raised when a required host port is already in use."""

    def __init__(self, message: str, hint: str | None = None):
        super().__init__(message, hint, exit_code=2)


class CommandFailedError(SlipwayError):
    """Raised when an external command (e.g. docker compose) fails."""

    def __init__(self, message: str, hint: str | None = None):
        super().__init__(message, hint, exit_code=2)


# Backward-compatibility alias
DevspeedError = SlipwayError
