from ultra_type.database import Database
from ultra_type.language import Language
from ultra_type.statistics import Statistics

class Model:
    def __init__(self):
        self.database = Database()
        self.language = None
        self.statistics = Statistics(self.database.load_stats())

    def set_language(self, language: str):
        self.language = Language(language)

    def get_word(self):
        return self.language.get_word()

    def check_word(self, word: str):
        return self.language.check_word(word)

    def update_stats(self, word: str, char: chr, user_input: chr, time: float):
        self.statistics.update({
            "word": word,
            "char": char,
            "user_input": user_input,
            "time": time,
        })

    def get_stats(self):
        return self.statistics.get_stats()

    def save_stats(self):
        self.database.save_stats(self.statistics.get_stats())