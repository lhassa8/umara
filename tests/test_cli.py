"""
Tests for the CLI module.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from umara.cli import main, print_banner


class TestCLIBanner:
    """Tests for banner display."""

    def test_print_banner(self, capsys):
        """Test that banner prints without error."""
        # Should not raise
        print_banner()


class TestCLIMain:
    """Tests for main CLI group."""

    def test_main_without_command(self):
        """Test main command without subcommand shows help."""
        runner = CliRunner()
        result = runner.invoke(main)
        assert result.exit_code == 0
        assert "Umara" in result.output or "umara" in result.output.lower()

    def test_main_help(self):
        """Test help option."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "run" in result.output
        assert "init" in result.output
        assert "themes" in result.output

    def test_version(self):
        """Test version option."""
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output


class TestCLIInit:
    """Tests for init command."""

    def test_init_creates_project(self):
        """Test init creates project structure."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            result = runner.invoke(main, ["init", "test_project"])
            assert result.exit_code == 0
            assert "Project created successfully" in result.output

            # Check files were created
            project_dir = Path(tmpdir) / "test_project"
            assert project_dir.exists()
            assert (project_dir / "app.py").exists()
            assert (project_dir / "requirements.txt").exists()
            assert (project_dir / "README.md").exists()

    def test_init_default_name(self):
        """Test init with default name."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            result = runner.invoke(main, ["init"])
            assert result.exit_code == 0

            project_dir = Path(tmpdir) / "my_app"
            assert project_dir.exists()

    def test_init_existing_directory(self):
        """Test init fails on existing directory."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            # Create directory first
            (Path(tmpdir) / "existing").mkdir()
            result = runner.invoke(main, ["init", "existing"])
            assert result.exit_code == 1
            assert "already exists" in result.output

    def test_init_creates_valid_app(self):
        """Test init creates syntactically valid app.py."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            runner.invoke(main, ["init", "valid_app"])

            app_file = Path(tmpdir) / "valid_app" / "app.py"
            content = app_file.read_text()

            # Should be valid Python
            import ast

            ast.parse(content)


class TestCLIThemes:
    """Tests for themes command."""

    def test_themes_lists_builtin(self):
        """Test themes command lists built-in themes."""
        runner = CliRunner()
        result = runner.invoke(main, ["themes"])
        assert result.exit_code == 0
        assert "light" in result.output.lower()
        assert "dark" in result.output.lower()


class TestCLIDocs:
    """Tests for docs command."""

    def test_docs_opens_browser(self):
        """Test docs command attempts to open browser."""
        runner = CliRunner()
        with patch("webbrowser.open") as mock_open:
            result = runner.invoke(main, ["docs"])
            assert result.exit_code == 0
            mock_open.assert_called_once_with("https://umara.dev/docs")
            assert "Opening documentation" in result.output


class TestCLIRun:
    """Tests for run command."""

    def test_run_nonexistent_file(self):
        """Test run with nonexistent file."""
        runner = CliRunner()
        result = runner.invoke(main, ["run", "nonexistent.py"])
        # Click catches the error for non-existent path
        assert result.exit_code != 0

    def test_run_non_python_file(self):
        """Test run with non-Python file."""
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a non-Python file
            txt_file = Path(tmpdir) / "test.txt"
            txt_file.write_text("hello")

            result = runner.invoke(main, ["run", str(txt_file)])
            assert result.exit_code == 1
            assert "must be a Python file" in result.output

    def test_run_help(self):
        """Test run help."""
        runner = CliRunner()
        result = runner.invoke(main, ["run", "--help"])
        assert result.exit_code == 0
        assert "--host" in result.output
        assert "--port" in result.output
        assert "--reload" in result.output
        assert "--debug" in result.output
