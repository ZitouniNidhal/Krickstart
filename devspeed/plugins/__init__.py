"""Public plugin API for krickstart."""

from krickstart.plugins.base import PLUGIN_API_VERSION, PluginError, StackPlugin
from krickstart.plugins.registry import (
    ENTRY_POINT_GROUP,
    PluginRegistry,
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
