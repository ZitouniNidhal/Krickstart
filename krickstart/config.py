from __future__ import annotations

import pathlib
from typing import Any, Optional

import yaml

from krickstart.errors import ConfigValidationError

CONFIG_FILENAME = "krickstart.yaml"


def config_path(directory: Optional[pathlib.Path] = None) -> pathlib.Path:  # noqa: UP045
    directory = directory or pathlib.Path.cwd()
    return directory / CONFIG_FILENAME


def load_config(directory: Optional[pathlib.Path] = None) -> dict[str, Any]:  # noqa: UP045
    """Charge et valide la configuration depuis krickstart.yaml."""

    path = config_path(directory)
    if not path.exists():
        raise ConfigValidationError(
            f"No {CONFIG_FILENAME} found in {path.parent}. Run 'krickstart init <stack>' first."
        )
    try:
        with path.open(encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except (OSError, yaml.YAMLError) as load_error:
        raise ConfigValidationError(
            f"Could not read {CONFIG_FILENAME}: invalid YAML ({load_error})."
        ) from load_error
    if not isinstance(config, dict):
        raise ConfigValidationError(
            f"{CONFIG_FILENAME} must contain a YAML mapping at the top level."
        )
    project = config.get("project")
    stack = config.get("stack")
    if not isinstance(project, str) or not project.strip():
        raise ConfigValidationError("'project' must be a non-empty string.")
    if not isinstance(stack, str) or not stack.strip():
        raise ConfigValidationError("'stack' must be a non-empty string.")
    return config


def validate_config(config: dict[str, Any]) -> None:
    """Valide la configuration avant de la passer au générateur.

    Lève ConfigValidationError si project ou stack n'est pas une string non vide.
    """

    if not isinstance(config, dict):
        raise ConfigValidationError("Configuration must be a mapping.")
    project = config.get("project")
    stack = config.get("stack")
    if not isinstance(project, str) or not project.strip():
        raise ConfigValidationError("'project' must be a non-empty string.")
    if not isinstance(stack, str) or not stack.strip():
        raise ConfigValidationError("'stack' must be a non-empty string.")


def save_config(
    config: dict[str, Any],
    directory: Optional[pathlib.Path] = None,  # noqa: UP045
) -> pathlib.Path:
    path = config_path(directory)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, sort_keys=False)
    return path
