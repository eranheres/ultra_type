from ultra_type.clicker import Clicker
class ViewPractice:

    def __init__(self, stdscr, win_width: int, win_height: int, is_ltr: bool):
        self._max_width = win_width
        self._max_height = win_height
        self._stdscr = stdscr
        self._is_ltr = is_ltr
        self._current_page = -1
        self.clicker = Clicker()

    def set_practice_text(self, practice_text: str):
        self._practice_text = practice_text
        self._pages = self._paginate_text(practice_text, int(self._max_height/2))

    def _get_pos_of_practice(self, pos: int) -> (int, int, int):
        line_cnt = 0
        page_cnt = 0
        for page in self._pages:
            for line in page:
                if pos < len(line):
                    return page_cnt, line_cnt, pos
                pos -= len(line)
                line_cnt += 1
            page_cnt += 1
        raise ValueError("Position is out of range")

    def _get_x_y_of_practice(self, pos: int):
        page, line, col = self._get_pos_of_practice(pos)
        y = (line % self._max_height) * 2 + 1
        if not self._is_ltr:
            x = self._max_width - col
        else:
            x = col
        return x, y

    def display_typed_char(self, char: str, pos: int):
        x, y = self._get_x_y_of_practice(pos)
        self._stdscr.move(y, x)
        self._stdscr.addstr(char)
        self._stdscr.refresh()

    # Gets a key stroke from the user at a specific position and return it and return the time it took to type it
    def get_user_key(self, pos: int) -> str:
        x, y = self._get_x_y_of_practice(pos)
        self._stdscr.move(y, x)
        return self._stdscr.getkey()

    def _paginate_text(self, text: str, max_height: int):
        words = text.split()
        pages = []
        lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 > self._max_width:
                current_line += " "
                lines.append(current_line)
                if len(lines) == max_height:
                    pages.append(lines)
                    lines = []
                current_line = word
            else:
                if current_line:  # Add a space if it's not the first word in the line
                    current_line += " "
                current_line += word

        # Add the last words and lines if not empty
        if current_line:
            lines.append(current_line)
        if lines != []:
            pages.append(lines)
        return pages

    def refresh_display(self, pos: int):
        page, _, _ = self._get_pos_of_practice(pos)
        if page == self._current_page:
            return
        self._current_page = page
        self._stdscr.clear()
        line_num = 0
        for line_txt in self._pages[self._current_page]:
            if not self._is_ltr:
                printed_text = line_txt[::-1]
                pos = self._max_width - len(line_txt) + 1
            else:
                printed_text = line_txt
                pos = 0
            self._stdscr.move(line_num*2, pos)
            self._stdscr.addstr(printed_text)
            self._stdscr.refresh()
            line_num += 1

    def _display_str_at(self, y: int, x: int, text: str):
        self._stdscr.move(y, x)
        self._stdscr.addstr(text)
        self._stdscr.refresh()

    def show_rt_practice_stats(self, current_word: str, word_cnt: int, wpm: int, accuracy: int, pos: int, last_char, errors):
        x = self._max_width + 5
        self._display_str_at(0, x, f"Word count: {word_cnt}\n")
        self._display_str_at(1, x, f"WPM: {wpm}\n")
        self._display_str_at(2, x, f"Accuracy: {accuracy}%\n")
        self._display_str_at(3, x, f"-----------------\n")
        self._display_str_at(4, x, f"Pos: {pos}\n")
        self._display_str_at(5, x, f"Page: {self._current_page}\n")
        self._display_str_at(6, x, f"Expected: {self._practice_text[pos]}\n")
        self._display_str_at(7, x, f"Last Typed: {last_char}\n")
        self._display_str_at(8, x, f"Errors: {errors}\n")
        self._display_str_at(0, x, f"Current word: {current_word}\n")
        self._stdscr.refresh()
