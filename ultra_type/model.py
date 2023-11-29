from ultra_type.database import Database
from ultra_type.languages.language import Language
from ultra_type.statistics import Statistics
import datetime
import importlib

class Model:
    def __init__(self):
        self.database = Database()
        self._statistics = Statistics(self.database.load_stats())
        self.load_setting()

    def __del__(self):
        self.save_stats()
        self.save_setting()

    @property
    def statistics(self):
        return self._statistics

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
            "language": self.language.name,
            "word": word,
            "char": char,
            "user_input": user_input,
            "time": time,
        })

    def save_stats(self):
        self.database.save_stats(self._statistics.get_stats())

    def save_setting(self):
        settings = {
            "language": self.language.__class__.__name__,
            "practice": self.practice.__class__.__name__
        }
        self.database.save_settings(settings)

    def load_setting(self):
        settings = self.database.load_settings({
            "language": "English",
            "practice": "PracticeRandom"
        })
        module = importlib.import_module("ultra_type.languages.language")
        self.language = getattr(module, settings["language"])()
        module = importlib.import_module("ultra_type.practices.practice")
        self.practice = getattr(module, settings["practice"])()
