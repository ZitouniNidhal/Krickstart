# [1.2.0](https://github.com/ZitouniNidhal/devspeed/compare/v1.1.0...v1.2.0) (2026-10-31)


### Features

* enhance CI/CD workflows with coverage uploads, package validation, and dependency auditing ([5d6df91](https://github.com/ZitouniNidhal/devspeed/commit/5d6df91dabef570c04cbf4f9588db48ed8a3ba7a))
* enhance package metadata and documentation with audit findings and roadmap ([0e79978](https://github.com/ZitouniNidhal/devspeed/commit/0e7997853977e8e8dc617bea187605baeb41469a))
* staff engineer audit fixes, loopback security, CI repair, and package metadata ([07edb2e](https://github.com/ZitouniNidhal/devspeed/commit/07edb2ef50e8b489332f4d2e40b49d6d5030f05e))

# [1.1.0](https://github.com/ZitouniNidhal/devspeed/compare/v1.0.0...v1.1.0) (2026-10-19)


### Bug Fixes

* **cli:** clear 'Run devspeed init <stack> first' message for up/status/logs when devspeed.yaml is missing ([77921ab](https://github.com/ZitouniNidhal/devspeed/commit/77921ab4adbde387c00497a94f13e4350de03b32))
* **cli:** fix missing imports for error classes ([efd3834](https://github.com/ZitouniNidhal/devspeed/commit/efd38340af78a998a85d55d72c050a28e818a896))
* **deps:** add pydantic and rich to project dependencies and register stacks ([4a8af25](https://github.com/ZitouniNidhal/devspeed/commit/4a8af257e4cbe14ebdf7e249df362ce20ca60654))
* resolve quality gate lint/formatting issues, Dockerfile packaging, and unit tests ([42713f1](https://github.com/ZitouniNidhal/devspeed/commit/42713f1ef7036e073c7d017d625ec5668360982f))


### Features

* add Dockerfile and container CI pipeline ([5d1152c](https://github.com/ZitouniNidhal/devspeed/commit/5d1152cbeed86e2cc064a5c02f602fa0abf67b9d))
* **cli:** add --version flag ([f12b12b](https://github.com/ZitouniNidhal/devspeed/commit/f12b12b0b9539349ebc1b84bd92483a94b347373))
* **cli:** add global --debug flag and unified DevspeedError handling in main() ([abae9b5](https://github.com/ZitouniNidhal/devspeed/commit/abae9b5acd915bacd4f8a0b363c24c0d2ed4b435))
* **cli:** consistent exit codes (0 ok, 1 user/config error, 2 environment/Docker error, 130 on Ctrl+C) ([5d5207e](https://github.com/ZitouniNidhal/devspeed/commit/5d5207e38daaa893a7a9c80547466a13f2ca75ec))
* **config:** add pydantic models for devspeed.yaml ([1abac90](https://github.com/ZitouniNidhal/devspeed/commit/1abac9071b73d964b0749cad74040b5d59bea55c))
* **doctor:** add free disk space check (warn below 2 GB) ([21a9500](https://github.com/ZitouniNidhal/devspeed/commit/21a95003ee3e367237f6411889f6bf195e8f278d))
* **doctor:** use rich table for system checks ([254a312](https://github.com/ZitouniNidhal/devspeed/commit/254a31228a7168348f55ce7ae8eadec332b537e0))
* **errors:** add DevspeedError exception hierarchy ([4fc50de](https://github.com/ZitouniNidhal/devspeed/commit/4fc50de0cee209a37443e1208e79b661d7a15d41))
* **stacks:** add express-mongodb stack ([1076519](https://github.com/ZitouniNidhal/devspeed/commit/1076519aada9a1792c0647d8f256c19f56da0d6a))
* **stacks:** add laravel-mysql stack and register new plugins ([8624310](https://github.com/ZitouniNidhal/devspeed/commit/8624310f5dc61e3d9033b5f88526297f680c878a))
* **stacks:** add spring-boot-mysql stack ([4fd88e3](https://github.com/ZitouniNidhal/devspeed/commit/4fd88e3c9d676dcc401c73872c870c25b5d6920c))

# 1.0.0 (2026-10-17)


### Bug Fixes

* correct semantic-release plugin names and installation ([1970857](https://github.com/ZitouniNidhal/devspeed/commit/197085710474d02144ea01764774e7f040505e4d))
* quote redis health check command to prevent docker pull error ([044bf0d](https://github.com/ZitouniNidhal/devspeed/commit/044bf0d0c64b967950b18fca2aa432886e7a2a04))
* resolve mypy type errors and add PyYAML stubs ([06a2e58](https://github.com/ZitouniNidhal/devspeed/commit/06a2e588225df12ac1538f96d08f741729f378f3))
* resolve ruff undefined name errors ([53fe4f2](https://github.com/ZitouniNidhal/devspeed/commit/53fe4f26c8804e0823223e36dc94293750a89080))


### Features

* add Spring Boot stack support to the registry and update README ([6d3ef11](https://github.com/ZitouniNidhal/devspeed/commit/6d3ef115e6a38f469df3b3a9292a62d32212a31d))
* add VS Code extension scaffold and publishing pipeline ([e4b78f1](https://github.com/ZitouniNidhal/devspeed/commit/e4b78f1e9e1dffb7cf215d3d7829cbdd3685c06a))
* **cli:** add devspeed export command for generating standalone Compose and env files ([837c7db](https://github.com/ZitouniNidhal/devspeed/commit/837c7dbeaaf48082ad19a77bc80ee7197b25c4be))
* **cli:** add version command, validate subcommand, and doctor --fix repair flag ([1c8f07f](https://github.com/ZitouniNidhal/devspeed/commit/1c8f07f71e60dd5976355095e0ae3136ff5dc1dd))
* enhance devspeed doctor with stale compose detection and port conflict checks ([fb0172a](https://github.com/ZitouniNidhal/devspeed/commit/fb0172a0c71ccecaaca946d0d1b2ce8ab07d2785))
* **stack:** add Spring Boot with PostgreSQL stack configuration and compose support ([e84dd93](https://github.com/ZitouniNidhal/devspeed/commit/e84dd930d70e3b8d46fb9f2878259212cfa2e4ae))
* **stacks:** add go-gin-postgres stack plugin for Go Gin REST API and PostgreSQL ([447d49b](https://github.com/ZitouniNidhal/devspeed/commit/447d49b745cb3223ef12a594bdaf51731c7831d9))
* **stacks:** add nextjs-postgres stack plugin for Next.js App Router and PostgreSQL ([6015313](https://github.com/ZitouniNidhal/devspeed/commit/6015313e45b092c1597cdea5ac564e296535a2c3))
