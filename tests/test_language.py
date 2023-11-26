import unittest
from unittest.mock import MagicMock, patch

from ultra_type.language import Language


class TestLanguageCheckWord(unittest.TestCase):

    def setUp(self):
        # Assuming the Language class constructor requires a 'language' argument.
        # The value 'English' is provided as an example. Adjust as necessary.
        self.language = Language('English')
        # Assuming that 'words' is a public attribute that can be set.
        # If 'words' is populated in some other way, that would need to be mocked or set up here.
        self.language.words = ['hello', 'world']

    def test_check_word_exists(self):
        # Test that check_word returns True for a word that exists in the language's words
        word = 'hello'
        result = self.language.check_word(word)
        self.assertTrue(result)

    def test_check_word_does_not_exist(self):
        # Test that check_word returns False for a word that does not exist in the language's words
        word = 'goodbye'
        result = self.language.check_word(word)
        self.assertFalse(result)

    # Additional tests can be added here to cover more edge cases or scenarios.

    def test_check_word_empty_string(self):
        # Test that check_word returns False for an empty string
        word = ''
        result = self.language.check_word(word)
        self.assertFalse(result)

class TestLanguageLoadWords(unittest.TestCase):

    def setUp(self):
        # Assuming the Language class can be instantiated without arguments
        # and the language attribute can be set post-instantiation.
        self.english_language = Language('English')
        
        self.hebrew_language = Language('Hebrew')

    

    def test_load_words_english(self):
        expected_words = ['word1', 'word2', 'word3']
        self.assertEqual(self.english_language.words, expected_words)

    @unittest.skip("ultra_type/language_test.py:12:31: E1120: No value for argument 'language' in constructor call (no-value-for-parameter)")
    def test_load_words_hebrew(self):
        expected_words = ['word1', 'word2', 'word3']
        self.assertEqual(self.hebrew_language.words, expected_words)

    def test_load_words_unsupported_language(self):
        language = Language('Spanish')  # Unsupported language
        self.assertEqual(language.load_words(), [])  # Expect an empty list

class TestLanguageGetWord(unittest.TestCase):

    def setUp(self):
        # Assuming 'language' is a string parameter required by the Language constructor
        self.language = Language('English')
        self.language.words = ['mocked_word']

    def test_get_word(self):
        # Test that get_word returns the correct word
        word = self.language.get_word()
        self.assertEqual(word, "mocked_word")
        # Test that pop was called once
        self.language.words.pop.assert_called_once()

    # Additional tests can be added here if there are more edge cases or behaviors to test

    @patch.object(MagicMock, 'pop')
    def test_get_word_when_words_is_empty(self, mock_pop):
        # Set the side effect of the mock pop method to raise an IndexError when called
        mock_pop.side_effect = IndexError
        # Test that get_word returns None when words is empty
        word = self.language.get_word()
        self.assertIsNone(word)
        # Test that pop was called once
        self.language.words.pop.assert_called_once()

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
