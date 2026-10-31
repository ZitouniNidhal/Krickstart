"""Backward-compatibility aliases for krickstart.stacks."""

from __future__ import annotations

from krickstart.stacks import (
    STACKS,
    PluginRegistry,
    StackPlugin,
    get_registry,
    get_stack,
    list_stacks,
)

__all__ = [
    "STACKS",
    "PluginRegistry",
    "StackPlugin",
    "get_registry",
    "get_stack",
    "list_stacks",
]
