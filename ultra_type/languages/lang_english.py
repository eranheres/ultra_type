from ultra_type.languages.language import Language


class English(Language):

    def __init__(self):
        super().__init__(language="English", direction_ltr=True)

    def map_keyboard_layout(self, english_char : chr):
        return english_char

    def get_words_filename(self):
        return "ultra_type/english_common_words.json"