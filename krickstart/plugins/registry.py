"""Plugin registry for Krickstart stacks."""

from __future__ import annotations

from krickstart.plugins.base import PluginError, StackPlugin


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

    def all(self) -> list[StackPlugin]:
        """Retourne tous les plugins enregistrés."""
        return list(self._plugins.values())

    def __contains__(self, name: str) -> bool:
        return name in self._plugins


def builtin_registry() -> PluginRegistry:
    """Charge et retourne le registre de tous les stacks intégrés."""
    registry = PluginRegistry()

    from krickstart.stacks.django_postgres import plugin as django_plugin
    from krickstart.stacks.express_mongodb import plugin as express_plugin
    from krickstart.stacks.fastapi_postgres import plugin as fastapi_plugin
    from krickstart.stacks.flask_postgres import plugin as flask_plugin
    from krickstart.stacks.go_gin_postgres import plugin as go_plugin
    from krickstart.stacks.laravel_mysql import plugin as laravel_plugin
    from krickstart.stacks.nextjs_postgres import plugin as nextjs_plugin
    from krickstart.stacks.node_postgres_redis import plugin as node_plugin
    from krickstart.stacks.spring_boot_mysql import plugin as spring_mysql_plugin
    from krickstart.stacks.spring_boot_postgres import plugin as spring_plugin

    registry.register(fastapi_plugin)
    registry.register(django_plugin)
    registry.register(node_plugin)
    registry.register(flask_plugin)
    registry.register(nextjs_plugin)
    registry.register(go_plugin)
    registry.register(spring_plugin)
    registry.register(express_plugin)
    registry.register(spring_mysql_plugin)
    registry.register(laravel_plugin)

    return registry


__all__ = ["PluginRegistry", "builtin_registry"]
