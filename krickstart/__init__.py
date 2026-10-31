
from __future__ import annotations

import warnings

from krickstart.plugins.base import StackPlugin
__version__ = "1.2.0"
PLUGIN_API_VERSION = "1.0"

warnings.warn(
    "'krickstart' has been renamed to 'krickstart'. Please update imports to 'krickstart'.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["PLUGIN_API_VERSION", "StackPlugin", "__version__"]
