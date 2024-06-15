from textual.app import ComposeResult, on
from textual.containers import Grid
from textual.screen import Screen
from textual.widgets import Button, Input, Label

from textual_simple_auth import auth


class BlackScreen(Screen, inherit_css=False):
    CSS = """
        BlackScreen {
            background: black;
        }
    """


class LoginScreen(Screen, inherit_css=False):

    CSS_PATH = "login.tcss"

    def __init__(self, app_name: str, app_author: str | None = None) -> None:
        super().__init__()
        self.app_name = app_name
        self.app_author = app_author

    def compose(self) -> ComposeResult:
        with (grid := Grid()):
            grid.border_title = "Login required"
            yield Label("Name:")
            yield Input(id="name")
            yield Label("Password:")
            yield Input(password=True, id="password")
            yield Button("Login", id="login", variant="primary")
            yield Button("Cancel", id="cancel", variant="error")

    @on(Button.Pressed, "#cancel")
    def cancel(self) -> None:
        self.dismiss(False)

    @on(Input.Submitted, "#password")
    @on(Button.Pressed, "#login")
    def verify_and_exit(self) -> None:
        username = self.query_one("#name").value
        password = self.query_one("#password").value

        self.dismiss(
            auth.verify_password(username, password, self.app_name, self.app_author)
        )
