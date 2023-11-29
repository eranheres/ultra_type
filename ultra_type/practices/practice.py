import json
import random

from ultra_type.languages.language import Language

class Practice:
    def __init__(self, name: str):
        self.name = name

    def generate_practice(self, lang: Language):
        assert NotImplementedError("This method must be implemented by the derived class")


class PracticeRandom(Practice):
    def __init__(self):
        super().__init__("Practice random common words")

    def generate_practice(self, lang: Language):
        filename = lang.get_words_filename()
        # read json words file from data/words.json and generate 100 random words string from it
        with open(filename) as f:
            data = json.load(f)
        words = data['words']
        random.shuffle(words)
        rand_words = words[:20]
        return ' '.join(rand_words)


class PracticeWeakWords(Practice):
    def __init__(self):
        super().__init__("Practice weak words")

    def generate_practice(self, lang: Language):
        return "Practice weak words"


class PracticeWeakLetters(Practice):
    def __init__(self):
        super().__init__("Practice weak letters")

    def generate_practice(self, lang: Language):
        return "Practice weak letters"
