"""Spring Boot and MySQL stack plugin."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from devspeed.plugins.base import StackPlugin

from .common import lifecycle_command


class SpringBootMysqlPlugin(StackPlugin):
    """Provide a Java Spring Boot application with MySQL."""

    @property
    def name(self) -> str:
        return "spring-boot-mysql"

    @property
    def description(self) -> str:
        return "Java Spring Boot API + MySQL"

    def default_config(self, project_name: str) -> dict[str, Any]:
        return {
            "project": project_name,
            "stack": self.name,
            "lifecycle": {
                "install": "./mvnw clean install -DskipTests",
                "dev": "./mvnw spring-boot:run",
            },
            "services": {
                "app": {"port": 8080, "java_version": "17"},
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
            "pom.xml": '<project xmlns="http://maven.apache.org/POM/4.0.0">\n  <modelVersion>4.0.0</modelVersion>\n  <groupId>com.devspeed</groupId>\n  <artifactId>app</artifactId>\n  <version>0.0.1-SNAPSHOT</version>\n  <dependencies>\n    <dependency>\n      <groupId>org.springframework.boot</groupId>\n      <artifactId>spring-boot-starter-web</artifactId>\n    </dependency>\n    <dependency>\n      <groupId>com.mysql</groupId>\n      <artifactId>mysql-connector-j</artifactId>\n    </dependency>\n  </dependencies>\n</project>',
            "src/main/java/com/devspeed/Application.java": 'package com.devspeed;\n\nimport org.springframework.boot.SpringApplication;\nimport org.springframework.boot.autoconfigure.SpringBootApplication;\nimport org.springframework.web.bind.annotation.GetMapping;\nimport org.springframework.web.bind.annotation.RestController;\n\n@SpringBootApplication\n@RestController\npublic class Application {\n    public static void main(String[] args) { SpringApplication.run(Application.class, args); }\n\n    @GetMapping("/")\n    public String hello() { return "Your DevSpeed Spring Boot app is running"; }\n}',
        }

    def compose_yaml(self, config: Mapping[str, Any]) -> str:
        services = config["services"]
        app = services["app"]
        mysql = services["mysql"]
        project = config["project"]
        command = lifecycle_command(
            config,
            "./mvnw clean install -DskipTests",
            "./mvnw spring-boot:run",
        )
        return f"""\
name: {project}

services:
  app:
    image: eclipse-temurin:{app["java_version"]}-jdk-alpine
    working_dir: /app
    volumes:
      - ./:/app
    command: {command}
    ports:
      - "{app["port"]}:{app["port"]}"
    environment:
      - SPRING_DATASOURCE_URL=jdbc:mysql://mysql:3306/{mysql["db"]}
      - SPRING_DATASOURCE_USERNAME={mysql["user"]}
      - SPRING_DATASOURCE_PASSWORD={mysql["password"]}
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
        return f"SPRING_DATASOURCE_URL=jdbc:mysql://localhost:{mysql['port']}/{mysql['db']}\n"

    def post_up_hints(self, config: Mapping[str, Any]) -> list[str]:
        port = config["services"]["app"]["port"]
        return [
            "App container runs Maven install and spring-boot:run.",
            f"API should be reachable at http://localhost:{port} once the JVM starts.",
            "Make sure you have the Maven wrapper (mvnw) in your project root.",
        ]


plugin = SpringBootMysqlPlugin()
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
