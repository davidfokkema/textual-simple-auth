import time

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Label


class LoginScreen(Screen):

    CSS = """
        LoginScreen {
            background: black;
        }
    """

    def compose(self) -> ComposeResult:
        time.sleep(1)
        yield Button("Press to log in")

    def on_button_pressed(self):
        self.dismiss()


class SimpleAuthDemo(App):

    CSS = """
        Screen {
            background: red;
        }
    """

    def compose(self) -> ComposeResult:
        for _ in range(100):
            yield Label("This should only be accessible after login.")

    def on_mount(self) -> None:
        self.push_screen(LoginScreen())


SimpleAuthDemo().run()
