from ultra_type.database import Database
from ultra_type.languages.language import Language
from ultra_type.statistics import Statistics
from ultra_type.languages.lang_english import English
from ultra_type.practices.practice import PracticeRandom
import datetime

class Model:
    def __init__(self):
        self.database = Database()
        self.language = English() # Default language is English
        self._statistics = Statistics(self.database.load_stats())
        self.practice = PracticeRandom()

    def get_stats(self):
        return self._statistics.get_stats()

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, lang: Language):
        self._language = lang

    @property
    def practice(self):
        return self._practice

    @practice.setter
    def practice(self, practice):
        self._practice = practice

    def update_stats(self, word: str, char: chr, user_input: chr, time: float):
        self._statistics.update({
            "input_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "word": word,
            "char": char,
            "user_input": user_input,
            "time": time,
        })


    def save_stats(self):
        self.database.save_stats(self._statistics.get_stats())