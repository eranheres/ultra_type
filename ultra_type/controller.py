from ultra_type.model import Model
from ultra_type.view import View

class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view

    def run(self):
        while True:
            self.view.display_word("Menu:\n1. Practice\n2. Show Stats\n3. Exit")
            action = self.view.get_user_number()
            if action == '3':
                self.model.save_stats()
                break
            elif action == '1':
                self.practice()
            elif action == '2':
                self.show_stats()

    def _practice_session(self, practice_str: str):
        pos = 0
        word_cnt = 0
        started = False
        while True:
            user_input, time = self.view.get_user_char(pos)
            started = True
            if started:
                self.model.update_stats(
                    practice_str.split(' ')[word_cnt],
                    practice_str[pos],
                    user_input,
                    time)
            if user_input != practice_str[pos]:
                continue
            if user_input == ' ':
                word_cnt += 1
            self.view.display_typed_char(user_input, pos)
            pos += 1
            if pos >= len(practice_str):
                break

    def practice(self):
        word = "This is a test"
        self.view.display_word(word)
        self._practice_session(word)

    def show_stats(self):
        stats = self.model.get_stats()
        self.view.display_stats(stats)



# run if main
if __name__ == '__main__':
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.practice()