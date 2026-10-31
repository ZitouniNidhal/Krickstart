"""Laravel and MySQL stack plugin."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from slipway.plugins.base import StackPlugin

from .common import lifecycle_command


class LaravelMysqlPlugin(StackPlugin):
    """Provide a PHP Laravel application with MySQL."""

    @property
    def name(self) -> str:
        return "laravel-mysql"

    @property
    def description(self) -> str:
        return "PHP Laravel App + MySQL"

    def default_config(self, project_name: str) -> dict[str, Any]:
        return {
            "project": project_name,
            "stack": self.name,
            "lifecycle": {
                "install": "composer install",
                "dev": "php artisan serve --host 0.0.0.0 --port 8000",
            },
            "services": {
                "app": {"port": 8000, "php_version": "8.3"},
                "mysql": {
                    "port": 3306,
                    "db": project_name.replace("-", "_"),
                    "user": "devspeed",
                    "password": "devspeed",
                },
            },
        }

    def starter_files(self, config: Mapping[str, Any]) -> dict[str, str]:
        return {
            "composer.json": '{\n  "name": "devspeed/laravel",\n  "require": { "laravel/framework": "^11.0" }\n}',
            ".env": f"DB_CONNECTION=mysql\nDB_HOST=mysql\nDB_PORT=3306\nDB_DATABASE={config['services']['mysql']['db']}\nDB_USERNAME={config['services']['mysql']['user']}\nDB_PASSWORD={config['services']['mysql']['password']}\n",
        }

    def compose_yaml(self, config: Mapping[str, Any]) -> str:
        services = config["services"]
        app = services["app"]
        mysql = services["mysql"]
        project = config["project"]
        command = lifecycle_command(
            config,
            "composer install",
            "php artisan serve --host 0.0.0.0 --port 8000",
        )
        return f"""\
name: {project}

services:
  app:
    image: php:{app["php_version"]}-alpine
    working_dir: /var/www/html
    volumes:
      - ./:/var/www/html
    command: {command}
    ports:
      - "{app["port"]}:8000"
    environment:
      - DB_HOST=mysql
      - DB_DATABASE={mysql["db"]}
      - DB_USERNAME={mysql["user"]}
      - DB_PASSWORD={mysql["password"]}
    depends_on:
      mysql:
        condition: service_healthy

  mysql:
    image: mysql:8.0
    ports:
      - "{mysql["port"]}:3306"
    environment:
      - MYSQL_DATABASE={mysql["db"]}
      - MYSQL_ROOT_PASSWORD={mysql["password"]}
      - MYSQL_USER={mysql["user"]}
      - MYSQL_PASSWORD={mysql["password"]}
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 3s
      timeout: 3s
      retries: 10

volumes:
  {project}_mysqldata:
"""

    def env_file(self, config: Mapping[str, Any]) -> str:
        mysql = config["services"]["mysql"]
        return f"DB_HOST=localhost\nDB_PORT={mysql['port']}\nDB_DATABASE={mysql['db']}\nDB_USERNAME={mysql['user']}\nDB_PASSWORD={mysql['password']}\n"

    def post_up_hints(self, config: Mapping[str, Any]) -> list[str]:
        port = config["services"]["app"]["port"]
        return [
            "App container runs composer install and artisan serve.",
            f"App should be reachable at http://localhost:{port} once dependencies finish installing.",
            "Make sure you have a valid Laravel project structure.",
        ]


plugin = LaravelMysqlPlugin()
NAME = plugin.name
DESCRIPTION = plugin.description


def default_config(project_name: str) -> dict[str, Any]:
    return plugin.default_config(project_name)


def starter_files(config: Mapping[str, Any]) -> dict[str, str]:
    return plugin.starter_files(config)


def compose_yaml(config: Mapping[str, Any]) -> str:
    return plugin.compose_yaml(config)


def env_file(config: Mapping[str, Any]) -> str:
    return plugin.env_file(config)


def post_up_hints(config: Mapping[str, Any]) -> list[str]:
    return plugin.post_up_hints(config)
