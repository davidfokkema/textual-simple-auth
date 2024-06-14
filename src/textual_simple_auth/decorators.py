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


def add_auth(command: str = "auth", help: str = "Manage user authentication."):
    def decorator(app: click.Group | click.Command):
        def wrapped_tui():
            print("Running my custom thingy.")

        if isinstance(app, click.Group):
            app.command(name=command, help=help)(wrapped_tui)
        else:
            new_group = click.Group()
            new_group.add_command(app)
            new_group.command(name=command, help=help)(wrapped_tui)
            return new_group

        return app

    return decorator
