from textual.app import App, ComposeResult
from textual.widgets import DataTable
from textual.screen import Screen
from textual.binding import Binding
from textual.widgets import Footer, Header
from textual.widgets import OptionList
from textual.containers import Horizontal
from textual import on, events

from ultra_type.model import Model


class StatsScreen(Screen):
    CSS_PATH = "view_stats.tcss"

    BINDINGS = [Binding("escape", "pop_screen()", "Back")]

    def __init__(self, model: Model):
        super().__init__()
        self.model = model

    def compose(self) -> ComposeResult:
        yield Header()
        yield Horizontal(
            OptionList(
                "Practice statistics",
                "Letters statistics",
                "Words statistics",
                "Daily practice time",
                id="stats_list"),
            DataTable(id="data_table")
        )
        yield Footer()

    @on(OptionList.OptionHighlighted, "#stats_list")
    def on_stats_list(self, message: OptionList.OptionHighlighted) -> None:
        header, data = self.model.statistics.word_data()
        if message.option.prompt == "Practice statistics":
            header, data = self.model.statistics.practices_data()
        elif message.option.prompt == "Letters statistics":
            header, data = self.model.statistics.letters_data()
        elif message.option.prompt == "Words statistics":
            header, data = self.model.statistics.word_data()
        elif message.option.prompt == "Daily practice time":
            header, data = self.model.statistics.daily_data()
        rows = list([header])
        rows.extend(data)
        self.query_one(DataTable).clear(columns=True)
        self.query_one(DataTable).add_columns(*rows[0])
        self.query_one(DataTable).add_rows(rows[1:])


class TableApp(App):
    BINDINGS = [Binding("o", "table", "Push screen")]

    def __init__(self, model: Model):
        super().__init__()
        self.model = model

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def action_table(self) -> None:
        self.push_screen(StatsScreen(self.model))


if __name__ == "__main__":
    m = Model()
    app = TableApp(m)
    app.run()
