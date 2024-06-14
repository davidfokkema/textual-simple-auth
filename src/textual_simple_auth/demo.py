import time

import click
from textual import work
from textual.app import App, ComposeResult, on
from textual.events import Compose, Mount
from textual.screen import Screen
from textual.widgets import Button, Label

from textual_simple_auth.decorators import add_auth, login_required


class BlackScreen(Screen):
    CSS = """
        BlackScreen {
            background: black;
            hatch: " " black;
        }
    """


class LoginScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Button("Yes", id="yes")
        yield Button("No")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "yes":
            self.dismiss(True)
        self.dismiss(False)


# @login_required(app_name="textual_simple_auth")
class SimpleAuthDemo(App):
    CSS_PATH = "demo.tcss"

    MODES = {"login": LoginScreen}

    def compose(self) -> ComposeResult:
        yield Label("This should only be accessible after login.")

    def on_mount(self):
        self.push_screen(LoginScreen(), callback=self._handle_auth)

    def _handle_auth(self, is_authenticated):
        if not is_authenticated:
            self.push_screen(BlackScreen())
            self.exit()


@add_auth(app_name="textual_simple_auth")
@click.command()
def demo():
    """Run a simple app to demonstrate login."""
    SimpleAuthDemo().run()


if __name__ == "__main__":
    demo()
