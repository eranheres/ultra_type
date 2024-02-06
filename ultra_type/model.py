from ultra_type.database import Database
from ultra_type.statistics import Statistics
from ultra_type.clicker import Clicker
from ultra_type.languages.language import *

import json
import datetime
import importlib


class Model:

    def __init__(self):
        self.database = Database(db_name="ultra_type.db", stats_fields=Statistics.FIELD_STRACTURE)
        self._language = None
        self._statistics = None
        self._practice = None

        self.clicker = Clicker()
        self.click_sound_enabled = self.clicker.sound_enabled
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
        self._statistics = Statistics(self.database.load_stats(self.language.name))

    def toggle_click_sound(self):
        self.clicker.toggle_sound()
        self.click_sound_enabled = self.clicker.sound_enabled

    @property
    def practice(self):
        return self._practice

    @property
    def click_sound_enabled(self):
        return self._click_sound_enabled

    @click_sound_enabled.setter
    def click_sound_enabled(self, value: bool):
        self._click_sound_enabled = value

    @practice.setter
    def practice(self, practice):
        self._practice = practice

    @property
    def languages(self) -> list:
        return [
            English(),
            Hebrew()
        ]


    def update_stats(self, practice_name: str, practice_guid: str, word: str, char: str, user_input: str, time: float,
                     position: int):
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
        self._practice.attributes["last_position"] = position

    def save_stats(self):
        self.database.save_stats(self.statistics.get_stats())

    def save_setting(self):
        attr = {} if hasattr(self.practice, "attributes") is False else self.practice.attributes
        settings = {"language": self.language.__class__.__name__,
                    "practice": self.practice.__class__.__name__,
                    "practice_attributes": attr,
                    'click_sound_enabled': self.click_sound_enabled}
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
        self.click_sound_enabled = settings.get('click_sound_enabled', True)
        if "practice_attributes" in settings:
            self.practice.attributes = settings["practice_attributes"]
