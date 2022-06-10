# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni
from functools import partial
from pathlib import Path

import typer
from cookiecutter.exceptions import OutputDirExistsException

from .. import api
from . import install

__version__ = "0.0.5"

cmd = typer.Typer()
cmd.add_typer(install.cmd, name="install", help="Install an anvil app or dependency")

_error = partial(typer.secho, fg=typer.colors.RED, err=True)
_success = partial(typer.secho, fg=typer.colors.GREEN)
_progress = partial(typer.secho, fg=typer.colors.CYAN)
_done = partial(_success, "Done! ✨️")


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
        _progress(f"Amoni project created in {directory}")
        _done()
    except OutputDirExistsException:
        _error("Error creating project:")
        _error(f"{directory} already exists")


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
    _progress("Starting anvil app and database servers")
    api.start_service("app", detach=True)
    _progress("Your app is available at http://localhost:3030")
    if launch:
        _progress("Launching app")
        typer.launch("http://localhost:3030")
    _done()


@cmd.command()
def stop():
    """Stop the anvil app and db servers"""
    typer.echo("Stopping the anvil app and database servers")
    api.stop_services()
    typer.secho("Done! ✨️", fg=typer.colors.GREEN)


@cmd.command()
def test():
    """Run the test suite"""
    typer.echo("Checking for newer images")
    service = "test_runner"
    api.build_image(service)
    api.run_service(service)


@cmd.command()
def stubs(app: str = typer.Argument(..., help="App folder name")):
    """Generate stubs for the database"""
    api.generate_table_stubs(app)
    typer.echo(f"Created table definitions in {api.TABLE_STUB_FILE}")
    typer.secho("Done! ✨️", fg=typer.colors.GREEN)
