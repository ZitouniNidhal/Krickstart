"""Base plugin interface for Krickstart stacks."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any


class PluginError(Exception):
    """Erreur liée aux plugins."""


class StackPlugin(ABC):
    """Interface de base qu'un stack plugin doit implémenter."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Identifiant stable du stack."""

    @property
    @abstractmethod
    def description(self) -> str:
        """Description affichée par le CLI."""

    @abstractmethod
    def default_config(self, project_name: str) -> dict[str, Any]:
        """Configuration par défaut pour ce stack."""

    @abstractmethod
    def compose_yaml(self, config: Mapping[str, Any]) -> str:
        """Génère le docker-compose.yaml pour ce stack."""

    @abstractmethod
    def env_file(self, config: Mapping[str, Any]) -> str:
        """Génère le .env pour ce stack."""

    @abstractmethod
    def post_up_hints(self, config: Mapping[str, Any]) -> list[str]:
        """Messages à afficher après le démarrage."""

    def starter_files(self, config: Mapping[str, Any]) -> dict[str, str]:
        """Fichiers de démarrage pour un nouveau projet (optionnel)."""
        return {}


__all__ = ["PluginError", "StackPlugin"]