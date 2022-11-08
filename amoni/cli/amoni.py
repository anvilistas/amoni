# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni
from pathlib import Path

import typer
from cookiecutter.exceptions import OutputDirExistsException

from .. import api
from . import app, echo, theme

__version__ = "0.0.11"

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
    with echo.working("Starting anvil app and database servers"):
        api.start_service("app", detach=True)
    echo.progress("Your app is available at http://localhost:3030")
    if launch:
        typer.launch("http://localhost:3030")
    echo.done()


@cmd.command()
def stop():
    """Stop the anvil app and db servers"""
    with echo.working("Stopping anvil app and database servers"):
        api.stop_services()
    echo.done()


@cmd.command()
def test():
    """Run the test suite"""
    echo.progress("Checking for newer images")
    service = "test_runner"
    api.build_image(service)
    api.run_service(service)


@cmd.command()
def stubs(app: str = typer.Argument(..., help="App folder name")):
    """Generate stubs for the database"""
    api.generate_table_stubs(app)
    echo.progress(f"Created table definitions in {api.TABLE_STUB_FILE}")
    echo.done()
