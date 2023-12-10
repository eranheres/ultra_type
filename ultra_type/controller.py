import json
from ultra_type.model import Model
from ultra_type.view import View
from ultra_type.languages.language import English, Hebrew
from ultra_type.practices.practice import PracticeWeakLetters, PracticeRandom, PracticeWeakWords, PracticeLesson
from ultra_type.practice_controller import PracticeController
from ultra_type.view_practice import ViewPractice

class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view

    def run(self):
        while (True):
            action = self.view.get_main_menu_selection(self.model.language.name, self.model.practice.description)
            if action == '1':
                view_practice = ViewPractice(
                    self.view.stdscr,
                    self.view.screen_width-40,
                    self.view.screen_height-4,
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
        stats = []
        while True:
            choice = self.view.show_stats_menu()
            if choice == '1':
                stats = self.model.statistics.prtactices_data()
            elif choice == '2':
                stats = self.model.statistics.letters_data()
            elif choice == '3':
                stats = self.model.statistics.word_data()
            elif choice == '4':
                stats = self.model.statistics.daily_data()
            elif choice == '5':
                break
            self.view.show_stats_from_structure(stats)

    def _change_practice(self):
        practices = [
            PracticeRandom(),
            PracticeWeakWords(),
            PracticeWeakLetters()
        ]
        # load lessons from json file
        with open('ultra_type/data/lessons/dictionary.json') as f:
            data = json.load(f)
        lessons = data['lessons']
        for lesson in lessons:
            if self.model.language.name != lesson["language"]:
                continue
            practice_lesson = PracticeLesson()
            practice_lesson.attributes = lesson
            practices.append(practice_lesson)
        selection = int(self.view.get_practice_selection(practices))
        if selection > len(practices):
            return
        self.model.practice = practices[selection-1]

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
