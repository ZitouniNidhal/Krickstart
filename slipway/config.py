from __future__ import annotations

import difflib
import pathlib
from typing import Any

import yaml
from pydantic import BaseModel, Field, ValidationError, field_validator

from slipway.errors import ConfigNotFoundError, ConfigValidationError

CONFIG_FILENAME = "slipway.yaml"
LEGACY_CONFIG_FILENAME = "devspeed.yaml"


class ServiceConfig(BaseModel):
    port: int | None = Field(None, ge=1, le=65535)
    db: str | None = None
    user: str | None = None
    password: str | None = None
    image: str | None = None
    node_version: str | None = None
    python_version: str | None = None


class LifecycleConfig(BaseModel):
    install: str | None = None
    dev: str | None = None


class SlipwayConfig(BaseModel):
    project: str = Field(..., min_length=1)
    stack: str = Field(..., min_length=1)
    services: dict[str, ServiceConfig] = Field(default_factory=dict)
    lifecycle: LifecycleConfig | None = None

    @field_validator("project")
    @classmethod
    def validate_project_name(cls, v: str) -> str:
        if any(char in v for char in ' /\\:;*?"<>|'):
            raise ValueError("Project name contains invalid characters")
        return v


DevspeedConfig = SlipwayConfig


def config_path(directory: pathlib.Path | None = None) -> pathlib.Path:
    dir_path = directory or pathlib.Path.cwd()
    primary = dir_path / CONFIG_FILENAME
    if primary.exists():
        return primary
    legacy = dir_path / LEGACY_CONFIG_FILENAME
    if legacy.exists():
        return legacy
    return primary


def load_config(directory: pathlib.Path | None = None) -> dict[str, Any]:
    path = config_path(directory)
    if not path.exists():
        raise ConfigNotFoundError(
            f"No {CONFIG_FILENAME} (or {LEGACY_CONFIG_FILENAME}) found in {path.parent}.",
            hint="Run 'slipway init <stack>' or 'slipway create' to start.",
        )
    filename = path.name
    try:
        with path.open(encoding="utf-8") as f:
            raw_config = yaml.safe_load(f)
    except (OSError, yaml.YAMLError) as load_error:
        raise ConfigValidationError(f"Could not read {filename}: {load_error}")

    if not isinstance(raw_config, dict):
        raise ConfigValidationError(f"The {filename} file must contain a YAML object.")

    # Check for unknown keys and suggest corrections
    known_keys = {"project", "stack", "services", "lifecycle"}
    actual_keys = set(raw_config.keys())
    unknown_keys = actual_keys - known_keys
    if unknown_keys:
        for key in unknown_keys:
            suggestions = difflib.get_close_matches(key, list(known_keys))
            if suggestions:
                pass

    try:
        validated = SlipwayConfig(**raw_config)
        return validated.model_dump()
    except ValidationError as e:
        err = e.errors()[0]
        loc = ".".join(str(x) for x in err["loc"])
        msg = err["msg"]
        raise ConfigValidationError(
            f"{loc}: {msg}", key_path=loc, hint=f"Check the value of '{loc}' in {filename}."
        )


def save_config(config: dict[str, Any], directory: pathlib.Path | None = None) -> pathlib.Path:
    path = config_path(directory)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, sort_keys=False)
    return path


def validate_config(config_data: dict[str, Any]) -> dict[str, Any]:
    """Validate a configuration dictionary using the Pydantic model."""
    try:
        validated = SlipwayConfig(**config_data)
        return validated.model_dump()
    except ValidationError as e:
        err = e.errors()[0]
        loc = ".".join(str(x) for x in err["loc"])
        msg = err["msg"]
        raise ConfigValidationError(
            f"{loc}: {msg}", key_path=loc, hint=f"Check the value of '{loc}' in {CONFIG_FILENAME}."
        )
