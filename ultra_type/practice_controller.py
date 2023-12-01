import uuid
import time

class PracticeController:
    def __init__(self, model, view):
        self._model = model
        self._view = view

        self._word_cnt = 0
        self._pos = 0
        self._err_cnt = 0

    def run(self):
        practice = self._model.practice
        practice_str = practice.generate_practice(self._model.language)
        self._view.display_practice(practice_str, self._model.language.is_ltr())
        self._practice_session(practice_str)
        self._start_practice = time.perf_counter()

    def _show_stats(self):
        practice_time = time.perf_counter() - self._start_practice
        self._view.show_rt_practice_stats(
            word_cnt=self._word_cnt,
            wpm=int(self._pos / 5 / (practice_time / 60)),
            accuracy=100 - int(self._err_cnt / (self._pos + 1) * 100)
        )

    def _practice_session(self, practice_str: str):
        practice_guid = str(uuid.uuid4())
        started = False
        while True:
            start = time.perf_counter()
            user_input = self._view.get_user_char(
                                            self._pos,
                                            practice_str,
                                            self._model.language.is_ltr())
            char_time = time.perf_counter() - start
            mapped_char = self._model.language.map_keyboard_layout(user_input)
            if started:
                self._model.update_stats(
                    practice_name=self._model.practice.__class__.__name__,
                    practice_guid=practice_guid,
                    word=practice_str.split(' ')[self._word_cnt],
                    char=practice_str[self._pos],
                    user_input=user_input,
                    time=char_time)
            started = True
            if mapped_char != practice_str[self._pos]:
                self._err_cnt += 1
                continue
            if mapped_char == ' ':
                self._word_cnt += 1
            self._view.display_typed_char(mapped_char,
                                         self._pos,
                                         practice_str,
                                         self._model.language.is_ltr())
            self._pos += 1
            if self.pos >= len(practice_str):
                break


