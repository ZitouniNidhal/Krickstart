# 🛠️ Custom Stacks & Plugins

`devspeed` is designed to be extensible. You can create your own stack templates to standardize environments across your organization.

## Creating a Custom `devspeed.yaml`

You don't always need a plugin. You can manually define your infrastructure in `devspeed.yaml`:

```yaml
project: my-enterprise-app
stack: custom
services:
  api:
    port: 8000
    image: my-company/api:latest
  db:
    port: 5432
    db: app_db
    user: admin
    password: secret_password
lifecycle:
  install: npm install && npm run build
  dev: npm run dev
```

## Developing a Stack Plugin

To distribute stacks as a package, you can create a Python plugin.

### 1. Define the Stack Logic
Create a class that inherits from the `BaseStack` (or the relevant stack type). Define the services, default ports, and environment variables.

### 2. Register the Entry Point
In your `pyproject.toml`, register your stack so `devspeed` can discover it:

```toml
[project.entry-points."devspeed.stacks"]
my-custom-stack = "my_plugin.stacks.my_stack:plugin"
```

### 3. Distribution
Once published to PyPI or installed via `pip install -e .`, your stack will appear in `devspeed list`.

## Lifecycle Hooks

`devspeed` supports two primary lifecycle hooks that run inside the application container:

- `lifecycle.install`: Runs once during the initial setup (e.g., `pip install`, `npm install`).
- `lifecycle.dev`: The command that starts your application (e.g., `python main.py`, `npm run dev`).
