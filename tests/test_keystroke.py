import datetime
import unittest

from ultra_type.keystroke import KeyStroke


class TestKeyStroke(unittest.TestCase):

    def setUp(self):
        self.test_character = 'a'
        self.keystroke = KeyStroke(self.test_character)

    def test_character_set_correctly(self):
        self.assertEqual(self.keystroke.character, self.test_character)

    def test_timestamp_set_correctly(self):
        now = datetime.datetime.now()
        self.assertAlmostEqual(self.keystroke.timestamp, now, delta=datetime.timedelta(seconds=1))

if __name__ == '__main__':
    unittest.main()
