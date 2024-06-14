from rich import print
from textual.app import App, ComposeResult, on
from textual.containers import Grid
from textual.widgets import Button, Input, Label

from textual_simple_auth import auth


class LoginApp(App[bool]):

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

    @on(Button.Pressed)
    def login(self, event: Button.Pressed) -> None:
        print(f"{event.button.id=}")
        if event.button.id == "login":
            username = self.query_one("#name").value
            password = self.query_one("#password").value

            result = auth.verify_password(
                username, password, self.app_name, self.app_author
            )

        else:
            result = False
        self.exit(result=result)
