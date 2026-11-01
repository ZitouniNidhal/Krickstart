
"""Base plugin interface for Krickstart stacks."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


class PluginError(Exception):
    """Erreur liée aux plugins."""


@runtime_checkable
class StackPlugin(Protocol):
    """Interface qu'un stack plugin doit implémenter."""

    name: str
    description: str

    def default_config(self) -> dict[str, Any]:
        """Retourne la configuration par défaut pour ce stack."""
        ...

    def compose_yaml(self, config: dict[str, Any]) -> str:
        """Génère le contenu docker-compose.yaml pour ce stack."""
        ...

    def env_file(self, config: dict[str, Any]) -> str:
        """Génère le contenu du .env pour ce stack."""
        ...

    def post_up_hints(self) -> str:
        """Retourne un message à afficher après le démarrage."""
        ...


__all__ = ["PluginError", "StackPlugin"]