class Language:
    def __init__(self, language: str, direction_ltr: bool):
        self.language = language
        self._direction_ltr = direction_ltr

    def is_ltr(self):
        return self._direction_ltr

    def map_keyboard_layout(self, english_char : chr):
        assert NotImplementedError("This method must be implemented by the derived class")

    def get_words_filename(self):
        assert NotImplementedError("This method must be implemented by the derived class")