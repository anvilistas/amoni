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

__version__ = "0.0.6"


cmd = typer.Typer()


@cmd.command()
def app(
    url: str = typer.Argument(..., help="Clone URL for the Anvil app"),
    name: str = typer.Argument(..., help="Name of the Anvil app"),
):
    """Fetch an anvil app and set it as the app to run"""
    api.add_submodule(url, Path("app", name), name)
    echo.progress(f"Added {name} as a submodule in the app directory")
    api.set_app(name)
    echo.progress(f"Updated config to set {name} as the app")
    api.generate_table_stubs(name)
    echo.progress(f"Created table definitions in {api.TABLE_STUB_FILE}")
    echo.done()


@cmd.command()
def dependency(
    url: str = typer.Argument(..., help="Clone URL for the Anvil app"),
    name: str = typer.Argument(..., help="Name of the dependency app"),
    id: str = typer.Argument(..., help="App ID of the dependency"),
):
    """Fetch an anvil app and set it as a dependency"""
    api.add_submodule(url, Path("app", name), name)
    echo.progress(f"Added {name} as a submodule in the app directory")
    api.set_dependency(id, name)
    echo.done()
