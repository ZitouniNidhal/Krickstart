from typing import Optional

class DevspeedError(Exception):
    """Base class for all devspeed exceptions."""
    def __init__(self, message: str, hint: Optional[str] = None, exit_code: int = 1):
        self.message = message
        self.hint = hint
        self.exit_code = exit_code
        super().__init__(self.message)

class ConfigNotFoundError(DevspeedError):
    """Raised when devspeed.yaml is missing."""
    def __init__(self, message: str, hint: Optional[str] = None):
        super().__init__(message, hint, exit_code=1)

class ConfigValidationError(DevspeedError):
    """Raised when devspeed.yaml contains invalid data."""
    def __init__(self, message: str, key_path: Optional[str] = None, hint: Optional[str] = None):
        self.key_path = key_path
        super().__init__(message, hint, exit_code=1)

class UnknownStackError(DevspeedError):
    """Raised when the requested stack is not found."""
    def __init__(self, message: str, hint: Optional[str] = None):
        super().__init__(message, hint, exit_code=1)

class DockerNotFoundError(DevspeedError):
    """Raised when the Docker CLI is not installed."""
    def __init__(self, message: str, hint: Optional[str] = None):
        super().__init__(message, hint, exit_code=2)

class DockerNotRunningError(DevspeedError):
    """Raised when the Docker daemon is not responding."""
    def __init__(self, message: str, hint: Optional[str] = None):
        super().__init__(message, hint, exit_code=2)

class ComposeNotFoundError(DevspeedError):
    """Raised when Docker Compose v2 is not available."""
    def __init__(self, message: str, hint: Optional[str] = None):
        super().__init__(message, hint, exit_code=2)

class PortConflictError(DevspeedError):
    """Raised when a required host port is already in use."""
    def __init__(self, message: str, hint: Optional[str] = None):
        super().__init__(message, hint, exit_code=2)

class CommandFailedError(DevspeedError):
    """Raised when an external command (e.g. docker compose) fails."""
    def __init__(self, message: str, hint: Optional[str] = None):
        super().__init__(message, hint, exit_code=2)
