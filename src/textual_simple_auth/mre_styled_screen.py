import mre_styled_screen_newscreen
from textual.app import App, ComposeResult
from textual.widgets import Label


class AppWithScreen(App[None]):
    CSS = """
        Screen {
            align: center middle;
            background: black;
        }

        Label {
            border: hkey $secondary;
            background: $panel;
        }
    """

    def compose(self) -> ComposeResult:
        yield Label("I'm stylish")

    def on_mount(self) -> None:
        self.push_screen(mre_styled_screen_newscreen.NewScreen())


AppWithScreen().run()
