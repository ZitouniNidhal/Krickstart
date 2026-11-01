import os
import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from krickstart import cli, config


class CliTests(unittest.TestCase):
    def test_init_creates_config_and_starter_files(self):
        with tempfile.TemporaryDirectory() as directory:
            original_directory = Path.cwd()
            os.chdir(directory)
            try:
                cli._create_config("fastapi-postgres", "test-api")
            finally:
                os.chdir(original_directory)

            self.assertTrue((Path(directory) / "krickstart.yaml").exists())
            self.assertTrue((Path(directory) / "main.py").exists())
            self.assertTrue((Path(directory) / "requirements.txt").exists())

    def test_init_does_not_overwrite_existing_starter(self):
        with tempfile.TemporaryDirectory() as directory:
            original_directory = Path.cwd()
            os.chdir(directory)
            try:
                Path("main.py").write_text("# keep this file\n")
                cli._create_config("fastapi-postgres", "test-api")
            finally:
                os.chdir(original_directory)

            self.assertEqual((Path(directory) / "main.py").read_text(), "# keep this file\n")

    def test_all_stacks_render_compose(self):
        for stack_name in (
            "node-postgres-redis",
            "fastapi-postgres",
            "django-postgres",
            "flask-postgres",
            "nextjs-postgres",
            "go-gin-postgres",
            "spring-boot-postgres",
        ):
            with self.subTest(stack=stack_name):
                stack = cli.get_stack(stack_name)
                config = stack.default_config("test-project")
                compose = stack.compose_yaml(config)
                self.assertIn("services:", compose)
                self.assertIsInstance(stack.starter_files(config), dict)

    def test_postgres_binds_to_localhost_by_default(self):
        stack = cli.get_stack("fastapi-postgres")
        config = stack.default_config("sec-test")
        compose = stack.compose_yaml(config)
        self.assertIn("127.0.0.1:", compose)

    def test_init_dry_run_does_not_write_files(self):
        with tempfile.TemporaryDirectory() as directory:
            original_directory = Path.cwd()
            os.chdir(directory)
            try:
                cli._create_config("flask-postgres", "dry-run", dry_run=True)
            finally:
                os.chdir(original_directory)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_up_generates_files_and_runs_mocked_docker(self):
        with tempfile.TemporaryDirectory() as directory:
            original_directory = Path.cwd()
            os.chdir(directory)
            try:
                config.save_config(cli.get_stack("fastapi-postgres").default_config("demo"))
                completed = type("Completed", (), {"returncode": 0})()
                with (
                    patch("krickstart.cli.shutil.which", return_value="docker"),
                    patch("krickstart.cli.subprocess.run", return_value=completed) as run,
                ):
                    cli.cmd_up(Namespace(dry_run=False))
                self.assertEqual(run.call_args.args[0][-2:], ["up", "-d"])
                self.assertTrue(Path(cli.GENERATED_COMPOSE).exists())
                self.assertTrue(Path(cli.GENERATED_ENV_EXAMPLE).exists())
                self.assertIn("<password>", Path(cli.GENERATED_ENV_EXAMPLE).read_text())
            finally:
                os.chdir(original_directory)

    def test_docker_commands_are_mocked_and_forwarded(self):
        with tempfile.TemporaryDirectory() as directory:
            original_directory = Path.cwd()
            os.chdir(directory)
            try:
                Path(cli.GENERATED_COMPOSE).write_text("services: {}\n")
                completed = type("Completed", (), {"returncode": 0})()
                with (
                    patch("krickstart.cli.shutil.which", return_value="docker"),
                    patch("krickstart.cli.subprocess.run", return_value=completed) as run,
                ):
                    with self.assertRaises(SystemExit) as down_exit:
                        cli.cmd_down(Namespace())
                    with self.assertRaises(SystemExit) as status_exit:
                        cli.cmd_status(Namespace())
                    with self.assertRaises(SystemExit) as logs_exit:
                        cli.cmd_logs(Namespace(follow=True, service="app"))
                self.assertEqual(down_exit.exception.code, 0)
                self.assertEqual(status_exit.exception.code, 0)
                self.assertEqual(logs_exit.exception.code, 0)
                self.assertEqual(run.call_count, 3)
                self.assertEqual(run.call_args.args[0][-2:], ["--follow", "app"])
            finally:
                os.chdir(original_directory)

    def test_missing_docker_message_is_actionable(self):
        with (
            patch("krickstart.cli.shutil.which", return_value=None),
            self.assertRaises(cli.DockerNotFoundError) as ctx,
        ):
            cli._require_docker()
        self.assertIn("docker.com/products/docker-desktop", str(ctx.exception))

    def test_invalid_yaml_exits_with_friendly_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / config.CONFIG_FILENAME
            path.write_text("services: [not: valid")
            with self.assertRaises(config.ConfigValidationError):
                config.load_config(Path(directory))

    def test_config_rejects_non_string_project_and_stack(self):
        with self.assertRaises(config.ConfigValidationError):
            config.validate_config({"project": 42, "stack": ["fastapi-postgres"], "services": {}})

    def test_list_and_parser_include_dry_run(self):
        output = StringIO()
        with redirect_stdout(output):
            cli.cmd_list(Namespace())
        self.assertIn("flask-postgres", output.getvalue())
        args = cli.build_parser().parse_args(["up", "--dry-run"])
        self.assertTrue(args.dry_run)

    def test_create_wizard_writes_selected_stack(self):
        with tempfile.TemporaryDirectory() as directory:
            original_directory = Path.cwd()
            os.chdir(directory)
            try:
                with patch("builtins.input", side_effect=["3", "wizard-api"]):
                    cli.cmd_create(Namespace(project_name=None, force=False, dry_run=False))
                self.assertIn("flask-postgres", Path("krickstart.yaml").read_text())
            finally:
                os.chdir(original_directory)

    def test_doctor_and_cleanup_use_mocked_docker(self):
        with tempfile.TemporaryDirectory() as directory:
            original_directory = Path.cwd()
            os.chdir(directory)
            try:
                stack = cli.get_stack("fastapi-postgres")
                cfg = stack.default_config("demo")
                config.save_config(cfg)
                Path(cli.GENERATED_COMPOSE).write_text(stack.compose_yaml(cfg), encoding="utf-8")
                Path(cli.GENERATED_ENV).write_text("DATABASE_URL=example\n")
                Path(cli.GENERATED_ENV_EXAMPLE).write_text("DATABASE_URL=example\n")
                completed = type("Completed", (), {"returncode": 0})()
                mock_usage = type("Usage", (), {"free": 50 * (1024**3)})()
                with (
                    patch("krickstart.cli.shutil.which", return_value="docker"),
                    patch("krickstart.cli.subprocess.run", return_value=completed),
                    patch("krickstart.cli.shutil.disk_usage", return_value=mock_usage),
                ):
                    cli.cmd_doctor(Namespace(fix=False))
                    cli.cmd_cleanup(Namespace())

                self.assertFalse(Path(cli.GENERATED_COMPOSE).exists())
                self.assertFalse(Path(cli.GENERATED_ENV).exists())
                self.assertFalse(Path(cli.GENERATED_ENV_EXAMPLE).exists())
            finally:
                os.chdir(original_directory)

    def test_cmd_version_outputs_version_string(self):
        output = StringIO()
        with redirect_stdout(output):
            cli.cmd_version(Namespace())
        self.assertIn("krickstart v", output.getvalue())

    def test_cmd_validate_checks_valid_config(self):
        with tempfile.TemporaryDirectory() as directory:
            original_directory = Path.cwd()
            os.chdir(directory)
            try:
                config.save_config(cli.get_stack("nextjs-postgres").default_config("validate-test"))
                output = StringIO()
                with redirect_stdout(output):
                    cli.cmd_validate(Namespace())
                self.assertIn("Configuration is valid", output.getvalue())
                self.assertIn("krickstart validate", output.getvalue())
            finally:
                os.chdir(original_directory)

    def test_doctor_fix_repairs_missing_env_example(self):
        with tempfile.TemporaryDirectory() as directory:
            original_directory = Path.cwd()
            os.chdir(directory)
            try:
                config.save_config(cli.get_stack("fastapi-postgres").default_config("demo"))
                completed = type("Completed", (), {"returncode": 0})()
                mock_usage = type("Usage", (), {"free": 50 * (1024**3)})()
                with (
                    patch("krickstart.cli.shutil.which", return_value="docker"),
                    patch("krickstart.cli.subprocess.run", return_value=completed),
                    patch("krickstart.cli.shutil.disk_usage", return_value=mock_usage),
                ):
                    cli.cmd_doctor(Namespace(fix=True))

                self.assertTrue(Path(cli.GENERATED_ENV_EXAMPLE).exists())
            finally:
                os.chdir(original_directory)

    def test_cmd_export_writes_standalone_files(self):
        with tempfile.TemporaryDirectory() as directory:
            original_directory = Path.cwd()
            os.chdir(directory)
            try:
                config.save_config(cli.get_stack("fastapi-postgres").default_config("export-demo"))
                output = StringIO()
                with redirect_stdout(output):
                    cli.cmd_export(Namespace(out="docker-compose.yml", env_out=".env"))
                self.assertTrue(Path("docker-compose.yml").exists())
                self.assertTrue(Path(".env").exists())
                self.assertIn("services:", Path("docker-compose.yml").read_text())
            finally:
                os.chdir(original_directory)


if __name__ == "__main__":
    unittest.main()
