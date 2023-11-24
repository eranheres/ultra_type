from ultra_type.model import Model
from ultra_type.view import View

class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view

    def run(self):
            print("Welcome to Ultra Type! Here are your options:")
            print("'quit': Exit the program")
            print("'practice': Practice typing in the chosen language")
            print("'show_stats': Display your typing statistics")
            print("Please choose an action from the menu.")
            while True:
                action = self.view.get_user_input()
                if action == 'quit':
                    print("You have chosen to quit the program.")
                    break
                elif action == 'practice':
                    print("You have chosen to practice.")
                    self.practice()
                elif action == 'show_stats':
                    print("You have chosen to show your statistics.")
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
