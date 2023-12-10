import unittest
from unittest.mock import patch


from ultra_type.model import Model


class TestModelUpdateStats(unittest.TestCase):

    @patch("ultra_type.statistics.Statistics.update")
    def test_update_stats(self, mock_statistics_update):
        # Arrange
        model = Model()

        # Act
        model.update_stats(
            practice_name= "practice_name",
            practice_guid= "practice_guid",
            word="word",
            char=chr(99),
            user_input="u",
            time=0.0,
            position=1)

        # Assert
        mock_statistics_update.assert_called_once()


class TestModelGetStats(unittest.TestCase):

    @patch("ultra_type.statistics.Statistics.get_stats")
    def test_get_stats(self, mock_get_stats):
        # Arrange
        mock_get_stats.return_value = {"total_games": 10, "average_score": 95}
        model = Model()

        # Act
        stats = model.statistics.get_stats()

        # Assert
        mock_get_stats.assert_called_once()
        self.assertEqual(stats, {"total_games": 10, "average_score": 95})

    @patch("ultra_type.statistics.Statistics.get_stats")
    def test_get_stats_when_no_games_played(self, mock_get_stats):
        # Arrange
        mock_get_stats.return_value = {"total_games": 0, "average_score": 0}
        model = Model()

        # Act
        stats = model.statistics.get_stats()

        # Assert
        mock_get_stats.assert_called_once()
        self.assertEqual(stats, {"total_games": 0, "average_score": 0})

    @patch("ultra_type.database.Database.save_stats")
    def test_save_stats(self, mock_save_stats):
        # Arrange
        model = Model()

        # Act
        model.save_stats()

        # Assert
        mock_save_stats.assert_called_once()
        self.assertTrue(True)




if __name__ == "__main__":
    unittest.main()

