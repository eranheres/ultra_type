class Language:
    def __init__(self, name: str, direction_ltr: bool):
        self._name = name
        self._direction_ltr = direction_ltr

    @property
    def name(self):
        return self._name

    def is_ltr(self):
        return self._direction_ltr

    def map_keyboard_layout(self, english_key: str):
        assert NotImplementedError("This method must be implemented by the derived class")

    def get_words_filename(self):
        assert NotImplementedError("This method must be implemented by the derived class")


class English(Language):

    def __init__(self):
        super().__init__(name="English", direction_ltr=True)

    def map_keyboard_layout(self, english_char : str):
        return english_char

    def get_words_filename(self):
        return "ultra_type/data/english_common_words.json"


class Hebrew(Language):
    def __init__(self):
        super().__init__(name="Hebrew", direction_ltr=False)
        self.hebrew_keyboard_mapping = {
            'q': '/', 'w': "'", 'e': 'ק', 'r': 'ר', 't': 'א', 'y': 'ט', 'u': 'ו', 'i': 'ן', 'o': 'ם', 'p': 'פ',
            'a': 'ש', 's': 'ד', 'd': 'ג', 'f': 'כ', 'g': 'ע', 'h': 'י', 'j': 'ח', 'k': 'ל', 'l': 'ך', ';': 'ף',
            "'": ',', '/': '.',
            'z': 'ז', 'x': 'ס', 'c': 'ב', 'v': 'ה', 'b': 'נ', 'n': 'מ', 'm': 'צ', ',': 'ת', '.': 'ץ', ' ': ' '
        }

    def map_keyboard_layout(self, english_char : str):
        # Convert the character if it's in the mapping, otherwise return it as is
        return self.hebrew_keyboard_mapping.get(english_char)

    def get_words_filename(self):
        return "ultra_type/data/hebrew_common_words.json"
