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

__version__ = "0.0.13"


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
    set_version: bool = typer.Option(
        False,
        help="Whether to set version from main app's anvil.yaml",
    ),
):
    """Fetch an anvil app and set it as the app to run"""
    if as_dependency and not id:
        raise typer.BadParameter(
            "You must specify the app id to add it as a dependency"
        )
    try:
        api.add_submodule(url, Path("app", name), name)
        echo.progress(f"Added {name} as a submodule in the app directory")

        if as_dependency:
            api.set_dependency(id, name)

        if set_version:
            # Get main app name from config
            anvil_config = api.load(api.ANVIL_CONFIG_FILE.open(), Loader=api.Loader)
            main_app = Path(anvil_config["app"]).name
            echo.progress(f"Main app: {main_app}")

            # Get main app's anvil.yaml
            app_config = api._get_app_config(main_app)
            deps = app_config.get("dependencies", [])
            echo.progress(f"Found {len(deps)} dependencies")

            # Find this dependency's version info
            for dep in deps:
                echo.progress(f"Checking dep {dep['dep_id']}")
                if dep["dep_id"] == id:
                    version_info = dep.get("version", {})
                    version = version_info.get("version_tag") or version_info.get(
                        "version_branch"
                    )
                    echo.progress(f"Found version info: {version_info}")
                    if version:
                        api.checkout_version(name, version)
                        echo.progress(f"Checked out version {version} for {name}")
                    break
        else:
            api.set_app(name)
            echo.progress(f"Updated config to set {name} as the app")
            generated_stubs = api.generate_table_stubs(name)
            if generated_stubs:
                echo.progress(f"Created table definitions in {api.TABLE_STUB_FILE}")
        echo.done()
    except RuntimeError as e:
        echo.error(str(e))
        raise typer.Exit(1)
