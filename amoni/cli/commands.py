import typer

amoni = typer.Typer()


@amoni.callback()
def main():
    pass


@amoni.command()
def init():
    """Initialise an amoni project"""
    typer.echo("amoni init called")


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
