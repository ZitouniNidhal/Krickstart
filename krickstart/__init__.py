"""Stack plugins for Krickstart."""

from __future__ import annotations

from krickstart.plugins.registry import PluginRegistry


def get_registry() -> PluginRegistry:
    """Retourne le registre de tous les stacks disponibles."""
    registry = PluginRegistry()

    from krickstart.stacks.fastapi_postgres import plugin as fastapi_plugin
    from krickstart.stacks.django_postgres import plugin as django_plugin
    from krickstart.stacks.node_postgres_redis import plugin as node_plugin
    from krickstart.stacks.flask_postgres import plugin as flask_plugin
    from krickstart.stacks.nextjs_postgres import plugin as nextjs_plugin
    from krickstart.stacks.go_gin_postgres import plugin as go_plugin
    from krickstart.stacks.spring_boot_postgres import plugin as spring_plugin
    from krickstart.stacks.express_mongodb import plugin as express_plugin
    from krickstart.stacks.spring_boot_mysql import plugin as spring_mysql_plugin
    from krickstart.stacks.laravel_mysql import plugin as laravel_plugin

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


__all__ = ["get_registry"]