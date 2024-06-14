from rich import print
from textual.app import App, ComposeResult, on
from textual.containers import Grid
from textual.widgets import Button, Input, Label


class LoginApp(App[bool]):

    CSS_PATH = "login.tcss"

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
            self.exit(result=True)
        else:
            self.exit(result=False)
