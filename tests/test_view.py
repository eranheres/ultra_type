import unittest
from unittest.mock import patch

from ultra_type.keystroke import KeyStroke
from ultra_type.view import View


class TestViewGetUserInput(unittest.TestCase):

    def setUp(self):
        self.view = View()

    @patch('builtins.input', return_value='a')
    def test_get_user_input_single_character(self, mock_input):
        keystrokes = self.view.get_user_input()
        self.assertEqual(len(keystrokes), 1)
        self.assertIsInstance(keystrokes[0], KeyStroke)
        self.assertEqual(keystrokes[0].character, 'a')

    @patch('builtins.input', return_value='abc')
    def test_get_user_input_multiple_characters(self, mock_input):
        keystrokes = self.view.get_user_input()
        self.assertEqual(len(keystrokes), 3)
        for i, keystroke in enumerate(keystrokes):
            self.assertIsInstance(keystroke, KeyStroke)
            self.assertEqual(keystroke.character, 'abc'[i])

    @patch('builtins.input', return_value='abc')
    def test_get_user_input_keystroke_timestamps(self, mock_input):
        keystrokes = self.view.get_user_input()
        for i in range(len(keystrokes) - 1):
            self.assertIsNotNone(keystrokes[i].timestamp)
            self.assertLess(keystrokes[i].timestamp, keystrokes[i + 1].timestamp)


if __name__ == '__main__':
    unittest.main()
