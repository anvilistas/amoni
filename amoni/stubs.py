# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni
from pathlib import Path

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

__version__ = "0.0.4"

_CONFIG_FILE = Path("amoni.yaml")


def generate_tables():
    amoni_config = load(_CONFIG_FILE.open(), Loader=Loader)
    app_config_file = Path("app", amoni_config["app"], "anvil.yaml")
    app_config = load(app_config_file.open(), Loader=Loader)
    tables = app_config["db_schema"].keys()
    table_definition = [f"{t}: Table\n" for t in tables]
    content = ["from anvil.tables import Table\n\n"] + table_definition
    stub_file = Path("anvil-stubs", "tables", "app_tables.pyi")
    with Path(stub_file).open("w") as f:
        f.truncate(0)
        f.writelines(content)
    return f"Created table definitions in {stub_file}"
