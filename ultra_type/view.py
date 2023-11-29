import curses
import time
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

    def get_user_number(self):
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
        self.display_str_at(0, 40, f"y: {y} x: {x}")
        if not is_ltr:
            self.stdscr.move(y * 2 + 1, self.screen_width - x - 1)
        else:
            self.stdscr.move(y * 2 + 1, x)
        self.stdscr.addstr(char)
        self.stdscr.refresh()

    # Gets a key stroke from the user at a specific position and return it and return the time it took to type it
    def get_user_char(self, pos: int, practice: str, is_ltr: bool):
        y, x = self.get_line_col_for_practice(pos, practice)
        start = time.perf_counter()
        if not is_ltr:
            self.stdscr.move(y * 2 + 1, self.screen_width - x - 1)
        else:
            self.stdscr.move(y * 2 + 1, x)
        c = chr(self.stdscr.getch())
        end = time.perf_counter()
        return c, end - start

    def get_user_text(self):
        # use curses to get user input character by character
        self.stdscr.keypad(True)
        user_input = ''
        while True:
            c = chr(self.stdscr.getch())
            c = self.get_user_char(2, False)
            if c == '\n':
                break
            # echo the character back to the screen
            self.stdscr.addstr(str(c))
            user_input += c

        return user_input

    def get_language_choice(self):
        self.stdscr.addstr("Choose a language: 1. English 2. Hebrew")
        self.stdscr.refresh()
        choice = int(self.stdscr.getstr().decode('utf-8'))
        return 'English' if choice == 1 else 'Hebrew' if choice == 2 else None

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

    def display_stats(self, stats: list):
        self.stdscr.clear()
        stat_str = self.get_average_times(stats)
        self.stdscr.addstr(stat_str)
        self.stdscr.refresh()
        self.stdscr.getch()

    def get_average_times(self, data: list):
        word_times = {}
        char_times = {}

        # Accumulate times and count occurrences
        for entry in data:
            word = entry['word']
            char = entry['char']
            time = entry['time']

            if word in word_times:
                word_times[word]['total'] += time
                word_times[word]['count'] += 1
            else:
                word_times[word] = {'total': time, 'count': 1}

            if char in char_times:
                char_times[char]['total'] += time
                char_times[char]['count'] += 1
            else:
                char_times[char] = {'total': time, 'count': 1}

        # Calculate and print average times for each word
        str = ""
        #str += "Average Time per Word:\n"
        #for word, info in word_times.items():
        #    average = info['total'] / info['count']
        #    str += f"Word '{word}': {average} sec\n"

        # Calculate and print average times for each letter
        str += "\nAverage Time per Character:\n"
        for char, info in char_times.items():
            average = info['total'] / info['count']
            str += f"Character '{char}': {average} sec\n"
        return str


# No lines to replace

# run if main
if __name__ == '__main__':
    view = View()
    word = view.get_user_input()
    view.display_word('got: ' + word)