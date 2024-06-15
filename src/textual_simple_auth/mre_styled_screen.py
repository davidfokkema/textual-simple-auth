from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Label


class NewScreen(Screen):
    CSS = """
        Screen {
            background: red;
        }
    """

    def compose(self) -> ComposeResult:
        yield Label("Hi there!")
        yield Button("Close")

    def on_mount(self) -> None:
        self.reset_styles()

    def on_button_pressed(self) -> None:
        self.dismiss()


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
        self.push_screen(NewScreen())


AppWithScreen().run()
