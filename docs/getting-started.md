# 🚀 Getting Started with devspeed

Welcome to `devspeed`! This guide will take you from installation to your first running development stack in minutes.

## 1. Installation

Install `devspeed` via pip:

```bash
pip install devspeed
```

## 2. Your First Stack

The fastest way to start is using the interactive wizard:

```bash
devspeed create
```

**What happens next?**
1. You'll be asked to choose a stack (e.g., `fastapi-postgres`).
2. You'll name your project.
3. `devspeed` generates a `devspeed.yaml` file in your current directory.

## 3. Launching the Environment

Once you have your `devspeed.yaml`, simply run:

```bash
devspeed up
```

`devspeed` will:
- Generate a optimized `docker-compose.devspeed.yml`.
- Create a `.env.devspeed` with all connection strings.
- Start your containers and wait for them to be healthy.

## 4. Verifying the Setup

Run the doctor command to ensure everything is wired correctly:

```bash
devspeed doctor
```

## 5. Stopping and Cleaning Up

To stop your services but keep your data:
```bash
devspeed down
```

To wipe everything (containers, volumes, and generated files) and start fresh:
```bash
devspeed cleanup
```
