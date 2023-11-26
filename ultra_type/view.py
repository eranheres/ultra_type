class View:
    def get_user_input(self):
        return self.stdscr.getstr().decode('utf-8')

    def get_language_choice(self):
        self.stdscr.addstr("Choose a language: English or Hebrew")
        self.stdscr.refresh()
        return self.stdscr.getstr().decode('utf-8')

    def display_word(self, word: str):
        print(word)

    def display_stats(self, stats: dict):
        print(stats)
import curses
    def display_stats(self, stats: dict):
        print(stats)
