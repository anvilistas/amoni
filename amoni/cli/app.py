# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni
from pathlib import Path

import typer

from .. import api
from . import echo

__version__ = "0.0.11"


cmd = typer.Typer()


@cmd.command()
def add(
    url: str = typer.Argument(..., help="Clone URL for the Anvil app"),
    name: str = typer.Argument(..., help="Name of the Anvil app"),
    id: str = typer.Argument("", help="App ID of the dependency"),
    as_dependency: bool = typer.Option(
        False,
        help="Whether to add the app as a dependency",
    ),
):
    """Fetch an anvil app and set it as the app to run"""
    if as_dependency and not id:
        raise typer.BadParameter(
            "You must specify the app id to add it as a dependency"
        )
    api.add_submodule(url, Path("app", name), name)
    echo.progress(f"Added {name} as a submodule in the app directory")
    if as_dependency:
        api.set_dependency(id, name)
    else:
        api.set_app(name)
        echo.progress(f"Updated config to set {name} as the app")
        generated_stubs = api.generate_table_stubs(name)
        if generated_stubs:
            echo.progress(f"Created table definitions in {api.TABLE_STUB_FILE}")
    echo.done()
