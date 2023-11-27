from ultra_type.model import Model
from ultra_type.view import View

class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view

    def run(self):
        while True:
            self.view.display_word("Menu:\n1. Change User\n2. Select Language\n3. Practice\n4. Show Stats\n5. Exit")
            self.view.display_word("\nDescriptions:\n1. Change User: Change the current user.\n2. Select Language: Choose the language for practice.\n3. Practice: Practice typing a word in the chosen language.\n4. Show Stats: Display your typing statistics.\n5. Exit: Exit the program. (Enter the option number)\n")
            action = self.view.get_user_input()
            action = int(action)
            if action == 5:
                break
            elif action == 1:
                self.change_user()
            elif action == 2:
                self.select_language()
            elif action == 3:
                self.practice()
            elif action == 4:
                self.show_stats()

    def practice(self):
def change_user(self):
    user = self.view.get_user_input("Enter new user name: ")
    self.model.set_user(user)

def select_language(self):
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
