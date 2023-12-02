
from ultra_type.model import Model
from ultra_type.view import View
from ultra_type.languages.language import English, Hebrew
from ultra_type.practices.practice import PracticeWeakLetters, PracticeRandom, PracticeWeakWords
from ultra_type.practice_controller import PracticeController
from ultra_type.view_practice import ViewPractice

class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.practices = [PracticeRandom(), PracticeWeakWords(), PracticeWeakLetters()]

    def run(self):
        while (True):
            action = self.view.get_main_menu_selection()
            if action == '1':
                view_practice = ViewPractice(
                    self.view.stdscr,
                    self.view.screen_width,
                    self.view.screen_height,
                    self.model.language.is_ltr())
                PracticeController(self.model, view_practice).run()
            elif action == '2':
                self._stats_menu()
            elif action == '3':
                self._change_lang()
            elif action == '4':
                self._change_practice()
            elif action == '5':
                self.model.save_stats()
                self.model.save_setting()
            elif action == '6':
                self.model.save_stats()
                self.model.save_setting()
                exit(0)

    def _stats_menu(self):
        while True:
            choice = self.view.show_stats_menu()
            if choice == '1':
                practice_data = self.model.statistics.get_prtactices_data()
                self.view.show_practice_stats(practice_data)
            elif choice == '2':
                char_times = self.model.statistics.get_char_times(self.model.language.name)
                self.view.show_letters_stats(char_times)
            elif choice == '3':
                break
    def _change_practice(self):
        self.model.practice = self.view.get_practice_selection([
            PracticeRandom(),
            PracticeWeakWords(),
            PracticeWeakLetters()
        ])

    def _change_lang(self):
        action = self.view.show_language_menu()
        if action == '1':
            self.model.language = English()
        elif action == '2':
            self.model.language = Hebrew()

# run if main
if __name__ == '__main__':
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.practice()
