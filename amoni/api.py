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
AMONI_CONFIG_FILE = Path("amoni.yaml")
ANVIL_CONFIG_FILE = Path("app", "config.yaml")


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


def add_submodule(url, path, name):
    repo = Repository(".")
    repo.add_submodule(url, path)
    _commit_all(repo, f"Add {name} submodule")


def set_app(name: str):
    amoni_config = load(AMONI_CONFIG_FILE.open(), Loader=Loader)
    anvil_config = load(ANVIL_CONFIG_FILE.open(), Loader=Loader)
    amoni_config["app"] = name
    anvil_config["app"] = Path("/", "app", name).as_posix()
    dump(amoni_config, AMONI_CONFIG_FILE.open("w"), Dumper=Dumper)
    dump(anvil_config, ANVIL_CONFIG_FILE.open("w"), Dumper=Dumper)
    repo = Repository(".")
    _commit_all(repo, f"Set {name} as the anvil app")


def set_dependency(id: str, name: str):
    anvil_config = load(ANVIL_CONFIG_FILE.open(), Loader=Loader)
    try:
        anvil_config["dep_id"][id] = name
    except KeyError:
        anvil_config["dep_id"] = {id: name}
    dump(anvil_config, ANVIL_CONFIG_FILE.open("w"), Dumper=Dumper)
    repo = Repository(".")
    _commit_all(repo, f"Set {name} as a dependency")