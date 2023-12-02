import uuid
import time
import curses
from ultra_type.view_practice import ViewPractice

class PracticeController:
    def __init__(self, model, view: ViewPractice):
        self._model = model
        self._view = view

        self._word_cnt = 0
        self._pos = 0
        self._err_cnt = 0
        self._start_practice = time.perf_counter()

    def run(self):
        practice = self._model.practice
        practice_str = practice.generate_practice(self._model)
        self._view.set_practice_text(practice_str)
        self._practice_session(practice_str)

    def _show_stats(self, last_char):
        practice_time = time.perf_counter() - self._start_practice
        self._view.show_rt_practice_stats(
            word_cnt=self._word_cnt,
            wpm=int(self._pos / 5 / (practice_time / 60)),
            accuracy=(100 - int(self._err_cnt / (self._pos + 1) * 100)),
            pos=self._pos,
            last_char=last_char,
            errors=self._err_cnt
        )

    def _practice_session(self, practice_str: str):
        practice_guid = str(uuid.uuid4())
        started = False
        prev_had_error = False
        while True:
            self._view.refresh_display(self._pos)
            start = time.perf_counter()
            user_input = self._view.get_user_char(self._pos)
            char_time = time.perf_counter() - start
            mapped_char = self._model.language.map_keyboard_layout(user_input)
            self._show_stats(mapped_char)
            if started:
                self._model.update_stats(
                    practice_name=self._model.practice.__class__.__name__,
                    practice_guid=practice_guid,
                    word=practice_str.split(' ')[self._word_cnt],
                    char=practice_str[self._pos],
                    user_input=user_input,
                    time=char_time)
            started = True
            if str(mapped_char) != str(practice_str[self._pos]):
                if not prev_had_error:
                    self._err_cnt += 1
                prev_had_error = True
                continue
            prev_had_error = False
            if mapped_char == ' ':
                self._word_cnt += 1
            self._view.display_typed_char(mapped_char, self._pos)
            self._pos += 1
            if self._pos >= len(practice_str):
                break


if __name__ == '__main__':
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    from ultra_type.model import Model
    from ultra_type.view_practice import ViewPractice

    PracticeController(Model(), ViewPractice(stdscr,20,4,True)).run()
