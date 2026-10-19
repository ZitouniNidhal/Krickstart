"""Express and MongoDB stack plugin."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from devspeed.plugins.base import StackPlugin

from .common import lifecycle_command


class ExpressMongodbPlugin(StackPlugin):
    """Provide a Node.js Express application with MongoDB."""

    @property
    def name(self) -> str:
        return "express-mongodb"

    @property
    def description(self) -> str:
        return "Node.js Express API + MongoDB"

    def default_config(self, project_name: str) -> dict[str, Any]:
        return {
            "project": project_name,
            "stack": self.name,
            "lifecycle": {
                "install": "npm install",
                "dev": "npm run dev",
            },
            "services": {
                "app": {"port": 3000, "node_version": "20"},
                "mongodb": {
                    "port": 27017,
                    "user": "devspeed",
                    "password": "devspeed",
                },
            },
        }

    def starter_files(self, config: Mapping[str, Any]) -> dict[str, str]:
        return {
            "package.json": '{\n  "name": "devspeed-express",\n  "version": "1.0.0",\n  "scripts": { "dev": "node app.js" },\n  "dependencies": { "express": "^4.19.0", "mongoose": "^8.0.0" }\n}',
            "app.js": 'const express = require("express");\nconst mongoose = require("mongoose");\n\nconst app = express();\nconst port = 3000;\n\nmongoose.connect(process.env.MONGODB_URI).then(() => console.log("Connected to MongoDB"));\n\napp.get("/", (req, res) => res.json({ message: "Your DevSpeed app is running" }));\n\napp.listen(port, () => console.log(`App listening on port ${port}`));',
        }

    def compose_yaml(self, config: Mapping[str, Any]) -> str:
        services = config["services"]
        app = services["app"]
        mongo = services["mongodb"]
        project = config["project"]
        command = lifecycle_command(
            config,
            "npm install",
            "npm run dev",
        )
        return f"""\
name: {project}

services:
  app:
    image: node:{app["node_version"]}-slim
    working_dir: /app
    volumes:
      - ./:/app
    command: {command}
    ports:
      - "{app["port"]}:{app["port"]}"
    environment:
      - MONGODB_URI=mongodb://{mongo["user"]}:{mongo["password"]}@mongodb:27017/devspeed_db?authSource=admin
    depends_on:
      mongodb:
        condition: service_healthy

  mongodb:
    image: mongo:6-alpine
    ports:
      - "{mongo["port"]}:27017"
    environment:
      - MONGO_INITDB_ROOT_USERNAME={mongo["user"]}
      - MONGO_INITDB_ROOT_PASSWORD={mongo["password"]}
    healthcheck:
      test: ["CMD", "mongo", "--eval", "db.adminCommand('ping')"]
      interval: 3s
      timeout: 3s
      retries: 10

volumes:
  {project}_mongodata:
"""

    def env_file(self, config: Mapping[str, Any]) -> str:
        mongo = config["services"]["mongodb"]
        return f"MONGODB_URI=mongodb://{mongo['user']}:{mongo['password']}@localhost:{mongo['port']}/devspeed_db?authSource=admin\n"

    def post_up_hints(self, config: Mapping[str, Any]) -> list[str]:
        port = config["services"]["app"]["port"]
        return [
            "App container runs npm install and npm run dev.",
            f"API should be reachable at http://localhost:{port} once dependencies finish installing.",
            "Make sure app.js is configured to use MONGODB_URI.",
        ]


plugin = ExpressMongodbPlugin()
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
