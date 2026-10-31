"""Backward-compatibility aliases for devspeed.config."""

from __future__ import annotations

from slipway.config import (
    CONFIG_FILENAME,
    LEGACY_CONFIG_FILENAME,
    DevspeedConfig,
    LifecycleConfig,
    ServiceConfig,
    SlipwayConfig,
    config_path,
    load_config,
    save_config,
    validate_config,
)

__all__ = [
    "CONFIG_FILENAME",
    "LEGACY_CONFIG_FILENAME",
    "DevspeedConfig",
    "LifecycleConfig",
    "ServiceConfig",
    "SlipwayConfig",
    "config_path",
    "load_config",
    "save_config",
    "validate_config",
]
