import json
import re
from ultra_type.model import Model
from ultra_type.practices.practice import PracticeWeakLetters, PracticeRandom, PracticeWeakWords, PracticeLesson
from ultra_type.clicker import Clicker
import time
import uuid


class Controller:
    def __init__(self, model: Model):
        self._model = model
        self._current_pos = 0
        self._text = ""
        self._timer = None
        self._practice_guid = str(uuid.uuid4())
        self._practice_time = None
        self._error_count = 0
        self._start_pos = 0
        self._clicker = Clicker(model.click_sound_enabled)

    @property
    def model(self):
        return self._model

    @property
    def current_pos(self):
        return self._current_pos

    @property
    def start_pos(self):
        return self._start_pos

    @property
    def error_count(self):
        return self._error_count

    @property
    def languages(self) -> list:
        return self.model.languages

    @property
    def practice_time(self):
        if self._practice_time:
            return time.perf_counter() - self._practice_time
        return 0

    @property
    def practices(self) -> list:
        practices = [
            PracticeRandom(),
            PracticeWeakWords(),
            PracticeWeakLetters()
        ]
        # load lessons from json file
        with open('ultra_type/data/lessons/dictionary.json') as f:
            data = json.load(f)
        lessons = data['lessons']
        for lesson in lessons:
            if self.model.language.name != lesson["language"]:
                continue
            practice_lesson = PracticeLesson()
            practice_lesson.attributes = lesson
            practices.append(practice_lesson)
        return practices

    def reset(self):
        self._current_pos = 0
        self._timer = None
        self._practice_guid = str(uuid.uuid4())
        self._practice_time = None
        self._error_count = 0
        self._start_pos = 0

    def pause(self):
        self._timer = None
        self._practice_time = None

    def reset_practice(self, text, pos):
        self._practice_guid = str(uuid.uuid4())
        self._practice_time = time.perf_counter()
        self._text = text
        self._current_pos = pos
        self._start_pos = pos
        self._error_count = 0

    def language_idx(self, lang: str = None) -> int:
        if lang is None:
            lang = self.model.language.name
        return next(i for i, obj in enumerate(self.model.languages) if obj.name == lang)

    def practice_idx(self, desc: str = None) -> int:
        if desc is None:
            desc = self.model.practice.description
        return next(i for i, obj in enumerate(self.practices) if obj.description == desc)

    def get_current_word(self):
        pattern = r'\w+|[^\w\s]|\s'

        # Find all matches in the text
        words = re.findall(pattern, self._text)

        current_pos = 0
        word_count = 0
        for string in words:
            if current_pos + len(string) > self._current_pos:
                return string, word_count
            current_pos += len(string)
            word_count += 1

        return None

    def _update_stats(self, mapped_char, timing):
        current_word, _ = self.get_current_word()
        self.model.update_stats(
            practice_name=self.model.practice.__class__.__name__,
            practice_guid=self._practice_guid,
            word=current_word,
            char=self._text[self._current_pos],
            user_input=mapped_char,
            time=timing,
            position=self._current_pos)

    def sound_enabled(self, value: bool):
        self._clicker.sound_enabled = value
        self.model.click_sound_enabled = value

    def get_current_key(self):
        return self._text[self._current_pos]

    def on_key(self, key_char) -> int:
        self._clicker.click()
        mapped_char = self.model.language.map_keyboard_layout(key_char)
        delta_time = None
        if self._timer:
            delta_time = time.perf_counter() - self._timer
        else:
            self._practice_time = time.perf_counter()
        self._timer = time.perf_counter()
        if mapped_char == str(self._text[self._current_pos]):
            self._current_pos += 1
        else:
            self._error_count += 1
        if delta_time:
            self._update_stats(mapped_char, delta_time)
        return self._current_pos

# run if main
