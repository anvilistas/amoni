import typer
from cookiecutter.main import cookiecutter
from python_on_whales import docker

amoni = typer.Typer()


@amoni.callback()
def main():
    pass


@amoni.command()
def init(
    project: str = typer.Option("", help="Project Name", prompt=True),
    app_folder_name: str = typer.Option(
        "hello_world", help="App Folder Name", prompt=True
    ),
):
    """Initialise an amoni project"""
    cookiecutter(
        "https://github.com/anvilistas/amoni-cookiecutter.git",
        no_input=True,
        extra_context={"project_name": project, "app_folder_name": app_folder_name},
    )
    typer.echo(f"amoni project created in {project} directory")


@amoni.command()
def start():
    """Start the anvil app and db servers"""
    typer.echo("Starting anvil app and database servers...")
    docker.compose.up(["app"], detach=True)
    typer.echo("Your app is available at http://localhost:3030")


@amoni.command()
def stop():
    """Stop the anvil app and db servers"""
    typer.echo("Stopping the anvil app and database servers...")
    docker.compose.down()
    typer.echo("Done")


@amoni.command()
def test():
    """Run the test suite"""
    typer.echo("amoni test called")


@amoni.command()
def app(url: str):
    """Fetch the main app from anvil or some other git server"""
    typer.echo(f"amoni app called with url {url}")


@amoni.command()
def dependency(url: str):
    """Fetch a dependency from anvil or some other git server"""
    typer.echo(f"amoni dependency called with url {url}")
