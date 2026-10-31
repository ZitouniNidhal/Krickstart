"""Backward-compatibility aliases for devspeed.plugin."""

from __future__ import annotations

from slipway.plugin import (
    ENTRY_POINT_GROUP,
    PLUGIN_API_VERSION,
    PluginError,
    PluginRegistry,
    StackPlugin,
    builtin_registry,
    discover_pypi_stack_packages,
    pypi_package_metadata,
)

__all__ = [
    "ENTRY_POINT_GROUP",
    "PLUGIN_API_VERSION",
    "PluginError",
    "PluginRegistry",
    "StackPlugin",
    "builtin_registry",
    "discover_pypi_stack_packages",
    "pypi_package_metadata",
]
