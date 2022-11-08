# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni
import os
from pathlib import Path
from typing import Dict, List

import keyring
import pygit2
from cookiecutter.main import cookiecutter
from python_on_whales import docker
from yaml import dump, load

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader

__version__ = "0.0.11"

COOKIECUTTER_URL = "https://github.com/anvilistas/amoni-cookiecutter.git"
ANVIL_CONFIG_FILE = Path("app", "config.yaml")
TABLE_STUB_FILE = Path("anvil-stubs", "tables", "app_tables.pyi")


def _commit_all(
    message, repo=None, ref=None, author=None, committer=None, tree=None, parents=None
):
    cwd = os.getcwd()
    repo = repo or pygit2.Repository(".")
    os.chdir(repo.path)
    repo.index.add_all()
    repo.index.write()

    ref = ref or repo.head.name
    author = author or repo.default_signature
    committer = committer or repo.default_signature
    tree = tree or repo.index.write_tree()
    parents = parents if parents is not None else [repo.head.target]
    repo.create_commit(ref, author, committer, message, tree, parents)

    os.chdir(cwd)


def _get_app_config(app: str) -> Dict:
    config_file = Path("app", app, "anvil.yaml")
    return load(config_file.open(), Loader=Loader)


def _save_app_config(app: str, config: Dict) -> None:
    config_file = Path("app", app, "anvil.yaml")
    dump(config, config_file.open("w"), Dumper=Dumper)


def init(directory: Path, app: str) -> None:
    """Initialise an amoni project

    Parameters
    ----------
    directory
        The full path of the amoni project folder to create
    app
        The name of folder within the 'app' folder which contains the app to be run
    """
    cookiecutter(
        COOKIECUTTER_URL,
        no_input=True,
        output_dir=directory.parent,
        extra_context={"project_name": directory.name, "app_folder_name": app},
    )
    repo = pygit2.init_repository(directory)
    _commit_all("Initial commit", repo=repo, ref="HEAD", parents=[])


def pull_image(name: str) -> None:
    """Pull a docker image from the github registry

    Parameters
    ----------
    name
        The name of the image to pull
    """
    docker.compose.pull([name])


def build_image(name: str) -> None:
    """Build a docker image
    Parameters
    ----------
    name
        The name of the image to pull
    """
    docker.compose.build([name], pull=True)


def start_service(name: str, detach: bool) -> None:
    """Start a given service

    Parameters
    ----------
    name
        The name of the service to start
    detach
        Whether to detach from the service console
    """
    docker.compose.up([name], detach=detach)


def stop_services() -> None:
    """Stop all amoni services"""
    docker.compose.down()


def run_service(name: str) -> None:
    """Run a given service

    Parameters
    ----------
    name
        The name of the service to start
    """
    docker.compose.run(name)


class AmoniRemoteCallbacks(pygit2.RemoteCallbacks):
    def credentials(self, url, user, allowed_types):
        if allowed_types & pygit2.credentials.GIT_CREDENTIAL_SSH_KEY:
            credentials = {
                key: keyring.get_password(url, key)
                for key in ("username", "pubkey", "privkey", "passphrase")
            }
            if user is not None:
                credentials["username"] = user
            return pygit2.Keypair(**credentials)
        return None


def add_submodule(url: str, path: Path, name: str) -> None:
    """Add a submodule to the current repository

    Parameters
    ----------
    url
        The url of the submodule to add
    path
        The directory where the submodule should be added
    name
        The name of the submodule
    """
    repo = pygit2.Repository(".")
    repo.add_submodule(url, path, callbacks=AmoniRemoteCallbacks())
    _commit_all(f"Add {name} submodule", repo=repo)


def set_app(name: str) -> None:
    """Set the app to be run by the anvil app server

    Parameters
    ----------
    name
        The name of the app
    """
    anvil_config = load(ANVIL_CONFIG_FILE.open(), Loader=Loader)
    anvil_config["app"] = Path("/", "app", name).as_posix()
    dump(anvil_config, ANVIL_CONFIG_FILE.open("w"), Dumper=Dumper)
    _commit_all(f"Set {name} as the anvil app")


def set_dependency(id: str, name: str) -> None:
    """Set an app to be a dependency

    Parameters
    ----------
    id
        The id of the dependency app
    name
        The name of the dependency app
    """
    anvil_config = load(ANVIL_CONFIG_FILE.open(), Loader=Loader)
    try:
        anvil_config["dep-id"][id] = name
    except KeyError:
        anvil_config["dep-id"] = {id: name}
    dump(anvil_config, ANVIL_CONFIG_FILE.open("w"), Dumper=Dumper)
    _commit_all(f"Set {name} as a dependency")


def generate_table_stubs(app: str, target: Path = TABLE_STUB_FILE) -> None:
    """Generate stub entries for app tables in anvil.yaml

    Parameters
    ----------
    app
        The name of the app
    target
        The stub file where the entries should be added
    """
    config = _get_app_config(app)
    try:
        tables = config["db_schema"]
    except KeyError:
        return False
    table_definition = [f"{t}: Table\n" for t in tables]
    content = ["from anvil.tables import Table\n\n"] + table_definition
    with Path(target).open("w") as f:
        f.truncate(0)
        f.writelines(content)
    return True


def build_theme(app: str) -> None:
    """Build the theme for the given app

    Parameters
    ----------
    app
        The name of the app
    """
    docker.compose.run("theme_builder", [app])


def add_table(
    app: str,
    name: str,
    client_permissions: str = "none",
    server_permissions: str = "full",
    columns: List = None,
):
    columns = columns if columns is None else []
    config = _get_app_config(app)
    table = {
        "title": name,
        "client": client_permissions,
        "server": server_permissions,
        "columns": columns,
    }
    try:
        config["db_schema"][name] = table
    except KeyError:
        config["db_schema"] = {name: table}
    _save_app_config(app, config)
    _commit_all(f"Add {name} data table")


def add_column(app: str, table: str, name: str, data_type: str, target: str = None):
    config = _get_app_config(app)
    column = {"name": name, "admin_ui": {"width": 200}, "type": data_type}
    if not target:
        column["target"] = target
    config["db_schema"][table]["columns"].append(column)
    _save_app_config(app, config)
    _commit_all(f"Add {name} column to {table} data table")
