import curses
import pandas as pd
from tabulate import tabulate


class View:
    def __init__(self):
        self.stdscr = curses.initscr()
        self.screen_height, self.screen_width = self.stdscr.getmaxyx()

        curses.noecho()
        curses.cbreak()

    def __del__(self):
        curses.endwin()

    def _display_menu(self, header: str, options: []):
        self.stdscr.clear()
        self.stdscr.addstr(header+"\n")
        self.stdscr.addstr("-" * (len(header) + 1) + "\n")
        for i, option in enumerate(options):
            self.stdscr.addstr(f"{i+1}. {option}\n")
        self.stdscr.addstr(f"{len(options)+1}. Exit\n")
        self.stdscr.refresh()
        while (True):
            try:
                key = self.get_user_key()
                if key in ["\x1b"]:
                    return len(options) + 1
                if int(key) <= len(options) + 1:
                    return key
                # check if key is escape
                self.display_str_at(7, 0, f"Invalid choice, please try again.{int(key)}")
            except ValueError:
                pass

    def get_main_menu_selection(self, language: str, practice: str):
        header = f"Main Menu     (Language:{language}, Practice:{practice})"
        return self._display_menu(header=header, options=[
            "Practice",
            "Show Stats",
            "Change Language",
            "Change practice",
            "Save settings"])

    def show_language_menu(self):
        return self._display_menu(header="Choose language:", options=[
            "English",
            "Hebrew"])

    def show_stats_menu(self):
        return self._display_menu(header="Choose statistics type:", options=[
            "Practice statistics",
            "Letters speed statistics",
            "Words statistics"])

    def show_stats_from_structure(self, stats: []):
        df = pd.DataFrame(stats)
        txt = str(tabulate(df, headers=df.columns, tablefmt='github'))
        self.display_full_screen_text(txt)

    def get_user_key(self) -> str:
        # start a timer
        return self.stdscr.getkey()

    def display_str_at(self, y: int, x: int, text: str):
        self.stdscr.move(y, x)
        self.stdscr.addstr(text)
        self.stdscr.refresh()

    def display_full_screen_text(self, text: str):
        lines = text.split('\n')
        # segment lines to pages of max_height size
        lines = [line.ljust(self.screen_width-1) for line in lines]
        pages = ["\n".join(lines[i:i + self.screen_height-1]) for i in range(0, len(lines), self.screen_height-1)]

        page_num = 0
        while True:
            self.stdscr.clear()
            self.stdscr.addstr(pages[page_num])
            self.stdscr.refresh()
            key = self.get_user_key()
            if key in ["\x1b", curses.KEY_ENTER]:
                break
            if (key in [curses.KEY_UP, 'k']) and page_num > 0:
                page_num -= 1
            if (key in [curses.KEY_DOWN, 'j']) and page_num < len(pages) - 1:
                page_num += 1

    def show_letters_stats(self, char_times: {}):
        str = "Average Time per Character:\n"
        for char, info in char_times.items():
            average = info['total'] / info['count']
            str += f"Character '{char}': {average} sec\n"
        self.display_full_screen_text(str)

    def get_practice_selection(self, practices: []):
        return self._display_menu(
            header="Choose practice:",
            options=[practice.description for practice in practices])
