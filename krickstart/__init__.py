"""Legacy compatibility package alias for krickstart."""

from __future__ import annotations

import warnings

from krickstart import PLUGIN_API_VERSION, StackPlugin, __version__

warnings.warn(
    "'krickstart' has been renamed to 'krickstart'. Please update imports to 'krickstart'.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["PLUGIN_API_VERSION", "StackPlugin", "__version__"]
