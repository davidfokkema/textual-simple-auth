import click
from textual.app import App, ComposeResult
from textual.widgets import Label

from textual_simple_auth.decorators import add_auth, login_required


@login_required(app_name="textual_simple_auth")
class SimpleAuthDemo(App):
    CSS_PATH = "demo.tcss"

    def compose(self) -> ComposeResult:
        yield Label("This should only be accessible after login.", id="msg")

    def on_mount(self) -> None:
        self.query_one("#msg").styles.text_style = "bold"


@add_auth(app_name="textual_simple_auth")
@click.command()
def demo():
    """Run a simple app to demonstrate login."""
    SimpleAuthDemo().run()


if __name__ == "__main__":
    demo()
