from rich import print
from textual.app import App, ComposeResult, on
from textual.containers import Grid
from textual.widgets import Button, Input, Label


class LoginApp(App[bool]):

    CSS_PATH = "auth.tcss"

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


def auth(cls):
    run = cls.run

    def new_run(self) -> None:
        login_app = LoginApp()
        success = login_app.run()
        if success is True:
            run(self)
        else:
            print(
                "[red]Authentication failed. You need to log in to access this app.[/]"
            )

    cls.run = new_run
    return cls


@auth
class A:
    def run(self) -> None:
        print("Running my app!")


if __name__ == "__main__":
    A().run()
