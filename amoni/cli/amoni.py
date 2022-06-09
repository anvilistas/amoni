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
from . import install

__version__ = "0.0.4"

cmd = typer.Typer()
cmd.add_typer(install.cmd, name="install")


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
    try:
        api.init(directory, app)
        typer.echo(f"Amoni project created in {directory}")
        typer.secho("Done! ✨️", fg=typer.colors.GREEN)
    except OutputDirExistsException:
        red = typer.colors.RED
        typer.secho("⚠️ Error creating project:", fg=red)
        typer.secho(f"{directory} already exists", fg=red)


@cmd.command()
def start(
    update: bool = typer.Option(False, help="Whether to update the docker images")
):
    """Start the anvil app and db servers"""
    if update:
        typer.echo("Rebuilding server images")
        api.build_image("app")
        api.pull_image("db")
    typer.echo("Starting anvil app and database servers")
    api.start_service("app", detach=True)
    typer.echo("Your app is available at http://localhost:3030")
    typer.secho("Done! ✨️", fg=typer.colors.GREEN)


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
