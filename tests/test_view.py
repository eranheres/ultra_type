from ultra_type.view import View

class TestView:
    def test_wrap_text(self):
        text = "This is a sample text to demonstrate how the function works with different screen widths."
        screen_width = 20
        expected = [
            "This is a sample ",
            "text to demonstrate ",
            "how the function ",
            "works with different ",
            "screen widths."
        ]
        assert expected == View().wrap_text(text, screen_width)

    def test_index(self):
        response = self.client.get(url_for('index'))
        self.assertEqual(response.status_code, 200)