import click
from rich import print

from textual_simple_auth.login import LoginApp


def login_required(cls):
    run = cls.run

    def new_run(self) -> None:
        login_app = LoginApp()
        success = login_app.run()
        if success is True:
            run(self)
        else:
            print(
                "[red]Authentication failed. You need to log in to access this app.[/]"
            )

    cls.run = new_run
    return cls


def add_auth(command: str = "auth"):
    def decorator(app: click.Group | click.Command):
        @click.command()
        @click.option("-N", "--number", default=3)
        def wrapped_tui(number):
            """Manage user authentication."""
            for idx in range(1, number + 1):
                print(f"{idx}. Running my custom thingy.")

        if isinstance(app, click.Group):
            app.add_command(wrapped_tui, name=command)
        else:
            new_group = click.Group()
            new_group.add_command(app)
            new_group.add_command(wrapped_tui, name=command)
            return new_group

        return app

    return decorator
