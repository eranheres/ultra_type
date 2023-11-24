class View:
    def get_user_input(self):
        return input()

    def get_language_choice(self):
        print("Choose a language: English or Hebrew")
        return input()

    def display_word(self, word: str):
        print(word)

    def display_stats(self, stats: dict):
        print(stats)
