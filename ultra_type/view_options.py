from textual import on, work
from textual.app import App, ComposeResult
from textual.widgets import Select, Label, Button, Pretty, Switch
from textual.containers import Vertical, Horizontal
from textual.screen import ModalScreen
from textual.message import Message

from ultra_type.controller import Controller
from ultra_type.model import Model

LANGS = ["English", "Hebrew"]
PRACTICES = ["Reading", "Writing", "Listening", "Speaking"]


class ViewOptions(ModalScreen[dict]):
    CSS_PATH = "view_options.tcss"
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def __init__(self, ctrlr: Controller):
        super().__init__()
        self.controller = ctrlr

    def compose(self) -> ComposeResult:
        practices = self._practice_options()
        languages = self._language_options()
        lang_index = self.controller.language_idx()
        practice_index = self.controller.practice_idx()
        sound_on = self.controller.model.click_sound_enabled
        lang_select: Select[int] = Select(options=languages, prompt="Language", value=lang_index, id="language_select")
        prac_select: Select[int] = Select(options=practices, prompt="Practice", value=practice_index, id="practice_select")
        yield Vertical(
            Horizontal(Label("Language"), lang_select),
            Horizontal(Label("Practice"), prac_select),
            Horizontal( Label("Sound"), Switch(value=sound_on),
            ),
            Horizontal(Button("OK", id="button_ok"), Button("Cancel", id="button_cancel")),
            id="options"
        )

    def _language_options(self) -> list:
        languages = self.controller.model.languages
        return [(languages[i].name, i) for i in range(len(languages))]

    def _practice_options(self) -> list:
        practices = self.controller.practices
        return [(practices[i].description, i) for i in range(len(practices))]


    @on(Select.Changed, "#language_select")
    def select_changed(self, event: Select.Changed) -> None:
        selected = event.value
        self.controller.model.language = self.controller.languages[selected]
        selections = self.query_one("#practice_select")
        selections.set_options(self._practice_options())
        selections.value = 0
        self.controller.model.practice = self.controller.practices[0]

    @on(Select.Changed, "#practice_select")
    def select_practice(self, event: Select.Changed) -> None:
        selected = event.value
        self.controller.model.practice = self.controller.practices[selected]

    class Settings(Message):
        def __init__(self, settings: dict) -> None:
            self.settings = settings
            super().__init__()

    @on(Button.Pressed, "#button_ok")
    def on_button_ok(self, event: Button.Pressed) -> None:
        options = {
            "language": self.controller.model.language.name,
            "practice": self.controller.model.practice.description,
            "sound_on": self.query_one(Switch).value
        }
        self.post_message(ViewOptions.Settings(options))

    @on(Button.Pressed, "#button_cancel")
    def on_button_cancel(self, event: Button.Pressed) -> None:
        self.post_message(ViewOptions.Settings({}))


class MyApp(App):
    SCREENS = {"options": ViewOptions}
    BINDINGS = [("o", "options", "Options")]

    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller

    def label_text(self):
        return f"""
        Welcome to UltraType! Press 'o' to open options
        Practice:{self.controller.model.practice.description}
        Language:{self.controller.model.language.name}
        """

    def action_options(self):
        self.push_screen(ViewOptions(self.controller))

    def compose(self):
        yield Label(self.label_text(), id="desc")
        yield Pretty({})

    def on_view_options_settings(self, message: ViewOptions.Settings) -> None:
        self.pop_screen()
        lang_index = self.controller.language_idx(message.settings["language"])
        prac_index = self.controller.practice_idx(message.settings["practice"])
        self.controller.model.language = self.controller.languages[lang_index]
        self.controller.model.practice = self.controller.practices[prac_index]
        self.query_one(Label).update(self.label_text())
        self.query_one(Pretty).update(message.settings)

if __name__ == "__main__":
    ctrl = Controller(model=Model())
    app = MyApp(ctrl)
    app.run()

