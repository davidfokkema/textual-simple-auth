import time

from textual.app import App, ComposeResult, on
from textual.screen import Screen
from textual.widgets import Button, Label


class Login(App):
    auth_successful = False

    def compose(self) -> ComposeResult:
        yield Button("Login", id="login")
        yield Button("Cancel", id="cancel")

    @on(Button.Pressed)
    def login(self, event: Button.Pressed) -> None:
        if event.button.id == "login":
            self.auth_successful = True
        self.exit()


class SimpleAuthDemo(App):
    CSS_PATH = "demo.tcss"

    def compose(self) -> ComposeResult:
        yield Label("This should only be accessible after login.")

    def run(self) -> None:
        login_app = Login()
        login_app.run()
        if login_app.auth_successful is True:
            super().run()


if __name__ == "__main__":
    SimpleAuthDemo().run()
