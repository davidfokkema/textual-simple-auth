from textual.app import App, ComposeResult
from textual.widgets import Label


class SimpleAuthDemo(App):
    CSS_PATH = "demo.tcss"

    def compose(self) -> ComposeResult:
        yield Label("This should only be accessible after login.")


if __name__ == "__main__":
    SimpleAuthDemo().run()
