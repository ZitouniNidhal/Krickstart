# Contributing to Krickstart

Thank you for helping make local development easier to reproduce. Krickstart is a
small tool with a deliberately readable core, so contributions should improve
clarity for both first-time users and people maintaining a project at scale.

## Development setup

### 1. Clone the repository

```bash
git clone https://github.com/ZitouniNidhal/Krickstart.git
cd Krickstart
```

Replace `OWNER` with the canonical GitHub organization or user once the public
repository is created.

### 2. Create an isolated Python environment

Python 3.9 through 3.12 are supported in CI.

```bash
python -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install the project and development tools

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

The development extra contains the formatter, linter, and type checker used by
continuous integration.

### 4. Run the test suite

```bash
python -m unittest discover -s tests -v
```

Tests should pass without Docker. Docker-dependent behavior is mocked in the
unit suite; integration tests that require a running daemon must be clearly
marked and documented when they are added.

### 5. Run quality checks

```bash
python -m ruff check krickstart tests
python -m ruff format --check krickstart tests
python -m mypy krickstart
python -m compileall -q krickstart
```

Before committing a formatting change, run:

```bash
python -m ruff format krickstart tests
```

## Coding standards

### Formatting

- Use Black with the repository configuration.
- Keep lines within the configured 100-character limit where practical.
- Use four spaces and UTF-8 source files.
- Avoid unrelated formatting churn in a focused pull request.

### Type hints

- Add type hints to public functions, methods, and meaningful internal helpers.
- Prefer precise collection types such as `dict[str, Any]`, `Mapping[str, Any]`,
  and `list[str]`.
- Keep Python 3.9 compatibility; use `Optional` and `Union` where required by
  the supported interpreter range.
- Do not silence type errors broadly. If a narrow ignore is necessary, explain
  why beside the ignore.

### Docstrings

Public classes and functions should have concise Google-style docstrings that
explain purpose, arguments, return values, raised exceptions, and non-obvious
side effects. Do not add documentation that merely repeats a variable name.

### Behavior and compatibility

- Preserve existing CLI commands and configuration keys unless a breaking
  change is explicitly approved.
- Prefer actionable errors over raw tracebacks for user-facing paths.
- Keep generated files deterministic so changes can be reviewed and tested.
- Never overwrite a user's application file silently.
- Avoid network access in unit tests; mock external services and subprocesses.
- Do not commit generated Compose files, local environment files, credentials,
  virtual environments, or tool caches.

## How to add a new stack

A stack is a module in `krickstart/stacks/` that follows the existing public
shape:

- `NAME: str`
- `DESCRIPTION: str`
- `default_config(project_name: str) -> dict`
- `starter_files(config: dict) -> dict[str, str]`
- `compose_yaml(config: dict) -> str`
- `env_file(config: dict) -> str`
- `post_up_hints(config: dict) -> list[str]`

Newer stacks should implement the `StackPlugin` class in
`krickstart/plugins/base.py` and export a module-level `plugin` instance. The
module-level functions below are retained as compatibility wrappers for older
stack integrations.



### Stack checklist

Before opening a pull request for a stack:

- Use a stable lowercase `NAME` with hyphens.
- Provide safe, documented default ports and versions.
- Include health checks for stateful dependencies.
- Include restart policies through the shared generator path.
- Include hot reload where the framework supports it.
- Make starter files runnable from a clean temporary directory.
- Ensure existing project files are never overwritten.
- Add tests for default configuration, Compose rendering, environment output,
  starter files, and invalid configuration.
- Add the stack to the README catalog and roadmap if appropriate.

## Pull request guidelines

Keep pull requests small and focused. A good PR should explain the user problem,
the chosen solution, and how it was verified.

Before opening a PR:

1. Rebase or update from the current default branch.
2. Run the full test suite.
3. Run Black, Ruff, mypy, and compile checks locally.
4. Review the diff for generated files, credentials, and unrelated changes.
5. Update documentation when user-visible behavior changes.
6. Add a migration note for breaking CLI or configuration changes.

Every behavior change should include tests. Documentation-only changes may omit
unit tests but should include a clear manual verification note.

CI runs on every push and pull request across Python 3.9 through 3.12 and
Ubuntu, Windows, and macOS. It installs the package, checks formatting, runs
Ruff, runs mypy, compiles the package, and executes the test suite.

## Issue triage and labels

Maintainers review new issues regularly and apply labels based on scope:

- `bug`: confirmed incorrect behavior.
- `documentation`: missing, misleading, or unclear documentation.
- `enhancement`: improvement to existing behavior.
- `new-stack`: request or work for a stack template.
- `plugin`: extension API or third-party integration.
- `good first issue`: scoped work suitable for a new contributor.
- `help wanted`: useful work where community assistance is welcome.
- `needs-reproduction`: not enough information to reproduce the report.
- `blocked`: dependent on an external decision or upstream change.

Triage normally follows this sequence:

1. Confirm that the report applies to the current default branch.
2. Request a minimal reproduction when behavior cannot be reproduced.
3. Identify severity, affected platforms, and whether data can be lost.
4. Assign labels and a milestone when the scope is understood.
5. Link duplicate issues and close them with a pointer to the canonical issue.
6. Convert accepted roadmap work into a focused issue with acceptance criteria.

Security vulnerabilities should not be posted publicly. Use the repository's
private security reporting channel when it is enabled, or contact the
maintainers through the address published in the GitHub security policy.

## Code review expectations

Reviewers focus on correctness, compatibility, tests, security, and user
clarity. Review comments should be specific and explain the reason for a
requested change. Contributors are encouraged to ask questions and revise
incrementally; a review is a collaboration, not a gatekeeping exercise.

## License

By contributing, you agree that your contribution will be licensed under the
MIT License used by this project.
