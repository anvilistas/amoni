import typer
from cookiecutter.main import cookiecutter

amoni = typer.Typer()


@amoni.callback()
def main():
    pass


@amoni.command()
def init(project: str = typer.Option(..., help="Project Name", prompt=True)):
    """Initialise an amoni project"""
    cookiecutter(
        "https://github.com/anvilistas/amoni-cookiecutter.git",
        no_input=True,
        extra_context={"project_name": project},
    )
    typer.echo(f"amoni project created in {project} directory")


@amoni.command()
def start():
    """Start the anvil app and db servers"""
    typer.echo("amoni start called")


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
