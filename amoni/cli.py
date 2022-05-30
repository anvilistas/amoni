# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni
import typer

from . import api

__version__ = "0.0.3"

amoni = typer.Typer()


@amoni.callback()
def main():
    pass


@amoni.command()
def init(
    project: str = typer.Option("", help="Project Name", prompt=True),
    app_folder_name: str = typer.Option(
        "hello_world", help="App Folder Name", prompt=True
    ),
):
    api.init(project, app_folder_name)
    typer.echo(f"amoni project created in {project} directory")


@amoni.command()
def start():
    """Start the anvil app and db servers"""
    typer.echo("Rebuilding server images")
    api.build_image("app")
    api.pull_image("db")
    typer.echo("Starting anvil app and database servers")
    api.start_service("app", detach=True)
    typer.echo("Your app is available at http://localhost:3030")


@amoni.command()
def stop():
    """Stop the anvil app and db servers"""
    typer.echo("Stopping the anvil app and database servers")
    api.stop_services()


@amoni.command()
def test():
    """Run the test suite"""
    typer.echo("Checking for newer images")
    service = "test_runner"
    api.build_image(service)
    api.run_service(service)
