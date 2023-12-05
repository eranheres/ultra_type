import uuid
import time
import re
from ultra_type.view_practice import ViewPractice


class PracticeController:
    def __init__(self, model, view: ViewPractice):
        self._model = model
        self._view = view

        self._pos = 0
        self._err_cnt = 0
        self._start_practice = time.perf_counter()
        self.practice_str = ""

    def run(self):
        practice = self._model.practice
        self.practice_str = practice.generate_practice(self._model)
        self._view.set_practice_text(self.practice_str)
        self._practice_session(self.practice_str)

    def _get_current_word(self, pos: int):
        pattern = r'\w+|[^\w\s]|\s'

        # Find all matches in the text
        words = re.findall(pattern, self.practice_str)

        current_pos = 0
        word_count = 0
        for string in words:
            if current_pos + len(string) > pos:
                return string, word_count
            current_pos += len(string)
            word_count += 1

        return None



        current_word = ""
        word_count = 0
        for i in range(0, len(self.practice_str)):
            if self.practice_str[i] in panctuations:
                word_count += 1
                break
            current_word += self.practice_str[i]
        return current_word,

    def _show_stats(self, last_char):
        practice_time = time.perf_counter() - self._start_practice

        word, word_count = self._get_current_word(self._pos)
        self._view.show_rt_practice_stats(
            current_word=word,
            word_cnt=word_count,
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
            user_input = self._view.get_user_key(self._pos)
            if user_input == '\x1b':
                break
            char_time = time.perf_counter() - start
            mapped_char = self._model.language.map_keyboard_layout(user_input)
            if mapped_char == None:
                mapped_char = user_input
            self._show_stats(mapped_char)
            if started:
                current_word, _ = self._get_current_word(self._pos)
                self._model.update_stats(
                    practice_name=self._model.practice.__class__.__name__,
                    practice_guid=practice_guid,
                    word=current_word,
                    char=practice_str[self._pos],
                    user_input=mapped_char,
                    time=char_time)
            if str(mapped_char) != str(practice_str[self._pos]):
                if not prev_had_error:
                    self._err_cnt += 1
                prev_had_error = True
                continue
            started = True
            prev_had_error = False
            self._view.display_typed_char(mapped_char, self._pos)
            self._pos += 1
            if self._pos >= len(practice_str):
                break

