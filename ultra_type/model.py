from ultra_type.database import Database
from ultra_type.language import Language
from ultra_type.statistics import Statistics

class Model:
    def __init__(self):
        self.database = Database()
        self.language = None
        self.statistics = Statistics()
        self.user = "default"

    def set_language(self, language: str):
        self.language = Language(language)

    def get_word(self):
        return self.language.get_word()

    def check_word(self, word: str):
        return self.language.check_word(word)

    def update_stats(self, success: bool):
        self.statistics.update(success)

    def get_stats(self):
        return self.statistics.get_stats()
    def set_user(self, user: str):
        self.user = user
