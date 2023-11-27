from ultra_type.model import Model
from ultra_type.view import View

class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view

    def run(self):
        while True:
            self.view.display_word("Menu:\n1. Practice\n2. Show Stats\n3. Exit")
            self.view.display_word("\nDescriptions:\n1. Practice: Practice typing a word in a chosen language.\n2. Show Stats: Display your typing statistics.\n3. Exit: Exit the program. (Enter the option number)\n")
            action = self.view.get_user_input()
            action = int(action)
            if action == 3:
                break
            elif action == 1:
                self.practice()
            elif action == 2:
                self.show_stats()

    def practice(self):
        """
        The Controller class is responsible for managing the interaction between the Model and View classes.
        """

def __init__(self, model: Model, view: View):
    """
    Initializes a new instance of the Controller class with a given Model and View.
    """
    self.model = model
    self.view = view

def run(self):
    """
    Runs the main loop of the program, which involves displaying the menu, getting user input, 
    and calling the appropriate method based on the user's choice.
    """
    while True:
        self.view.display_word("Menu:\n1. Practice\n2. Show Stats\n3. Exit")
        self.view.display_word("\nDescriptions:\n1. Practice: Practice typing a word in a chosen language.\n2. Show Stats: Display your typing statistics.\n3. Exit: Exit the program. (Enter the option number)\n")
        action = self.view.get_user_input()
        action = int(action)
        if action == 3:
            break
        elif action == 1:
            self.practice()
        elif action == 2:
            self.show_stats()
        language_choice = self.view.get_language_choice()
        language = 'English' if language_choice == 1 else 'Hebrew' if language_choice == 2 else None
        self.model.set_language(language)
        word = self.model.get_word()
        self.view.display_word(word)
        user_input = self.view.get_user_input()
        success = self.model.check_word(user_input)
        self.model.update_stats(success)

    def show_stats(self):
        stats = self.model.get_stats()
        self.view.display_stats(stats)
    def practice(self):
        """
        Allows the user to practice typing a word in a chosen language, checks the user's input against the correct word, 
        and updates the user's statistics based on whether they typed the word correctly.
        """
    language_choice = self.view.get_language_choice()
    language = 'English' if language_choice == 1 else 'Hebrew' if language_choice == 2 else None
    self.model.set_language(language)
    word = self.model.get_word()
    self.view.display_word(word)
    user_input = self.view.get_user_input()
    success = self.model.check_word(user_input)
    self.model.update_stats(success)

    def show_stats(self):
        """
        Retrieves the user's typing statistics from the Model and displays them using the View.
        """
    stats = self.model.get_stats()
    self.view.display_stats(stats)
