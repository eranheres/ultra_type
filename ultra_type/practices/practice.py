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

    @property
    def attributes(self):
        return {}

    @attributes.setter
    def attributes(self, attributes: dict):
        pass

    def is_lang_supported(self, lang: Language):
        return True

    def generate_practice(self, model: Model) -> (str, int):
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
        return ' '.join(rand_words), 0


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
        self.last_poistion = attributes["last_position"] if "last_position" in attributes else 0

    def is_lang_supported(self, lang: Language):
        return True

    def generate_practice(self, model: Model) -> (str, int):
        filename = self._attributes["filename"]
        # read text file from filename and path ultra_type/data/lessons
        with open(f"ultra_type/data/lessons/{filename}") as f:
            data = f.read()
        data = data.replace("\n", "").replace('’', "'").replace("‘", "'").replace("”", '"').\
                    replace("“", '"').replace("—", "-").replace("…", "...").replace("–", "-").\
                    replace("—", "-").replace("**", "")
        last_position = 0
        if "last_position" in self._attributes:
            last_position = self._attributes["last_position"]
            if last_position >= len(data):
                last_position = 0
            else:
                last_position = data[:last_position].rfind(".")+1

        return data, last_position

class PracticeWeakWords(Practice):
    def __init__(self):
        super().__init__("Practice weak words")

    def generate_practice(self, model: Model) -> (str, int):
        word_data = model.statistics.word_data()
        if len(word_data) == 0:
            return ".", 0
        weights = [record["error_rate"]*100+(100-record["wpm"]) for record in word_data]
        words_list = [record["word"] for record in random.choices(word_data, weights=weights, k=40)]
        return " ".join([record for record in words_list]), 0


class PracticeWeakLetters(Practice):
    def __init__(self):
        super().__init__("Practice weak letters")

    def generate_practice(self, model: Model) -> (str, int):
        word_data = model.statistics.word_data()
        if len(word_data) == 0:
            return ".", 0
        letters_raw = model.statistics.letters_data()
        letters = []
        for record in letters_raw:
            if record["char"] not in [" ", "\n", ".", "?", "!", ",", ";", ":", "-", "(", ")", "[", "]", "{", "}"]:
                letters.append(record)
        words_per_letter = {}
        for letter in letters:
            words_per_letter[letter["char"]] = [record["word"] for record in word_data if letter["char"] in record["word"]]
            if len(words_per_letter[letter["char"]]) == 0:
                Exception(f"no words for letter '{letter}'")
        weights = [record["error_rate"]*100+(100-record["wpm"]) for record in letters]
        letters_to_practice = random.choices(letters, weights=weights, k=60)
        # for each letter in letters_to_practice, choose a random word from words_per_letter
        words_to_practice = [random.choice(words_per_letter[letter["char"]]) for letter in letters_to_practice]
        return " ".join(words_to_practice), 0
