import uuid

from ultra_type.model import Model
from ultra_type.view import View
from ultra_type.languages.language import English, Hebrew
from ultra_type.practices.practice import PracticeWeakLetters, PracticeRandom, PracticeWeakWords
import time

class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.practices = [PracticeRandom(), PracticeWeakWords(), PracticeWeakLetters()]

    def run(self):
        while True:
            action = self.view.get_main_menu_selection()
            if action == '1':
                self.practice()
            elif action == '2':
                char_times = self.model.statistics.get_char_times(self.model.language.name)
                self.view.show_stats(char_times)
            elif action == '3':
                self._change_lang()
            elif action == '4':
                self._change_practice()
            if action == '5':
                break

    def _change_practice(self):
        self.model.practice = self.view.get_practice_selection([
            PracticeRandom(),
            PracticeWeakWords(),
            PracticeWeakLetters()
        ])

    def _change_lang(self):
        action = self.view.get_language_choice()
        if action == '1':
            self.model.language = English()
        elif action == '2':
            self.model.language = Hebrew()

    def _practice_session(self, practice_str: str):
        practice_guid = str(uuid.uuid4())
        pos = 0
        word_cnt = 0
        err_cnt = 0
        started = False
        start_practice = time.perf_counter()
        while True:
            practice_time = time.perf_counter() - start_practice
            self.view.show_practice_stats(
                word_cnt=word_cnt,
                wpm=int(pos / 5 / (practice_time / 60)),
                accuracy=100 - int(err_cnt / (pos+1) * 100)
            )
            start = time.perf_counter()
            user_input = self.view.get_user_char(pos,
                                                 practice_str,
                                                 self.model.language.is_ltr())
            char_time = time.perf_counter() - start
            mapped_char = self.model.language.map_keyboard_layout(user_input)
            if started:
                self.model.update_stats(
                    practice_name=self.model.practice.__class__.__name__,
                    practice_guid=practice_guid,
                    word=practice_str.split(' ')[word_cnt],
                    char=practice_str[pos],
                    user_input=user_input,
                    time=char_time)
            started = True
            if mapped_char != practice_str[pos]:
                err_cnt += 1
                continue
            if mapped_char == ' ':
                word_cnt += 1
            self.view.display_typed_char(mapped_char,
                                         pos,
                                         practice_str,
                                         self.model.language.is_ltr())
            pos += 1
            if pos >= len(practice_str):
                break

    def practice(self):
        practice = self.model.practice
        practice_str = practice.generate_practice(self.model.language)
        self.view.display_practice(practice_str, self.model.language.is_ltr())
        self._practice_session(practice_str)


# run if main
if __name__ == '__main__':
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.practice()
