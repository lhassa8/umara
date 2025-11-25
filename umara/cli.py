"""
Command-line interface for Umara.

Provides commands for running Umara apps and development tools.
"""

from __future__ import annotations

import sys
import os
import importlib.util
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def print_banner():
    """Print the Umara banner."""
    banner = """
    ╦ ╦┌┬┐┌─┐┬─┐┌─┐
    ║ ║│││├─┤├┬┘├─┤
    ╚═╝┴ ┴┴ ┴┴└─┴ ┴
    """
    console.print(Panel(
        Text(banner, style="bold magenta", justify="center"),
        subtitle="Beautiful Python UIs",
        border_style="magenta",
    ))


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version="0.1.0", prog_name="Umara")
def main(ctx):
    """Umara - Beautiful Python UIs.

    Run Umara apps with: umara run app.py
    """
    if ctx.invoked_subcommand is None:
        print_banner()
        console.print("\n  Run [cyan]umara --help[/cyan] for available commands.\n")


@main.command()
@click.argument("script", type=click.Path(exists=True))
@click.option("--host", "-h", default="127.0.0.1", help="Host to bind to")
@click.option("--port", "-p", default=8501, type=int, help="Port to bind to")
@click.option("--reload/--no-reload", default=True, help="Enable hot reload")
@click.option("--debug/--no-debug", default=False, help="Enable debug mode")
def run(script: str, host: str, port: int, reload: bool, debug: bool):
    """Run an Umara application.

    Example: umara run app.py
    """
    script_path = Path(script).resolve()

    if not script_path.exists():
        console.print(f"[red]Error:[/red] Script not found: {script}")
        sys.exit(1)

    if not script_path.suffix == ".py":
        console.print(f"[red]Error:[/red] Script must be a Python file (.py)")
        sys.exit(1)

    print_banner()
    console.print(f"\n  [green]Starting Umara server...[/green]")
    console.print(f"  [dim]Script:[/dim] {script_path}")
    console.print(f"  [dim]URL:[/dim] [cyan]http://{host}:{port}[/cyan]")

    if reload:
        console.print(f"  [dim]Hot reload:[/dim] [green]enabled[/green]")

    console.print()

    # Add script directory to path
    script_dir = str(script_path.parent)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    # Load and run the app
    from umara.core import get_app
    from umara.server import run_with_reload, start_server

    app = get_app()

    # Load the user's script as a module
    spec = importlib.util.spec_from_file_location("user_app", str(script_path))
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        sys.modules["user_app"] = module

        def run_user_app():
            # Clear and reload module
            if "user_app" in sys.modules:
                # Reload by re-executing
                spec.loader.exec_module(module)

        app.set_app_function(run_user_app)

        if reload:
            run_with_reload(str(script_path), host=host, port=port, debug=debug)
        else:
            start_server(app, host=host, port=port, debug=debug)


@main.command()
@click.argument("name", default="my_app")
def init(name: str):
    """Create a new Umara project.

    Example: umara init my_app
    """
    project_dir = Path(name)

    if project_dir.exists():
        console.print(f"[red]Error:[/red] Directory '{name}' already exists")
        sys.exit(1)

    print_banner()
    console.print(f"\n  Creating new Umara project: [cyan]{name}[/cyan]\n")

    # Create project structure
    project_dir.mkdir(parents=True)

    # Create main app file
    app_content = '''"""
My Umara App
"""

import umara as um

# Set theme
um.set_theme('light')

# Header
um.header('Welcome to Umara! 👋')
um.text('Build beautiful UIs with pure Python.')

# Create a card with some interactive widgets
with um.card():
    um.subheader('Interactive Demo')

    # Text input
    name = um.input('Your name', placeholder='Enter your name...')

    # Slider
    age = um.slider('Your age', 0, 100, 25)

    # Select
    color = um.select(
        'Favorite color',
        options=['Red', 'Green', 'Blue', 'Purple'],
        default='Blue'
    )

    # Checkbox
    subscribe = um.checkbox('Subscribe to newsletter')

    # Button
    if um.button('Say Hello', variant='primary'):
        if name:
            um.success(f'Hello {name}! You are {age} years old and like {color}.')
        else:
            um.warning('Please enter your name first!')

# Two column layout
with um.columns(2):
    with um.column():
        with um.card():
            um.subheader('Column 1')
            um.text('This is the left column.')
            um.metric('Users', '1,234', delta=12.5, delta_label='vs last week')

    with um.column():
        with um.card():
            um.subheader('Column 2')
            um.text('This is the right column.')
            um.progress(75, label='Progress')

# Footer
um.divider()
um.text('Built with Umara - Beautiful Python UIs', color='#64748b', size='14px')
'''

    (project_dir / "app.py").write_text(app_content)

    # Create requirements.txt
    requirements = "umara>=0.1.0\n"
    (project_dir / "requirements.txt").write_text(requirements)

    # Create README
    readme = f"""# {name}

A beautiful web UI built with Umara.

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:
   ```bash
   umara run app.py
   ```

3. Open http://localhost:8501 in your browser.

## Learn More

- [Umara Documentation](https://umara.dev/docs)
- [Examples](https://umara.dev/examples)
"""
    (project_dir / "README.md").write_text(readme)

    console.print(f"  [green]✓[/green] Created {name}/app.py")
    console.print(f"  [green]✓[/green] Created {name}/requirements.txt")
    console.print(f"  [green]✓[/green] Created {name}/README.md")
    console.print()
    console.print("  [green]Project created successfully![/green]")
    console.print()
    console.print("  Get started:")
    console.print(f"    [cyan]cd {name}[/cyan]")
    console.print(f"    [cyan]pip install -r requirements.txt[/cyan]")
    console.print(f"    [cyan]umara run app.py[/cyan]")
    console.print()


@main.command()
def themes():
    """List available themes."""
    from umara.themes import list_themes, BUILTIN_THEMES

    print_banner()
    console.print("\n  [bold]Available Themes:[/bold]\n")

    for theme_name in list_themes():
        theme = BUILTIN_THEMES.get(theme_name)
        if theme:
            primary = theme.colors.primary
            bg = theme.colors.background
            console.print(f"  • [cyan]{theme_name}[/cyan]")
            console.print(f"    Primary: {primary}, Background: {bg}")
        else:
            console.print(f"  • [cyan]{theme_name}[/cyan] (custom)")
        console.print()


@main.command()
def docs():
    """Open Umara documentation in browser."""
    import webbrowser
    webbrowser.open("https://umara.dev/docs")
    console.print("  Opening documentation in browser...")


if __name__ == "__main__":
    main()
