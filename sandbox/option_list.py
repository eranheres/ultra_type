from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Select


LANGS = ["English", "Hebrew", "Spanish"]
PRACTICES = ["Reading", "Writing", "Listening", "Speaking"]

class SelectApp(App):
    CSS_PATH = "select.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Select.from_values(LANGS)
        yield Select.from_values(PRACTICES)

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        self.title = str(event.value)


if __name__ == "__main__":
    app = SelectApp()
    app.run()

