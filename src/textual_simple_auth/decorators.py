import click
from rich import print

from textual_simple_auth.auth import auth
from textual_simple_auth.login import LoginApp


def login_required(app_name: str, app_author: str | None = None):
    def decorator(cls):
        run = cls.run

        def new_run(self) -> None:
            login_app = LoginApp(app_name, app_author)
            success = login_app.run()
            if success is True:
                run(self)
            else:
                print(
                    "[red]Authentication failed. You need to log in to access this app.[/]"
                )

        cls.run = new_run
        return cls

    return decorator


def add_auth(app_name: str, app_author: str | None = None, command: str = "auth"):
    def decorator(app: click.Group | click.Command):
        context = {"obj": {"app_name": app_name, "app_author": app_author}}
        auth.context_settings |= context
        if isinstance(app, click.Group):
            app.add_command(auth, name=command)
        else:

            @click.group(invoke_without_command=True)
            @click.pass_context
            def new_group(ctx):
                if ctx.invoked_subcommand is None:
                    app()

            new_group.add_command(auth, name=command)
            return new_group

        return app

    return decorator
