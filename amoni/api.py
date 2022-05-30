# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni
from cookiecutter.main import cookiecutter
from python_on_whales import docker

__version__ = "0.0.3"

COOKIECUTTER_URL = "https://github.com/anvilistas/amoni-cookiecutter.git"


def init(project: str, app_folder_name: str) -> None:
    """Initialise an amoni project

    Parameters
    ----------
    project
        The name of the amoni project folder to create
    app_folder_name
        The name of folder within the 'app' folder which contains the app to be run
    """
    cookiecutter(
        COOKIECUTTER_URL,
        no_input=True,
        extra_context={"project_name": project, "app_folder_name": app_folder_name},
    )


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
