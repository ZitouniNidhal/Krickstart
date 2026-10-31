"""Plugin discovery and registry management for Slipway."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from collections.abc import Callable
from html.parser import HTMLParser
from importlib.metadata import EntryPoint, entry_points
from typing import Any

from slipway.plugins.base import PLUGIN_API_VERSION, PluginError, StackPlugin

ENTRY_POINT_GROUP = "slipway.stacks"
LEGACY_ENTRY_POINT_GROUP = "devspeed.stacks"
PYPI_SIMPLE_INDEX = "https://pypi.org/simple/"


class _SimpleIndexParser(HTMLParser):
    """Extract package names from the PyPI simple repository index."""

    def __init__(self) -> None:
        super().__init__()
        self.packages: list[str] = []

    def handle_data(self, data: str) -> None:
        package = data.strip()
        if package.startswith(("slipway-stack-", "devspeed-stack-")):
            self.packages.append(package)


class PluginRegistry:
    """Registry of validated built-in and installed third-party plugins."""

    def __init__(self) -> None:
        self._plugins: dict[str, StackPlugin] = {}
        self.errors: list[str] = []

    def register(self, plugin: StackPlugin, *, replace: bool = False) -> StackPlugin:
        """Validate and register ``plugin`` under its stable name.

        Duplicate names fail by default so an installed package cannot silently
        replace a built-in or approved plugin. ``replace=True`` is reserved for
        explicitly configured application-level overrides.
        """
        plugin.validate()
        if plugin.name in self._plugins and not replace:
            raise PluginError(f"duplicate stack plugin name: {plugin.name}")
        self._plugins[plugin.name] = plugin
        return plugin

    def discover(self) -> PluginRegistry:
        """Load all installed ``slipway.stacks`` and legacy ``devspeed.stacks`` entry points.

        A broken optional plugin is recorded in ``errors`` and does not prevent
        healthy plugins from loading. This keeps ``slipway list`` usable when a
        user has an unrelated, partially installed extension.
        """
        for point in _entry_points():
            distribution = getattr(getattr(point, "dist", None), "name", None)
            if distribution in ("slipway", "devspeed"):
                continue
            try:
                self.register(_coerce_plugin(point.load()))
            except (AttributeError, ImportError, PluginError, TypeError) as error:
                self.errors.append(f"{point.name}: {error}")
        return self

    def get(self, name: str) -> StackPlugin:
        """Return a plugin by name or raise an actionable ``KeyError``."""
        if name not in self._plugins:
            available = ", ".join(sorted(self._plugins)) or "none"
            raise KeyError(f"Unknown stack '{name}'. Available stacks: {available}")
        return self._plugins[name]

    def all(self) -> list[StackPlugin]:
        """Return registered plugins in discovery order."""
        return list(self._plugins.values())


def _entry_points() -> list[EntryPoint]:
    """Read entry points across supported importlib.metadata APIs for both groups."""
    discovered = entry_points()
    points: list[EntryPoint] = []
    seen_names: set[str] = set()

    for group in (ENTRY_POINT_GROUP, LEGACY_ENTRY_POINT_GROUP):
        group_points: list[EntryPoint] = []
        if hasattr(discovered, "select"):
            group_points = list(discovered.select(group=group))
        else:
            group_points = list(discovered.get(group, []))  # type: ignore[attr-defined]

        for p in group_points:
            if p.name not in seen_names:
                points.append(p)
                seen_names.add(p.name)

    return points


def _coerce_plugin(value: Any) -> StackPlugin:
    """Convert an entry-point value into a validated plugin instance."""
    if isinstance(value, StackPlugin):
        plugin = value
    elif isinstance(value, type) and issubclass(value, StackPlugin):
        plugin = value()
    elif callable(value):
        plugin = value()
        if not isinstance(plugin, StackPlugin):
            raise PluginError("entry point factory did not return a StackPlugin")
    else:
        raise PluginError("entry point must expose a StackPlugin or factory")
    plugin.validate()
    return plugin


def builtin_registry() -> PluginRegistry:
    """Return a registry pre-loaded with built-in stack plugins.

    Built-ins are imported explicitly to ensure they are always available
    without relying on entry-point discovery.
    """
    registry = PluginRegistry()
    from slipway.stacks.django_postgres import DjangoPostgresPlugin
    from slipway.stacks.express_mongodb import ExpressMongodbPlugin
    from slipway.stacks.fastapi_postgres import FastAPIPostgresPlugin
    from slipway.stacks.flask_postgres import FlaskPostgresPlugin
    from slipway.stacks.go_gin_postgres import GoGinPostgresPlugin
    from slipway.stacks.laravel_mysql import LaravelMysqlPlugin
    from slipway.stacks.nextjs_postgres import NextjsPostgresPlugin
    from slipway.stacks.node_postgres_redis import NodePostgresRedisPlugin
    from slipway.stacks.spring_boot_mysql import SpringBootMysqlPlugin
    from slipway.stacks.spring_boot_postgres import SpringBootPostgresPlugin

    registry.register(DjangoPostgresPlugin())
    registry.register(FastAPIPostgresPlugin())
    registry.register(FlaskPostgresPlugin())
    registry.register(GoGinPostgresPlugin())
    registry.register(NextjsPostgresPlugin())
    registry.register(NodePostgresRedisPlugin())
    registry.register(SpringBootPostgresPlugin())
    registry.register(ExpressMongodbPlugin())
    registry.register(SpringBootMysqlPlugin())
    registry.register(LaravelMysqlPlugin())
    return registry


def discover_pypi_stack_packages(timeout: float = 5.0) -> list[str]:
    """Return published package names using the stack package naming convention."""
    request = urllib.request.Request(PYPI_SIMPLE_INDEX, headers={"User-Agent": "slipway"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        parser = _SimpleIndexParser()
        parser.feed(response.read().decode("utf-8"))
    return sorted(set(parser.packages))


def pypi_package_metadata(package_name: str, timeout: float = 5.0) -> dict[str, Any]:
    """Fetch metadata for one PyPI package without installing it."""
    encoded_name = urllib.parse.quote(package_name)
    request = urllib.request.Request(
        f"https://pypi.org/pypi/{encoded_name}/json", headers={"User-Agent": "slipway"}
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload["info"]


PluginFactory = Callable[[], StackPlugin]
__all__ = [
    "ENTRY_POINT_GROUP",
    "LEGACY_ENTRY_POINT_GROUP",
    "PLUGIN_API_VERSION",
    "PluginError",
    "PluginFactory",
    "PluginRegistry",
    "StackPlugin",
    "builtin_registry",
    "discover_pypi_stack_packages",
    "pypi_package_metadata",
]
