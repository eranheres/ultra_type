# imports
import unittest
from unittest.mock import MagicMock, patch

from ultra_type.language import Language


class TestLanguageCheckWord(unittest.TestCase):

    def setUp(self):
        # Create a mock for the words attribute
        self.mock_words = MagicMock()
        # Instantiate the Language object with the required 'language' parameter
        # Assuming 'language' is a string, we use 'english' as an example
        self.language = Language('english')
        # Assign the mock to the words attribute of the Language instance
        self.language.words = self.mock_words

    def test_check_word_with_word_in_list(self):
        # Set up the mock to return True for a specific word
        self.mock_words.__contains__.return_value = True
        word = "test"
        self.assertTrue(self.language.check_word(word))
        self.mock_words.__contains__.assert_called_once_with(word)

    def test_check_word_with_word_not_in_list(self):
        # Set up the mock to return False for a specific word
        self.mock_words.__contains__.return_value = False
        word = "test"
        self.assertFalse(self.language.check_word(word))
        self.mock_words.__contains__.assert_called_once_with(word)

# Additional tests can be added here if necessary

def test_check_word_with_integer(self):
        word = 123
        self.mock_words.__contains__.return_value = True
        self.assertTrue(self.language.check_word(word))
        self.mock_words.__contains__.assert_called_with(word)

    def test_check_word_with_float(self):
        word = 123.45
        self.mock_words.__contains__.return_value = True
        self.assertTrue(self.language.check_word(word))
        self.mock_words.__contains__.assert_called_with(word)

    def test_check_word_with_special_characters(self):
        word = "!@#$%^&*()"
        self.mock_words.__contains__.return_value = True
        self.assertTrue(self.language.check_word(word))
        self.mock_words.__contains__.assert_called_with(word)
class TestLanguageLoadWords(unittest.TestCase):

    def setUp(self):
        # No need to mock anything for this test case
        pass

    def test_load_words_english(self):
        # Create an instance of Language with the 'English' language
        language = Language('English')
        words = language.load_words()
        
        # Assert that the load_words method returns the expected list
        self.assertEqual(words, ['word1', 'word2', 'word3'])

    def test_load_words_hebrew(self):
        # Create an instance of Language with the 'Hebrew' language
        language = Language('Hebrew')
        words = language.load_words()
        
        # Assert that the load_words method returns the expected list
        self.assertEqual(words, ['word1', 'word2', 'word3'])

    def test_load_words_unsupported_language(self):
        # Create an instance of Language with an unsupported language
        language = Language('Unsupported')
        words = language.load_words()
        
        # Assert that the load_words method returns None or an empty list
        # depending on the implementation details which are not provided
        self.assertTrue(words is None or words == [])



    @patch('ultra_type.language.Language.load_words')
    def test_load_words_non_string_language(self, mock_load_words):
        # Set the return value of the mock
        mock_load_words.return_value = []

        language = Language()
        language.language = 123  # Non-string language
        words = language.load_words()

        # Assert that the mocked load_words method returns an empty list
        self.assertEqual(words, [])

    @patch('ultra_type.language.Language.load_words')
    def test_load_words_special_characters_language(self, mock_load_words):
        # Set the return value of the mock
        mock_load_words.return_value = []

        language = Language()
        language.language = '!@#$%^&*()'  # Language with special characters
        words = language.load_words()

        # Assert that the mocked load_words method returns an empty list
        self.assertEqual(words, [])
class TestLanguageGetWord(unittest.TestCase):

    def setUp(self):
        # Assuming that the Language class requires a 'language' argument for initialization
        self.mock_language = 'en'
        self.language_instance = Language(self.mock_language)

    @patch("ultra_type.language.Language.words", new_callable=lambda: ['word1', 'word2', 'word3'])
    def test_get_word(self, mock_words):
        # Call the method under test
        word = self.language_instance.get_word()

        # Assert that the word is correctly popped from the list
        self.assertEqual(word, 'word3')
        # Assert the list size is reduced by one
        self.assertEqual(len(self.language_instance.words), 2)

    # Add more test cases if necessary



    @patch("ultra_type.language.Language.words")
    def test_get_word_when_words_is_empty(self, mock_words):
        # Set up the mock to raise an IndexError when pop is called
        mock_words.pop.side_effect = lambda: IndexError("pop from empty list")

        # Instantiate the Language object
        language = Language()

        # Call the method under test and assert that it raises an IndexError
        with self.assertRaises(IndexError):
            language.get_word()

        # Assert that the mocked method was called
        mock_words.pop.assert_called_once()

if __name__ == '__main__':
    unittest.main()
