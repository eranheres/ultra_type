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
        self.plain_text = self.paginate_text(text)
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
        word, word_count = ctrl.get_current_word()
        stats = self.query_one("#stats")
        stats.pos = self.controller.current_pos
        stats.word = word
        stats.word_count = word_count
        if ctrl.practice_time:
            stats.wpm = int((ctrl.current_pos-ctrl.start_pos) / 5 / (ctrl.practice_time / 60))
        stats.accuracy = (100 - int(ctrl.error_count / (ctrl.current_pos + 1) * 100))
        stats.errors = ctrl.error_count
        stats.progress = int(ctrl.current_pos / len(self.plain_text) * 100)
        stats.current_key = ctrl.get_current_key()

    def update_label(self):
        if not self.plain_text:
            return
        current_pos = self.controller.current_pos
        line_start_pos, line_end_pos = self._get_line_coordinations(current_pos)
        rich_text = Text(self.plain_text)
        color = "blue"
        if self.controller.model.language.is_ltr():
            rich_text.stylize(color, 0, current_pos)
            rich_text.stylize("underline ", current_pos , current_pos + 1)
        else:
            rich_text.stylize(color, 0, line_start_pos)
            curser_pos = line_start_pos + (line_end_pos - current_pos)
            rich_text.stylize(color, curser_pos, line_end_pos)
            rich_text.stylize("underline ", curser_pos - 1, line_end_pos - current_pos)
        l = self.query_one("#text")
        # label.text_style.stylize("red", 0, pos)
        l.update(rich_text)
        self.render()

    def on_key(self, event: events.Key) -> None:
        if self.plain_text is None:
            return
        if event.key in self.controls:
            return

        self.controller.on_key(event.character)
        self.update_label()
        self.update_statss()

    def _get_line_coordinations(self, pos: int) -> (int, int):
        s = self.plain_text
        bindex = s[:pos + 1].rfind("\n")
        if bindex == -1:
            bindex = 0
        eindex = s[pos:].find("\n")
        if eindex == -1:
            eindex = len(s)
        else:
            eindex += pos
        return bindex, eindex

    def paginate_text(self, text) -> str:
        if self.controller.model.language.is_ltr():
            return text
        label = self.query_one("#text")
        width = label.container_size.width - 2
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 > width:
                current_line += " "
                lines.append(current_line[::-1])
                current_line = word
            else:
                if current_line:  # Add a space if it's not the first word in the line
                    current_line += " "
                current_line += word

        # Add the last words and lines if not empty
        if current_line:
            lines.append(current_line[::-1])
        return "\n".join(lines)

