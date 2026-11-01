"""Error classes for Krickstart."""

from __future__ import annotations


class KrickstartError(Exception):
    """Base exception for all Krickstart errors."""


# Alias de compatibilité (anciens noms)
DevspeedError = KrickstartError
SlipwayError = KrickstartError


class ConfigNotFoundError(KrickstartError):
    """Configuration file not found."""


class ConfigValidationError(KrickstartError):
    """Configuration is invalid."""


class ComposeNotFoundError(KrickstartError):
    """Docker Compose file not found."""


class DockerNotFoundError(KrickstartError):
    """Docker is not installed."""


class DockerNotRunningError(KrickstartError):
    """Docker daemon is not running."""


class PortConflictError(KrickstartError):
    """A port is already in use."""


class UnknownStackError(KrickstartError):
    """The requested stack does not exist."""


class CommandFailedError(KrickstartError):
    """A subprocess command failed."""


__all__ = [
    "CommandFailedError",
    "ComposeNotFoundError",
    "ConfigNotFoundError",
    "ConfigValidationError",
    "DevspeedError",
    "DockerNotFoundError",
    "DockerNotRunningError",
    "KrickstartError",
    "PortConflictError",
    "SlipwayError",
    "UnknownStackError",
]