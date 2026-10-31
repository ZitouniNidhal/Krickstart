"""Backward-compatibility aliases for devspeed.plugins.base."""

from __future__ import annotations

from slipway.plugins.base import PLUGIN_API_VERSION, PluginError, StackPlugin

__all__ = ["PLUGIN_API_VERSION", "PluginError", "StackPlugin"]
