from ultra_type.model import Model
from ultra_type.view import View

class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view

    def run(self):
            while True:
                print("Menu options:")
                print("1. 'quit' - Exit the application")
                print("2. 'practice' - Practice typing in the selected language")
                print("3. 'show_stats' - Display your typing statistics")
                action = self.view.get_user_input()
            if action == 'quit':
                break
            elif action == 'practice':
                self.practice()
            elif action == 'show_stats':
                self.show_stats()

    def practice(self):
        language = self.view.get_language_choice()
        self.model.set_language(language)
        word = self.model.get_word()
        self.view.display_word(word)
        user_input = self.view.get_user_input()
        success = self.model.check_word(user_input)
        self.model.update_stats(success)

    def show_stats(self):
        stats = self.model.get_stats()
        self.view.display_stats(stats)
