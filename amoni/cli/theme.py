# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni

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
def build(app: str = typer.Argument(..., help="App folder name")):
    """Build the theme for the app"""
    api.build_theme(app)
    echo.progress(f"Created theme.css in app/{app}/theme/assets")
    echo.done()
