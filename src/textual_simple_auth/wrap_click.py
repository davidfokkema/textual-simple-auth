import click


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


@add_auth()
@click.command()
def thingy():
    """Does the thingy."""
    print("This is main!")


if __name__ == "__main__":
    thingy()
