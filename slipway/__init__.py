"""Slipway: Lightning-fast local dev environment manager powered by Docker Compose."""

from slipway.plugins.base import PLUGIN_API_VERSION, StackPlugin

__version__ = "1.2.0"

__all__ = ["PLUGIN_API_VERSION", "StackPlugin", "__version__"]
