import click
from textual.app import App, ComposeResult
from textual.widgets import Label

from textual_simple_auth.decorators import add_auth, auth


@auth
class SimpleAuthDemo(App):
    CSS_PATH = "demo.tcss"

    def compose(self) -> ComposeResult:
        yield Label("This should only be accessible after login.")


@add_auth()
@click.command()
def demo():
    """Run a simple app to demonstrate login."""
    SimpleAuthDemo().run()


if __name__ == "__main__":
    demo()
