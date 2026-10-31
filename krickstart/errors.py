"""Backward-compatibility aliases for krickstart.errors."""

from __future__ import annotations

from krickstart.errors import (
    CommandFailedError,
    ComposeNotFoundError,
    ConfigNotFoundError,
    ConfigValidationError,
    DevspeedError,
    DockerNotFoundError,
    DockerNotRunningError,
    PortConflictError,
    SlipwayError,
    UnknownStackError,
)

__all__ = [
    "CommandFailedError",
    "ComposeNotFoundError",
    "ConfigNotFoundError",
    "ConfigValidationError",
    "DevspeedError",
    "DockerNotFoundError",
    "DockerNotRunningError",
    "PortConflictError",
    "SlipwayError",
    "UnknownStackError",
]
