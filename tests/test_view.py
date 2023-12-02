from ultra_type.view import View
import unittest

class TestView(unittest.TestCase):
    def test_wrap_text(self):
        text = "This is a sample text to demonstrate how the function works with different screen widths."
        expected = [
            ["This is a sample ",
             "text to demonstrate ",
             "how the function "],
            ["works with different ",
             "screen widths."]
        ]
        view = View()
        view._screen_width = 20
        view._screen_height = 3
        assert expected == View().paginate_text(text)

    def test_get_line_col_for_practice(self):
        text = "This is a sample text to demonstrate how the function works with different screen widths."
        view = View()
        view._screen_width = 20
        view._screen_height = 3
        expected = View().get_line_col_for_practice(0, text)
        assert expected == (0, 0, 0)
        expected = View().get_line_col_for_practice(3, text)
        assert expected == (0, 0, 3)
        expected = View().get_line_col_for_practice(20, text)
        assert expected == (0, 1, 3)
        expected = View().get_line_col_for_practice(50, text)
        assert expected == (0, 2, 13)

    def test_get_line_col_for_practice_out_of_range(self):
        text = "This is a sample text to demonstrate how the function works with different screen widths."
        view = View()
        view._screen_width = 20
        view._screen_height = 3
        # check if exception is raised when pos is out of range
        with self.assertRaises(ValueError, msg="Position out of range"):
            View().get_line_col_for_practice(100, text)


