import json
import random

from ultra_type.languages.language import Language
from ultra_type.model import Model

class Practice:
    def __init__(self, description: str):
        self._description = description

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    def is_lang_supported(self, lang: Language):
        return True

    def generate_practice(self, model: Model):
        assert NotImplementedError("This method must be implemented by the derived class")


class PracticeRandom(Practice):
    def __init__(self):
        super().__init__("Practice random common words")

    def generate_practice(self, model: Model):
        filename = model.language.get_words_filename()
        # read json words file from data/words.json and generate 100 random words string from it
        with open(filename) as f:
            data = json.load(f)
        words = data['words']
        random.shuffle(words)
        rand_words = words[:50]
        return ' '.join(rand_words)


class PracticeLesson(Practice):
    def __init__(self):
        super().__init__("")
        self._attributes = {}

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, attributes: dict):
        self._attributes = attributes
        self.description = attributes["title"]

    def is_lang_supported(self, lang: Language):
        return True

    def generate_practice(self, model: Model):
        filename = self._attributes["filename"]
        # read text file from filename and path ultra_type/data/lessons
        with open(f"ultra_type/data/lessons/{filename}") as f:
            data = f.read()
        return data

class PracticeWeakWords(Practice):
    def __init__(self):
        super().__init__("Practice weak words")

    def generate_practice(self, model: Model):
        data = model.statistics.process_word_data()
        truncated_data = data[0:40]
        random.shuffle(truncated_data)
        return " ".join([record["word"] for record in truncated_data])


class PracticeWeakLetters(Practice):
    def __init__(self):
        super().__init__("Practice weak letters")

    def generate_practice(self, model: Model):
        return "Practice weak letters"
