from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Label
from textual.containers import Grid
from textual.widgets import Header, Footer, Static
from rich.text import Text
from textual import events
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual import work

from ultra_type.view_options import ViewOptions
from ultra_type.view_stats import StatsScreen
from ultra_type.controller import Controller

class Stats(Static):
    pos = reactive(0)
    word = reactive("")
    word_count = reactive(0)

    wpm = reactive(0)
    accuracy = reactive(0)
    errors = reactive(0)
    progress = reactive(0)
    current_key = reactive("")
    line = reactive(0)
    line_start_pos = reactive(0)
    line_end_pos = reactive(0)
    cursor_pos = reactive(0)

    def compose(self) -> ComposeResult:
        yield Label(id="stats_label")

    def render(self) -> str:
        str = ""
        str += f"Pos : {self.pos}\n"
        #str += f"Word: {self.word}\n"
        str += f"Word: {self.word_count}\n"
        str += f"WPM : {self.wpm}\n"
        str += f"Accu: {self.accuracy}%\n"
        str += f"Err : {self.errors}\n"
        str += f"Prog: {self.progress}%\n"
        str += f"Key : {self.current_key}\n"
        str += f"Line: {self.line}\n"
        str += f"LnSt: {self.line_start_pos}\n"
        str += f"LnEn: {self.line_end_pos}\n"
        str += f"CPos: {self.cursor_pos}\n"
        return str

class PauseScreen(ModalScreen):
    def compose(self):
        yield Label("Paused !!!\nPress any key to resume...", id="paused")

    def on_key(self, event: events.Key) -> None:
        event.stop()
        self.dismiss()

class ViewMain(App):
    CSS_PATH = "view_main.tcss"
    BINDINGS = [Binding("ctrl+q", "quit", "Quit"),
                Binding("ctrl+o", "options", "Options"),
                Binding("ctrl+r", "restart", "Restart"),
                Binding("ctrl+s", "save", "Save"),
                Binding("ctrl+t", "stats", "Stats"),
                Binding("escape", "pause", "Pause")]

    SCREENS = {"options": ViewOptions}
    controls = ["ctrl+q", "ctrl+o", "ctrl+r", "ctrl+s", "escape", "ctrl+t", "up", "down", "left", "right", "enter", "tab"]

    def __init__(self, controller: Controller):
        super().__init__()
        self.practice_text = None
        self.controller = controller

    async def on_mount(self):
        self.set_timer(1, self.load_practice)

    def action_restart(self):
        self.controller.reset()
        self.action_new()

    def action_save(self):
        self.controller.model.save_setting()
        self.controller.model.save_stats()

    @work
    async def action_pause(self):
        self.controller.pause()
        await self.push_screen_wait(PauseScreen())
        self.pop_screen()

    @work
    async def action_stats(self):
        self.controller.pause()
        await self.push_screen_wait(StatsScreen(self.controller.model))
        self.pop_screen()


    def load_practice(self):
        text, pos = self.controller.model.practice.generate_practice(self.controller.model)
        self._viewed_plain_text = self._viewed_text(text)
        self.controller.reset_practice(text, pos)
        self.action_new()

    def action_new(self):
        if self.controller.model.language.is_ltr():
            self.text_widget.styles.text_align = "left"
        else:
            self.text_widget.styles.text_align = "right"
        self.update_label()

    def action_options(self):
        self.push_screen(ViewOptions(self.controller))

    def on_view_options_settings(self, message: ViewOptions.Settings) -> None:
        self.pop_screen()
        lang_index = self.controller.language_idx(message.settings["language"])
        prac_index = self.controller.practice_idx(message.settings["practice"])
        self.controller.model.language = self.controller.languages[lang_index]
        self.controller.model.practice = self.controller.practices[prac_index]
        self.controller.model.click_sound_enabled = message.settings["sound_on"]
        self.controller.sound_enabled(message.settings["sound_on"])
        self.load_practice()

    def compose(self):
        self.text_widget = Label("", id="text")
        yield Header()
        # yield Stats(TEXT, id="stats")
        yield Grid(
            Stats(id="stats"),
            self.text_widget,
        )
        yield Footer()

    def action_exit(self):
        self.exit()

    def watch_text(self):
        self.bell()
        label = self.query_one("text")
        if label:
            label.text = "aaa"
            self.render()

    def update_statss(self):
        ctrl = self.controller
        line_start_pos, line_end_pos, line_number = self._get_line_coordinations(ctrl.current_pos)
        word, word_count = ctrl.get_current_word()
        stats = self.query_one("#stats")
        stats.pos = ctrl.current_pos
        stats.word = word
        stats.word_count = word_count
        if ctrl.practice_time:
            stats.wpm = int((ctrl.current_pos-ctrl.start_pos) / 5 / (ctrl.practice_time / 60))
        stats.accuracy = (100 - int(ctrl.error_count / (ctrl.current_pos + 1) * 100))
        stats.errors = ctrl.error_count
        stats.progress = int(ctrl.current_pos / len(ctrl.text) * 100)
        stats.current_key = ctrl.get_current_key()
        stats.line = line_number
        stats.line_start_pos = line_start_pos
        stats.line_end_pos = line_end_pos
        stats.cursor_pos = line_start_pos + (line_end_pos - ctrl.current_pos)

    def update_label(self):
        if not self._viewed_plain_text:
            return
        current_pos = self.controller.current_pos
        rich_text = Text(self._viewed_plain_text)
        color = "blue"
        if self.controller.model.language.is_ltr():
            rich_text.stylize(color, 0, current_pos)
            rich_text.stylize("underline ", current_pos , current_pos + 1)
        else:
            line_start_pos, line_end_pos, line_number = self._get_line_coordinations(current_pos)
            rich_text.stylize(color, 0, line_start_pos + line_number)
            curser_pos = line_start_pos + (line_end_pos - current_pos) + line_number
            rich_text.stylize(color, curser_pos, line_end_pos + line_number)
            rich_text.stylize("underline ", curser_pos - 1, curser_pos)
        l = self.query_one("#text")
        # label.text_style.stylize("red", 0, pos)
        l.update(rich_text)
        self.render()

    def on_key(self, event: events.Key) -> None:
        if self._viewed_plain_text is None:
            return
        if event.key in self.controls:
            return

        self.controller.on_key(event.character)
        self.update_label()
        self.update_statss()

    def _get_line_coordinations(self, pos: int) -> (int, int, int):
        lines = self._viewed_plain_text.split("\n")
        line_start_pos = 0
        line_end_pos = 0
        line_number = 0
        for line in lines:
            line_end_pos += len(line)
            if line_end_pos > pos:
                break
            line_start_pos = line_end_pos
            line_number += 1
        return line_start_pos, line_end_pos, line_number

    def _viewed_text(self, text) -> str:
        if self.controller.model.language.is_ltr():
            return text
        label = self.query_one("#text")
        width = label.container_size.width
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            # if the word is too long to fit in the line
            if len(current_line) + len(word) + 1 > width:
                lines.append(current_line[::-1])
                current_line = ""
            current_line += word + " "

        current_line = current_line[:-1]  # remove the last space
        lines.append(current_line[::-1])
        return "\n".join(lines)

