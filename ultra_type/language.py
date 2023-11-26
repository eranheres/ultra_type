class Language:
    def __init__(self, language: str):
        self.language = language
        self.words = self.load_words()

    def load_words(self):
        if self.language == 'English':
            return ['word1', 'word2', 'word3']  # Load the 1000 most popular English words
        elif self.language == 'Hebrew':
            return ['word1', 'word2', 'word3']  # Load the 1000 most popular Hebrew words
        else:
            return []  # Unsupported language

    def get_word(self):
        return self.words.pop()

    def check_word(self, word: str):
        return word in self.words
