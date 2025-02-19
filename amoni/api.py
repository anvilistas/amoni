# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

import keyring
import pygit2
from cookiecutter.main import cookiecutter
from dotenv import load_dotenv
from yaml import dump, load

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader

__version__ = "0.0.13"

COOKIECUTTER_URL = os.environ.get(
    "AMONI_COOKIECUTTER_PATH", "https://github.com/anvilistas/amoni-cookiecutter.git"
)
ANVIL_CONFIG_FILE = Path("app", "config.yaml")
TABLE_STUB_FILE = Path("anvil-stubs", "tables", "app_tables.pyi")


def get_ports() -> Tuple[str, str, str, bool]:
    """Get the configured ports and origin URL for app and database servers.
    If no .env file is found, falls back to default values:
    - app_port=3030
    - db_port=5432
    - origin_url=http://localhost:3030

    Returns
    -------
    Tuple[str, str, str, bool]
        A tuple containing (app_port, db_port, origin_url, env_file_found)
        where env_file_found indicates if the .env file was loaded successfully
    """
    env_file_found = load_dotenv(dotenv_path=".env")

    app_port = os.environ.get("AMONI_APP_PORT", "3030")
    db_port = os.environ.get("AMONI_DB_PORT", "5432")
    origin_url = os.environ.get("ORIGIN_URL", f"http://localhost:{app_port}")

    return app_port, db_port, origin_url, env_file_found


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

    Raises
    ------
    RuntimeError
        If both docker compose and docker-compose commands fail
    """
    try:
        subprocess.run(["docker", "compose", "pull", name], check=True)
    except subprocess.CalledProcessError:
        try:
            subprocess.run(["docker-compose", "pull", name], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to pull image {name}: {e}")


def build_image(name: str) -> None:
    """Build a docker image

    Parameters
    ----------
    name
        The name of the image to build

    Raises
    ------
    RuntimeError
        If both docker compose and docker-compose commands fail
    """
    try:
        subprocess.run(["docker", "compose", "build", "--pull", name], check=True)
    except subprocess.CalledProcessError:
        try:
            subprocess.run(["docker-compose", "build", "--pull", name], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to build image {name}: {e}")


def start_service(name: str, detach: bool) -> None:
    """Start a given service

    Parameters
    ----------
    name
        The name of the service to start
    detach
        Whether to detach from the service console

    Raises
    ------
    RuntimeError
        If both docker compose and docker-compose commands fail
    """
    cmd = ["docker", "compose", "up"]
    if detach:
        cmd.append("-d")
    cmd.append(name)

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        cmd = ["docker-compose", "up"]
        if detach:
            cmd.append("-d")
        cmd.append(name)
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to start service {name}: {e}")


def stop_services() -> None:
    """Stop all amoni services

    Raises
    ------
    RuntimeError
        If both docker compose and docker-compose commands fail
    """
    try:
        subprocess.run(["docker", "compose", "down"], check=True)
    except subprocess.CalledProcessError:
        try:
            subprocess.run(["docker-compose", "down"], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to stop services: {e}")


def run_service(name: str, remove: bool = True) -> None:
    """Run a given service

    Parameters
    ----------
    name
        The name of the service to start
    remove
        Whether to remove the container after running

    Raises
    ------
    RuntimeError
        If both docker compose and docker-compose commands fail
    """
    cmd = ["docker", "compose", "run"]
    if remove:
        cmd.append("--rm")
    cmd.append(name)

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        cmd = ["docker-compose", "run"]
        if remove:
            cmd.append("--rm")
        cmd.append(name)
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to run service {name}: {e}")


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

    Raises
    ------
    RuntimeError
        If both docker compose and docker-compose commands fail
    """
    try:
        subprocess.run(
            ["docker", "compose", "run", "--rm", "theme_builder", app], check=True
        )
    except subprocess.CalledProcessError:
        try:
            subprocess.run(
                ["docker-compose", "run", "--rm", "theme_builder", app], check=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to build theme for {app}: {e}")


def add_table(
    app: str,
    name: str,
    client_permissions: str = "none",
    server_permissions: str = "full",
    columns: List = None,
):
    columns = [] if columns is None else columns
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


def checkout_version(app: str, version: str = None) -> None:
    """Checkout a specific version (tag or branch) of a submodule

    Parameters
    ----------
    app : str
        The name of the app (submodule)
    version : str, optional
        The version (tag or branch) to checkout. If not provided,
        stays on default branch.
    """
    if not version:
        return

    app_path = Path("app", app)

    try:
        subprocess.run(
            ["git", "fetch", "--tags"],
            cwd=app_path,
            check=True,
            capture_output=True,
            text=True,
        )

        subprocess.run(
            ["git", "checkout", version],
            cwd=app_path,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to checkout version '{version}' in {app}: {e.stderr}"
        )
