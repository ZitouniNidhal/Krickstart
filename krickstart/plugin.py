"""Compatibility exports for the Krickstart plugin system."""

from __future__ import annotations

from krickstart.plugins.base import PluginError, StackPlugin
from krickstart.plugins.registry import PluginRegistry, builtin_registry

# Constantes optionnelles (si d'autres modules les importent)
ENTRY_POINT_GROUP = "krickstart.stacks"
PLUGIN_API_VERSION = "1.0"

__all__ = [
    "ENTRY_POINT_GROUP",
    "PLUGIN_API_VERSION",
    "PluginError",
    "PluginRegistry",
    "StackPlugin",
    "builtin_registry",
]
