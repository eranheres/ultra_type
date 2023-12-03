from ultra_type.database import Database
from ultra_type.languages.language import Language
from ultra_type.statistics import Statistics
import datetime
import importlib

class Model:

    def __init__(self):
        self.database = Database(db_name="ultra_type.db", stats_fields=Statistics.FIELD_STRACTURE)
        self._statistics = Statistics(self.database.load_stats())
        self.load_setting()

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

    def update_stats(self, practice_name: str, practice_guid: str, word: str, char: str, user_input: str, time: float):
        # generate guid
        self._statistics.update({
            "input_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "practice_name": practice_name,
            "practice_guid": practice_guid,
            "language": self.language.name,
            "word": word,
            "char": char,
            "user_input": user_input,
            "time": time,
        })

    def save_stats(self):
        self.database.save_stats(self.statistics.get_stats())

    def save_setting(self):
        attr = {} if hasattr(self.practice, "attributes") is False else self.practice.attributes
        settings = {
            "language": self.language.__class__.__name__,
            "practice": self.practice.__class__.__name__,
            "practice_attributes": attr
        }
        self.database.save_settings(settings)

    def load_setting(self):
        settings = self.database.load_settings({
            "language": "English",
            "practice": "PracticeRandom",
            "practice_attributes": {}
        })
        module = importlib.import_module("ultra_type.languages.language")
        self.language = getattr(module, settings["language"])()
        module = importlib.import_module("ultra_type.practices.practice")
        self.practice = getattr(module, settings["practice"])()
        if "practice_attributes" in settings:
            self.practice.attributes = settings["practice_attributes"]
