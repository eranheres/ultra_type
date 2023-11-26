import curses

class View:
    def __init__(self):
        self.stdscr = curses.initscr()
    def get_user_input(self):
        return self.stdscr.getstr().decode('utf-8')

    def get_language_choice(self):
        self.stdscr.addstr("Choose a language: English or Hebrew")
        self.stdscr.refresh()
        return self.stdscr.getstr().decode('utf-8')

    def display_word(self, word: str):
        self.stdscr.clear()
        self.stdscr.addstr(word)
        self.stdscr.refresh()

    def display_stats(self, stats: dict):
        self.stdscr.clear()
        self.stdscr.addstr(str(stats))
        self.stdscr.refresh()
# No lines to replace
