import curses
import pandas as pd
from ultra_type.curses_mock import CursesMock

class View:
    def __init__(self):
        self.screen_width = 20
        try:
            self.stdscr = curses.initscr()
            self.curses_available = True
            curses.noecho()
            curses.cbreak()
        except:
            self.curses_available = False
            self.stdscr = CursesMock()

    def __del__(self):
        if self.curses_available:
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
            "Letters speed statistics"])

    def show_rt_practice_stats(self, word_cnt: int, wpm: int, accuracy: int):
        self.display_str_at(0, 50, f"Word count: {word_cnt}\n")
        self.display_str_at(1, 50, f"WPM: {wpm}\n")
        self.display_str_at(2, 50, f"Accuracy: {accuracy}%\n")
        self.stdscr.refresh()

    def get_user_key(self):
        # start a timer
        return chr(self.stdscr.getch())

    def get_line_col_for_practice(self, pos: int, practice: str):
        wrapped = self.wrap_text(practice, self.screen_width)
        line_cnt = 0
        for line in wrapped:
            if pos < len(line):
                return line_cnt, pos
            pos -= len(line)
            line_cnt += 1

    def display_str_at(self, y: int, x: int, text: str):
        self.stdscr.move(y, x)
        self.stdscr.addstr(text)
        self.stdscr.refresh()

    def display_typed_char(self, char: str, pos: int, practice: str, is_ltr):
        y, x = self.get_line_col_for_practice(pos, practice)
        if not is_ltr:
            self.stdscr.move(y * 2 + 1, self.screen_width - x - 1)
        else:
            self.stdscr.move(y * 2 + 1, x)
        self.stdscr.addstr(char)
        self.stdscr.refresh()

    # Gets a key stroke from the user at a specific position and return it and return the time it took to type it
    def get_user_char(self, pos: int, practice: str, is_ltr: bool):
        y, x = self.get_line_col_for_practice(pos, practice)
        if not is_ltr:
            self.stdscr.move(y * 2 + 1, self.screen_width - x - 1)
        else:
            self.stdscr.move(y * 2 + 1, x)
        return chr(self.stdscr.getch())

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

    def wrap_text(self, text, screen_width):
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 > screen_width:
                current_line += " "
                lines.append(current_line)
                current_line = word
            else:
                if current_line:  # Add a space if it's not the first word in the line
                    current_line += " "
                current_line += word

        # Add the last line if it's not empty
        if current_line:
            lines.append(current_line)

        return lines

    def display_practice(self, words: [], is_ltr):
        self.stdscr.clear()
        lines = self.wrap_text(words, self.screen_width)
        line_num = 0
        for line in lines:
            if not is_ltr:
                printed_text = line[::-1]
                pos = self.screen_width - len(line)
            else:
                printed_text = line
                pos = 0
            self.stdscr.move(line_num*2, pos)
            self.stdscr.addstr(printed_text)
            self.stdscr.refresh()
            line_num += 1

    def show_letters_stats(self, char_times: {}):
        str = "Average Time per Character:\n"
        for char, info in char_times.items():
            average = info['total'] / info['count']
            str += f"Character '{char}': {average} sec\n"
        self.display_text(str)
        self.get_user_key()

    def show_practice_stats(self, practice_stats: []):
        df = pd.DataFrame(practice_stats)
        tbl = df.to_string(index=False)
        self.display_text(tbl)
        self.get_user_key()

    def get_practice_selection(self, practices: []):
        pass
        #return self._display_menu([practice.description for practice in practices])

# run if main
if __name__ == '__main__':
    view = View()
    word = view.get_user_input()
    view.display_word('got: ' + word)