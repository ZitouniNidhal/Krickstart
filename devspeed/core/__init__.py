"""Core generation services for krickstart (legacy alias)."""

from krickstart.core.compose_generator import (
    DEFAULT_COMPOSE_FILENAME,
    DEFAULT_ENV_FILENAME,
    ComposeGenerationError,
    ComposeGenerator,
    ConfigValidationError,
    GeneratedArtifacts,
    GeneratorSettings,
    OutputFileExistsError,
    PluginResolutionError,
    PortConflictError,
    WriteResult,
)

__all__ = [
    "DEFAULT_COMPOSE_FILENAME",
    "DEFAULT_ENV_FILENAME",
    "ComposeGenerationError",
    "ComposeGenerator",
    "ConfigValidationError",
    "GeneratedArtifacts",
    "GeneratorSettings",
    "OutputFileExistsError",
    "PluginResolutionError",
    "PortConflictError",
    "WriteResult",
]
