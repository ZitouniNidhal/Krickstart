"""Backward-compatibility aliases for krickstart.cli."""

from __future__ import annotations

from krickstart.cli import (
    GENERATED_COMPOSE,
    GENERATED_ENV,
    GENERATED_ENV_EXAMPLE,
    build_parser,
    deprecated_alias_main,
)
from krickstart.cli import deprecated_alias_main as main

__all__ = [
    "GENERATED_COMPOSE",
    "GENERATED_ENV",
    "GENERATED_ENV_EXAMPLE",
    "build_parser",
    "deprecated_alias_main",
    "main",
]
