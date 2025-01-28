# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni
import os
import time
from pathlib import Path

import typer
from cookiecutter.exceptions import OutputDirExistsException

from .. import api
from . import app, echo, theme

__version__ = "0.0.13"

cmd = typer.Typer()
cmd.add_typer(app.cmd, name="app", help="Manage anvils apps and dependencies")
cmd.add_typer(theme.cmd, name="theme", help="Build the theme.css for an app")


@cmd.callback()
def main():
    pass


@cmd.command()
def init(
    directory: Path = typer.Argument(
        ..., file_okay=False, resolve_path=True, help="Directory to initialiase"
    ),
    app: str = typer.Argument("hello_world", help="App Folder Name"),
    interactive: bool = typer.Option(
        False,
        "--interactive",
        "-i",
        help="Use interactive setup mode that guides you through configuration",
    ),
):
    """Create the amoni folder structure and initialise a git repo there"""
    try:
        api.init(directory, app)
        echo.progress(f"Amoni project created in {directory}")

        if interactive:
            _interactive_setup(directory)

        echo.done()
    except OutputDirExistsException:
        echo.error(f"Error creating project. {directory} already exists")


@cmd.command()
def start(
    update: bool = typer.Option(False, help="Whether to update the docker images"),
    launch: bool = typer.Option(True, help="Whether to launch the app"),
):
    """Start the anvil app and db servers"""
    if update:
        typer.echo("Rebuilding server images")
        api.build_image("app")
        api.pull_image("db")
    try:
        # Get configuration before starting services to fail fast if .env is missing
        current_app_port, current_db_port, origin_url = api.get_ports()

        with echo.working("Starting anvil app and database servers"):
            api.start_service("app", detach=True)

        echo.progress(f"Your app is available at {origin_url}!")
        echo.progress(
            f"PostgreSQL database is available at localhost:{current_db_port}!"
        )
        if launch:
            echo.progress("Waiting for services to be ready...")
            time.sleep(2)  # Wait for 2 seconds before launching browser
            try:
                typer.launch(origin_url)
            except Exception:
                # Browser launch failed (e.g., no graphical interface)
                echo.progress(
                    "Browser launch failed - you can manually open the URL in your browser"
                )
        echo.done()
    except RuntimeError as e:
        echo.error(str(e))
        raise typer.Exit(1)


@cmd.command()
def stop():
    """Stop the anvil app and db servers"""
    with echo.working("Stopping anvil app and database servers"):
        api.stop_services()
    echo.done()


@cmd.command()
def test(
    update: bool = typer.Option(False, help="Whether to update the docker image"),
):
    """Run the test suite"""
    echo.progress("Checking for newer images")
    service = "test_runner"
    if update:
        api.build_image(service)
    api.run_service(service)


def _interactive_setup(directory: Path):
    """Handle the interactive setup process after project initialization.

    Parameters
    ----------
    directory : Path
        The project directory where setup is being performed
    """
    # Change to project directory
    os.chdir(directory)
    # Get main app details
    repo_url = typer.prompt("Enter the repository URL for your main app")
    repo_name = typer.prompt("Enter the name for your main app")

    # Add main app
    app.add(repo_url, repo_name, as_dependency=False)

    # Parse dependencies from main app's anvil.yaml
    app_config = api._get_app_config(repo_name)
    deps = app_config.get("dependencies", [])

    # Get dependency details
    for dep in deps:
        dep_id = dep["dep_id"]
        package_name = dep["resolution_hints"]["package_name"]
        dep_url = typer.prompt(
            f"Enter repository URL for dependency {package_name} ({dep_id})"
        )
        app.add(dep_url, package_name, id=dep_id, as_dependency=True, set_version=True)

    # Get port configurations
    app_port = typer.prompt("Enter port number for the app server", default="3030")
    db_port = typer.prompt("Enter port number for the database", default="5432")
    origin_url = typer.prompt(
        "Enter origin URL", default=f"http://localhost:{app_port}"
    )

    # Update .env file with configurations
    env_path = directory / ".env"
    if env_path.exists():
        with open(env_path) as f:
            lines = f.readlines()

        # Create a dictionary of existing variables and their values
        env_vars = {}
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _ = line.split("=", 1)
                env_vars[key] = True

        # Update or append new values
        new_content = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                new_content.append(line)
            elif "=" in line:
                key, _ = line.split("=", 1)
                if key == "AMONI_APP_PORT":
                    new_content.append(f"AMONI_APP_PORT={app_port}")
                elif key == "AMONI_DB_PORT":
                    new_content.append(f"AMONI_DB_PORT={db_port}")
                elif key == "ORIGIN_URL":
                    new_content.append(f"ORIGIN_URL={origin_url}")
                else:
                    new_content.append(line)

        # Add any missing variables
        if "AMONI_APP_PORT" not in env_vars:
            new_content.append(f"AMONI_APP_PORT={app_port}")
        if "AMONI_DB_PORT" not in env_vars:
            new_content.append(f"AMONI_DB_PORT={db_port}")
        if "ORIGIN_URL" not in env_vars:
            new_content.append(f"ORIGIN_URL={origin_url}")

        # Write back with proper line endings
        with open(env_path, "w") as f:
            f.write("\n".join(new_content) + "\n")

    # Commit changes
    api._commit_all("Update project configuration")

    echo.progress("Interactive setup completed successfully")


@cmd.command()
def stubs(app: str = typer.Argument(..., help="App folder name")):
    """Generate stubs for the database"""
    api.generate_table_stubs(app)
    echo.progress(f"Created table definitions in {api.TABLE_STUB_FILE}")
    echo.done()
