"""Legacy compatibility package alias for Slipway."""

from __future__ import annotations

import warnings

from slipway import PLUGIN_API_VERSION, StackPlugin, __version__

warnings.warn(
    "'devspeed' has been renamed to 'slipway'. Please update imports to 'slipway'.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["PLUGIN_API_VERSION", "StackPlugin", "__version__"]
