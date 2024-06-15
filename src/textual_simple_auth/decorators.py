import click
from rich import print

from textual_simple_auth.auth import auth
from textual_simple_auth.login import BlackScreen, LoginScreen


def login_required(app_name: str, app_author: str | None = None):
    def decorator(cls):
        run = cls.run
        try:
            _on_mount = cls._on_mount
        except AttributeError:
            _on_mount = None

        def new_run(self, *args, **kwargs) -> None:
            run(self, *args, **kwargs)
            if not self._is_authenticated:
                print(
                    "[red]Authentication failed. You need to log in to access this app.[/]"
                )

        def new_on_mount(self):
            self.push_screen(
                LoginScreen("textual_simple_auth"),
                callback=lambda value: _handle_auth(self, value),
            )

        def _handle_auth(self, is_authenticated):
            self._is_authenticated = is_authenticated
            if not is_authenticated:
                self.push_screen(BlackScreen())
                self.exit()
            else:
                if _on_mount is not None:
                    _on_mount(self)
                else:
                    # If there is no _on_mount method, there may be an on_mount
                    # method. Run that, instead.
                    try:
                        self.on_mount()
                    except AttributeError:
                        pass

        cls.run = new_run
        cls._on_mount = new_on_mount
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
