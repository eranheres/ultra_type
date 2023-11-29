from ultra_type.languages.language import Language

class Hebrew(Language):
    def __init__(self):
        super().__init__("Hebrew", direction_ltr=False)
        self.hebrew_keyboard_mapping = {
            'q': '/', 'w': "'", 'e': 'ק', 'r': 'ר', 't': 'א', 'y': 'ט', 'u': 'ו', 'i': 'ן', 'o': 'ם', 'p': 'פ',
            'a': 'ש', 's': 'ד', 'd': 'ג', 'f': 'כ', 'g': 'ע', 'h': 'י', 'j': 'ח', 'k': 'ל', 'l': 'ך', ';': 'ף',
            "'": ',',
            'z': 'ז', 'x': 'ס', 'c': 'ב', 'v': 'ה', 'b': 'נ', 'n': 'מ', 'm': 'צ', ',': 'ת', '.': 'ץ', ' ': ' '
        }

    def map_keyboard_layout(self, english_char : chr):
        # Convert the character if it's in the mapping, otherwise return it as is
        return self.hebrew_keyboard_mapping.get(english_char)

    def get_words_filename(self):
        return "ultra_type/hebrew_common_words.json"