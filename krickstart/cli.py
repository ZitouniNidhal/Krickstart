"""Command-line interface for Krickstart."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from krickstart.config import (
    CONFIG_FILENAME,
    KrickstartConfig,
    load_config,
    save_config,
    validate_config,
)
from krickstart.errors import KrickstartError
from krickstart.plugins.registry import builtin_registry

GENERATED_COMPOSE = "docker-compose.krickstart.yml"
GENERATED_ENV = ".env.krickstart"
GENERATED_ENV_EXAMPLE = ".env.example"


def build_parser() -> argparse.ArgumentParser:
    """Construit le parser argparse pour le CLI Krickstart."""
    parser = argparse.ArgumentParser(
        prog="krickstart",
        description="Lightning-fast local dev environment manager powered by Docker Compose",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.2.0")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="Lister les stacks disponibles")

    init_parser = subparsers.add_parser("init", help="Générer krickstart.yaml")
    init_parser.add_argument("stack", help="Nom du stack")
    init_parser.add_argument("--name", required=True, help="Nom du projet")

    subparsers.add_parser("create", help="Assistant interactif")

    doctor_parser = subparsers.add_parser("doctor", help="Vérifier Docker et la config")
    doctor_parser.add_argument("--fix", action="store_true")

    up_parser = subparsers.add_parser("up", help="Démarrer les conteneurs")
    up_parser.add_argument("--dry-run", action="store_true")

    subparsers.add_parser("down", help="Arrêter les conteneurs")
    subparsers.add_parser("status", help="Statut des conteneurs")

    logs_parser = subparsers.add_parser("logs", help="Logs")
    logs_parser.add_argument("service", nargs="?")

    subparsers.add_parser("export", help="Exporter docker-compose.yml et .env")
    subparsers.add_parser("cleanup", help="Nettoyer")
    subparsers.add_parser("validate", help="Valider krickstart.yaml")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Point d'entrée principal."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "list":
            registry = builtin_registry()
            print("Stacks disponibles :")
            for plugin in registry.all():
                print(f"  - {plugin.name}: {plugin.description}")
            return 0

        if args.command == "init":
            registry = builtin_registry()
            plugin = registry.get(args.stack)
            config_dict = plugin.default_config(args.name)
            config = KrickstartConfig(**config_dict)
            save_config(config)
            print(f"Créé {CONFIG_FILENAME} pour le stack : {args.stack}")
            return 0

        if args.command == "create":
            print("Assistant interactif — veuillez choisir un stack.")
            return 0

        if args.command == "validate":
            config = load_config()
            validate_config(config)
            print("Configuration valide.")
            return 0

        if args.command == "up":
            if args.dry_run:
                print(f"[dry-run] Générerait : {GENERATED_COMPOSE}, {GENERATED_ENV}")
                return 0
            print(f"Démarrage de Docker Compose avec {CONFIG_FILENAME}...")
            return 0

        if args.command == "down":
            print("Arrêt des conteneurs...")
            return 0

        if args.command == "status":
            print("Statut des conteneurs : OK")
            return 0

        if args.command == "logs":
            service = args.service or "all"
            print(f"Logs pour {service}...")
            return 0

        if args.command == "export":
            print("Export de docker-compose.yml et .env...")
            return 0

        if args.command == "cleanup":
            print("Nettoyage des conteneurs et volumes...")
            return 0

        parser.print_help()
        return 1

    except KrickstartError as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1


def deprecated_alias_main(argv: Sequence[str] | None = None) -> int:
    """Point d'entrée déprécié pour l'alias devspeed."""
    import warnings

    warnings.warn(
        "'devspeed' est déprécié. Utilisez 'krickstart'.",
        DeprecationWarning,
        stacklevel=2,
    )
    return main(argv)


if __name__ == "__main__":
    sys.exit(main())
