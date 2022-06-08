# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni
import os
from pathlib import Path

from cookiecutter.main import cookiecutter
from pygit2 import init_repository
from python_on_whales import docker

__version__ = "0.0.4"

COOKIECUTTER_URL = "https://github.com/anvilistas/amoni-cookiecutter.git"


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
    os.chdir(directory)
    repo.index.add_all()
    repo.index.write()
    commit_args = {
        "ref": "HEAD",
        "author": repo.default_signature,
        "committer": repo.default_signature,
        "message": "Initial commit",
        "tree": repo.index.write_tree(),
        "parents": [],
    }
    repo.create_commit(*commit_args.values())


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
