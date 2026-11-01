"""Stack plugins for Krickstart."""

from __future__ import annotations


def get_registry():
    """Retourne le registre de tous les stacks disponibles."""
    from krickstart.plugins.registry import builtin_registry

    return builtin_registry()


def get_stack(name: str):
    """Retourne un stack par son nom."""
    return get_registry().get(name)


def list_stacks() -> list[tuple[str, str]]:
    """Retourne (nom, description) pour tous les stacks."""
    return [(p.name, p.description) for p in get_registry().all()]


__all__ = ["get_registry", "get_stack", "list_stacks"]
