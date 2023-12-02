import curses
import pandas as pd
from ultra_type.curses_mock import CursesMock

class View:
    def __init__(self):
        self.stdscr = curses.initscr()
        self.screen_height, self.screen_width = self.stdscr.getmaxyx()

        curses.noecho()
        curses.cbreak()

    def __del__(self):
        curses.endwin()

    def _display_menu(self, options: []):
        self.stdscr.clear()
        for i, option in enumerate(options):
            self.stdscr.addstr(f"{i+1}. {option}\n")
        self.stdscr.addstr(f"{len(options)+1}. Exit\n")
        self.stdscr.refresh()
        while (True):
            try:
                key = self.get_user_key()
                if key == '\x1b' or key == chr(27):
                    return len(options) + 1
                if int(key) <= len(options) + 1:
                    return key
                # check if key is escape
                self.display_str_at(7,0,f"Invalid choice, please try again.{int(key)}")
            except ValueError:
                pass

    def get_main_menu_selection(self):
        return self._display_menu([
            "Practice",
            "Show Stats",
            "Change Language",
            "Change practice",
            "Save settings"])

    def show_language_menu(self):
        return self._display_menu([
            "English",
            "Hebrew"])

    def show_stats_menu(self):
        return self._display_menu([
            "Practice statistics",
            "Letters speed statistics",
            "Words statistics"])

    def show_stats_from_structure(self, stats: []):
        trimed_stats = stats[0:10]
        df = pd.DataFrame(trimed_stats)
        tbl = df.to_string(index=False)
        self.display_text(tbl)
        self.get_user_key()

    def get_user_key(self):
        # start a timer
        return chr(self.stdscr.getch())

    def display_str_at(self, y: int, x: int, text: str):
        self.stdscr.move(y, x)
        self.stdscr.addstr(text)
        self.stdscr.refresh()

    def get_user_text(self):
        # use curses to get user input character by character
        self.stdscr.keypad(True)
        user_input = ''
        while True:
            c = chr(self.stdscr.getch())
            if c == '\n':
                break
            # echo the character back to the screen
            self.stdscr.addstr(str(c))
            user_input += c

        return user_input

    def display_text(self, word: str):
        self.stdscr.clear()
        self.stdscr.addstr(word)
        self.stdscr.refresh()

    def show_letters_stats(self, char_times: {}):
        str = "Average Time per Character:\n"
        for char, info in char_times.items():
            average = info['total'] / info['count']
            str += f"Character '{char}': {average} sec\n"
        self.display_text(str)
        self.get_user_key()

    def get_practice_selection(self, practices: []):
        return self._display_menu([practice.description for practice in practices])

# run if main
if __name__ == '__main__':
    view = View()
    word = view.get_user_input()
    view.display_word('got: ' + word)