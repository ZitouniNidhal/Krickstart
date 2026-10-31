"""Backward-compatibility aliases for devspeed.errors."""

from __future__ import annotations

from slipway.errors import (
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
