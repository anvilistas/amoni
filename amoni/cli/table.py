# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni
import typer

from .. import api
from . import echo

__version__ = "0.0.11"


cmd = typer.Typer()


@cmd.command()
def create(
    app: str = typer.Argument(..., help="Name of the anvil app"),
    table: str = typer.Argument(..., help="Name of the table to create"),
    client: str = typer.Option("none", help="Client permissions for the table"),
    server: str = typer.Option("full", help="Server permissions for the table"),
):
    """Add a new data table to an app"""
    api.add_table(app=app, name=table, client=client, server=server)
    echo.progress(f"Added data table {table} to {app}")
    echo.done()


@cmd.command()
def add_column(
    app: str = typer.Argument(..., help="Name of the anvil app"),
    table: str = typer.Argument(..., help="Name of the table to create"),
    name: str = typer.Argument(..., help="Name of the column to create"),
    data_type: str = typer.Argument(..., help="Data of the new column"),
    target: str = typer.Argument("", help="Linked table name"),
):
    """Add a new column to a data table"""
    api.add_column(app=app, table=table, name=name, data_type=data_type, target=target)
    echo.progress(f"Added {name} column to {table}")
    echo.done()
