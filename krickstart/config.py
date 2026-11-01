"""Configuration loader for Krickstart."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field

# Noms de fichiers
CONFIG_FILENAME = "krickstart.yaml"
LEGACY_CONFIG_FILENAME = "devspeed.yaml"


class LifecycleConfig(BaseModel):
    """Lifecycle hooks for a stack."""
    install: str | None = None
    dev: str | None = None


class ServiceConfig(BaseModel):
    """Configuration for a single service (database, cache, etc.)."""
    port: int | None = None
    db: str | None = None
    user: str | None = None
    password: str | None = None


class KrickstartConfig(BaseModel):
    """Root configuration for krickstart.yaml."""
    project: str
    stack: str
    services: dict[str, ServiceConfig] = Field(default_factory=dict)
    lifecycle: LifecycleConfig = Field(default_factory=LifecycleConfig)


def config_path() -> Path:
    """Return the path to the active configuration file."""
    if Path(CONFIG_FILENAME).exists():
        return Path(CONFIG_FILENAME)
    if Path(LEGACY_CONFIG_FILENAME).exists():
        return Path(LEGACY_CONFIG_FILENAME)
    return Path(CONFIG_FILENAME)


def load_config(path: str | Path | None = None) -> KrickstartConfig:
    """Load and parse the configuration file."""
    config_file = Path(path) if path else config_path()
    if not config_file.exists():
        raise FileNotFoundError(
            f"Aucun fichier de configuration trouvé. Lancez 'krickstart init <stack>' "
            f"pour créer {CONFIG_FILENAME}."
        )
    with config_file.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    return KrickstartConfig(**raw)


def validate_config(config: KrickstartConfig) -> None:
    """Validate the configuration (raises on invalid)."""
    if not config.project:
        raise ValueError("Le champ 'project' est obligatoire.")
    if not config.stack:
        raise ValueError("Le champ 'stack' est obligatoire.")


def save_config(config: KrickstartConfig, path: str | Path | None = None) -> Path:
    """Save the configuration to a YAML file."""
    config_file = Path(path) if path else Path(CONFIG_FILENAME)
    data = config.model_dump(exclude_none=True)
    with config_file.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False)
    return config_file