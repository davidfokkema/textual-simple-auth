import click


@click.group()
def auth():
    """Manage user authentication."""


@auth.command()
@click.option("-N", "--number", default=3)
def list(number):
    """List users."""
    for idx in range(1, number + 1):
        print(f"{idx}. Running my custom thingy.")


@auth.command()
def add():
    """Add user or update password."""
    ...


@auth.command()
def remove():
    """Remove user."""
    ...
