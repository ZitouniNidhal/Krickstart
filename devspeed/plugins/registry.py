"""Backward-compatibility aliases for devspeed.plugins.registry."""

from __future__ import annotations

from slipway.plugins.registry import (
    ENTRY_POINT_GROUP,
    LEGACY_ENTRY_POINT_GROUP,
    PLUGIN_API_VERSION,
    PluginError,
    PluginFactory,
    PluginRegistry,
    StackPlugin,
    builtin_registry,
    discover_pypi_stack_packages,
    pypi_package_metadata,
)

__all__ = [
    "ENTRY_POINT_GROUP",
    "LEGACY_ENTRY_POINT_GROUP",
    "PLUGIN_API_VERSION",
    "PluginError",
    "PluginFactory",
    "PluginRegistry",
    "StackPlugin",
    "builtin_registry",
    "discover_pypi_stack_packages",
    "pypi_package_metadata",
]
