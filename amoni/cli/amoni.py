# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni
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
):
    """Create the amoni folder structure and initialise a git repo there"""
    try:
        api.init(directory, app)
        echo.progress(f"Amoni project created in {directory}")
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


@cmd.command()
def stubs(app: str = typer.Argument(..., help="App folder name")):
    """Generate stubs for the database"""
    api.generate_table_stubs(app)
    echo.progress(f"Created table definitions in {api.TABLE_STUB_FILE}")
    echo.done()
