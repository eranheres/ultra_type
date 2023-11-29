from ultra_type.model import Model
from ultra_type.view import View
from ultra_type.languages.lang_english import English
from ultra_type.languages.lang_hebrew import Hebrew

from ultra_type.practices.practice import PracticeWeakLetters, PracticeRandom, PracticeWeakWords
class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.practices = [PracticeRandom(), PracticeWeakWords(), PracticeWeakLetters()]

    def run(self):
        while True:
            self.view.display_text("Menu:\n1. Practice\n2. Show Stats\n3. Change Language\n4. Change practice.\n5. Exit\n")
            action = self.view.get_user_number()
            if action == '1':
                self.practice()
            elif action == '2':
                self.show_stats()
            elif action == '3':
                self._change_lang()
            elif action == '4':
                self._change_practice()
            if action == '5':
                self.model.save_stats()
                break


    def _change_practice(self):
        self.view.display_text("Choose practice:\n1. Random\n2. Weak Words\n3. Weak Letters\n")
        action = self.view.get_user_number()
        if action == '1':
            self.model.practice = PracticeRandom()
        elif action == '2':
            self.model.practice = PracticeWeakWords()
        elif action == '3':
            self.model.practice = PracticeWeakLetters()

    def _change_lang(self):
        self.view.display_text("Choose language:\n1. English\n2. Hebrew\n")
        action = self.view.get_user_number()
        if action == '1':
            self.model.language = English()
        elif action == '2':
            self.model.language = Hebrew()

    def _practice_session(self, practice_str: str):
        pos = 0
        word_cnt = 0
        started = False
        while True:
            user_input, time = self.view.get_user_char(pos,
                                                       practice_str,
                                                       self.model.language.is_ltr())
            mapped_char = self.model.language.map_keyboard_layout(user_input)
            if started:
                self.model.update_stats(
                    practice_str.split(' ')[word_cnt],
                    practice_str[pos],
                    mapped_char,
                    time)
            started = True
            if mapped_char != practice_str[pos]:
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

    def show_stats(self):
        stats = self.model.get_stats()
        self.view.display_stats(stats)


# run if main
if __name__ == '__main__':
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.practice()