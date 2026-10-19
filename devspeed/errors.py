from typing import Optional

class DevspeedError(Exception):
    """Base class for all devspeed exceptions."""
    def __init__(self, message: str, hint: Optional[str] = None):
        self.message = message
        self.hint = hint
        super().__init__(self.message)

class ConfigNotFoundError(DevspeedError):
    """Raised when devspeed.yaml is missing."""
    pass

class ConfigValidationError(DevspeedError):
    """Raised when devspeed.yaml contains invalid data."""
    def __init__(self, message: str, key_path: Optional[str] = None, hint: Optional[str] = None):
        self.key_path = key_path
        super().__init__(message, hint)

class UnknownStackError(DevspeedError):
    """Raised when the requested stack is not found."""
    pass

class DockerNotFoundError(DevspeedError):
    """Raised when the Docker CLI is not installed."""
    pass

class DockerNotRunningError(DevspeedError):
    """Raised when the Docker daemon is not responding."""
    pass

class ComposeNotFoundError(DevspeedError):
    """Raised when Docker Compose v2 is not available."""
    pass

class PortConflictError(DevspeedError):
    """Raised when a required host port is already in use."""
    pass

class CommandFailedError(DevspeedError):
    """Raised when an external command (e.g. docker compose) fails."""
    pass
