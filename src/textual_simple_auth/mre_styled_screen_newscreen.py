import textual.widgets
from textual.app import App, ComposeResult
from textual.screen import Screen


class MyLabel(textual.widgets.Label, inherit_css=False):
    DEFAULT_CSS = """
        MyLabel {
            width: auto;
            height: auto;
            min-height: 1;
        }
    """


class MyButton(textual.widgets.Button): ...


class NewScreen(Screen, inherit_css=False):

    def compose(self) -> ComposeResult:
        yield MyLabel("Hi there!")
        yield MyButton("Close")

    def on_button_pressed(self) -> None:
        self.dismiss()
