from ultra_type.view_practice import ViewPractice
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
        view = ViewPractice(stdscr=None, win_width=20, win_height=3, is_ltr=True)
        assert view._paginate_text(text, 3) == expected

    def test_get_line_col_for_practice(self):
        text = "This is a sample text to demonstrate how the function works with different screen widths."
        view = ViewPractice(None, 20, 3*2, True)
        view.set_practice_text(text)
        expected = view._get_pos_of_practice(pos=0)
        assert expected == (0, 0, 0)
        expected = view._get_pos_of_practice(pos=3)
        assert expected == (0, 0, 3)
        expected = view._get_pos_of_practice(pos=20)
        assert expected == (0, 1, 3)
        expected = view._get_pos_of_practice(pos=50)
        assert expected == (0, 2, 13)

    def test_get_line_col_for_practice_out_of_range(self):
        text = "This is a sample text to demonstrate how the function works with different screen widths."
        view = ViewPractice(None, 20, 3*2, True)
        view.set_practice_text(text)
        # check if exception is raised when pos is out of range
        with self.assertRaises(ValueError, msg="Position out of range"):
            view._get_pos_of_practice(pos=100)

