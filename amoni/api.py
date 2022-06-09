# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni
import os
from pathlib import Path

from cookiecutter.main import cookiecutter
from pygit2 import Repository, init_repository
from python_on_whales import docker
from yaml import dump, load

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader

__version__ = "0.0.4"

COOKIECUTTER_URL = "https://github.com/anvilistas/amoni-cookiecutter.git"
ANVIL_CONFIG_FILE = Path("app", "config.yaml")
TABLE_STUB_FILE = Path("anvil-stubs", "tables", "app_tables.pyi")


def _commit_all(
    repo, message, ref=None, author=None, committer=None, tree=None, parents=None
):
    cwd = os.getcwd()
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
    repo = init_repository(directory)
    _commit_all(repo, "Initial commit", ref="HEAD", parents=[])


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
    repo = Repository(".")
    repo.add_submodule(url, path)
    _commit_all(repo, f"Add {name} submodule")


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
    repo = Repository(".")
    _commit_all(repo, f"Set {name} as the anvil app")


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
        anvil_config["dep_id"][id] = name
    except KeyError:
        anvil_config["dep_id"] = {id: name}
    dump(anvil_config, ANVIL_CONFIG_FILE.open("w"), Dumper=Dumper)
    repo = Repository(".")
    _commit_all(repo, f"Set {name} as a dependency")


def generate_table_stubs(app: str, target: Path = TABLE_STUB_FILE) -> None:
    """Generate stub entries for app tables in anvil.yaml

    Parameters
    ----------
    app
        The name of the app to generate stubs for
    target
        The stub file where the entries should be added
    """
    app_config_file = Path("app", app, "anvil.yaml")
    app_config = load(app_config_file.open(), Loader=Loader)
    tables = app_config["db_schema"]
    table_definition = [f"{t}: Table\n" for t in tables]
    content = ["from anvil.tables import Table\n\n"] + table_definition
    with Path(target).open("w") as f:
        f.truncate(0)
        f.writelines(content)
