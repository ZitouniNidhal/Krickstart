"""Plugin system for Krickstart.

Fournit l'interface StackPlugin, un PluginRegistry, et la découverte
automatique via les entry points Python.
"""

from __future__ import annotations

import importlib.metadata
from typing import Any, Protocol, runtime_checkable

# Constantes
ENTRY_POINT_GROUP = "krickstart.stacks"
PLUGIN_API_VERSION = "1.0"


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


class PluginRegistry:
    """Registre des stack plugins disponibles."""

    def __init__(self) -> None:
        self._plugins: dict[str, StackPlugin] = {}

    def register(self, plugin: StackPlugin) -> None:
        """Enregistre un plugin."""
        if not plugin.name:
            raise PluginError("Le plugin doit avoir un nom non vide.")
        self._plugins[plugin.name] = plugin

    def get(self, name: str) -> StackPlugin:
        """Récupère un plugin par nom."""
        if name not in self._plugins:
            raise PluginError(f"Stack inconnu : {name}")
        return self._plugins[name]

    def list(self) -> list[StackPlugin]:
        """Liste tous les plugins enregistrés."""
        return list(self._plugins.values())

    def __contains__(self, name: str) -> bool:
        return name in self._plugins


def builtin_registry() -> PluginRegistry:
    """Charge les stacks intégrés de Krickstart."""
    registry = PluginRegistry()

    try:
        from krickstart.stacks.fastapi_postgres import plugin as fastapi_plugin

        registry.register(fastapi_plugin)
    except ImportError:
        pass

    try:
        from krickstart.stacks.django_postgres import plugin as django_plugin

        registry.register(django_plugin)
    except ImportError:
        pass

    try:
        from krickstart.stacks.node_postgres_redis import plugin as node_plugin

        registry.register(node_plugin)
    except ImportError:
        pass

    try:
        from krickstart.stacks.flask_postgres import plugin as flask_plugin

        registry.register(flask_plugin)
    except ImportError:
        pass

    try:
        from krickstart.stacks.nextjs_postgres import plugin as nextjs_plugin

        registry.register(nextjs_plugin)
    except ImportError:
        pass

    try:
        from krickstart.stacks.go_gin_postgres import plugin as go_plugin

        registry.register(go_plugin)
    except ImportError:
        pass

    try:
        from krickstart.stacks.spring_boot_postgres import plugin as spring_plugin

        registry.register(spring_plugin)
    except ImportError:
        pass

    try:
        from krickstart.stacks.express_mongodb import plugin as express_plugin

        registry.register(express_plugin)
    except ImportError:
        pass

    try:
        from krickstart.stacks.spring_boot_mysql import plugin as spring_mysql_plugin

        registry.register(spring_mysql_plugin)
    except ImportError:
        pass

    try:
        from krickstart.stacks.laravel_mysql import plugin as laravel_plugin

        registry.register(laravel_plugin)
    except ImportError:
        pass

    return registry


def discover_pypi_stack_packages() -> list[StackPlugin]:
    """Découvre les plugins installés via les entry points."""
    plugins: list[StackPlugin] = []
    for entry_point in importlib.metadata.entry_points(group=ENTRY_POINT_GROUP):
        try:
            plugin = entry_point.load()
            plugins.append(plugin)
        except Exception as exc:  # noqa: BLE001
            import logging

            logging.getLogger(__name__).warning(
                "Failed to load plugin %s: %s", entry_point.name, exc
            )
        continue
    return plugins


def pypi_package_metadata(package_name: str) -> dict[str, Any]:
    """Récupère les métadonnées d'un package PyPI (nom, version, description)."""
    try:
        metadata = importlib.metadata.metadata(package_name)
        return {
            "name": metadata.get("Name", package_name),
            "version": metadata.get("Version", "unknown"),
            "description": metadata.get("Summary", ""),
        }
    except importlib.metadata.PackageNotFoundError:
        return {"name": package_name, "version": "not installed", "description": ""}


__all__ = [
    "ENTRY_POINT_GROUP",
    "PLUGIN_API_VERSION",
    "PluginError",
    "PluginRegistry",
    "StackPlugin",
    "builtin_registry",
    "discover_pypi_stack_packages",
    "pypi_package_metadata",
]
