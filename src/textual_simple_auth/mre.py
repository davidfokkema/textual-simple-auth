from textual.app import App, ComposeResult
from textual.widgets import Button, Label


class LoginApp(App):
    def compose(self) -> ComposeResult:
        yield Button("Press to log in")

    def on_button_pressed(self):
        self.exit()


class SimpleAuthDemo(App):

    def compose(self) -> ComposeResult:
        yield Label("This should only be accessible after login.")

    def run(self):
        LoginApp().run()
        super().run()


SimpleAuthDemo().run()
