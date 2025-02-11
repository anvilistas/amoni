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
from dotenv import load_dotenv, set_key

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
        current_app_port, current_db_port, origin_url, env_file_found = api.get_ports()
        if not env_file_found:
            echo.warn(
                "No .env file found. Falling back to default values for app url and ports"
            )

        with echo.working("Starting anvil app and database servers"):
            api.start_service("app", detach=True)

        echo.progress(f"Your app is available at {origin_url}!")
        echo.progress(
            f"PostgreSQL database is available at localhost:{current_db_port}!"
        )
        if launch:
            echo.progress("Waiting for services to be ready...")
            time.sleep(2)
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
    os.chdir(directory)
    repo_url = typer.prompt("Enter the repository URL for your main app")
    repo_name = typer.prompt("Enter the name for your main app")

    app.add(repo_url, repo_name, as_dependency=False)

    app_config = api._get_app_config(repo_name)
    deps = app_config.get("dependencies", [])

    for dep in deps:
        dep_id = dep["dep_id"]
        package_name = dep["resolution_hints"]["package_name"]
        dep_url = typer.prompt(
            f"Enter repository URL for dependency {package_name} ({dep_id})"
        )
        app.add(dep_url, package_name, id=dep_id, as_dependency=True, set_version=True)

    app_port = typer.prompt("Enter port number for the app server", default="3030")
    db_port = typer.prompt("Enter port number for the database", default="5432")
    origin_url = typer.prompt(
        "Enter origin URL", default=f"http://localhost:{app_port}"
    )

    env_path = Path(directory, ".env")
    load_dotenv(env_path)

    set_key(env_path, "AMONI_APP_PORT", app_port)
    set_key(env_path, "AMONI_DB_PORT", db_port)
    set_key(env_path, "ORIGIN_URL", origin_url)

    api._commit_all("Update project configuration")

    echo.progress("Interactive setup completed successfully")


@cmd.command()
def stubs(app: str = typer.Argument(..., help="App folder name")):
    """Generate stubs for the database"""
    api.generate_table_stubs(app)
    echo.progress(f"Created table definitions in {api.TABLE_STUB_FILE}")
    echo.done()
