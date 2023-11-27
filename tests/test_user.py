import unittest
from unittest.mock import patch

from ultra_type.model import Model


class TestUser(unittest.TestCase):

    @patch("ultra_type.model.Model.set_user")
    def test_set_user_valid_string(self, mock_set_user):
        model = Model()
        user = "test_user"
        model.set_user(user)
        mock_set_user.assert_called_once_with(user)
        self.assertEqual(model.user, user)

    @patch("ultra_type.model.Model.set_user")
    def test_set_user_empty_string(self, mock_set_user):
        model = Model()
        user = ""
        model.set_user(user)
        mock_set_user.assert_called_once_with(user)
        self.assertEqual(model.user, user)

    def test_set_user_non_string(self):
        model = Model()
        user = 123
        with self.assertRaises(TypeError):
            model.set_user(user)

if __name__ == "__main__":
    unittest.main()
