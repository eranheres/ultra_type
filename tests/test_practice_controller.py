from ultra_type.practice_controller import PracticeController
from ultra_type.view_practice import ViewPractice

class TestPracticeController:

    def test_get_current_word(self):
        controller = PracticeController(None, ViewPractice(None, 0, 0, True))
        controller.practice_str = "This is a test?!? "
        assert controller._get_current_word(0) == ("This", 0)
        assert controller._get_current_word(3) == ("This", 0)
        assert controller._get_current_word(4) == (" ", 1)
        assert controller._get_current_word(5) == ("is", 2)
        assert controller._get_current_word(8) == ("a", 4)
        assert controller._get_current_word(9) == (" ", 5)
        assert controller._get_current_word(14) == ("?", 7)
        assert controller._get_current_word(15) == ("!", 8)
        assert controller._get_current_word(17) == (" ", 10)

    def test_get_current_word_heb(self):
        controller = PracticeController(None, ViewPractice(None, 0, 0, True))
        controller.practice_str = "זה בדיקה!?."
        assert controller._get_current_word(0) == ("זה", 0)
        assert controller._get_current_word(2) == (" ", 1)
        assert controller._get_current_word(4) == ("בדיקה", 2)
        assert controller._get_current_word(8) == ("!", 3)
        assert controller._get_current_word(10) == (".", 5)
