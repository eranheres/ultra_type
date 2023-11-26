import unittest

from ultra_type.statistics import Statistics


class TestStatisticsUpdate(unittest.TestCase):

    def setUp(self):
        self.statistics = Statistics()

    def test_update_success_true(self):
        # Test the update method with success = True
        self.statistics.update(success=True)
        self.assertEqual(self.statistics.total_count, 1)
        self.assertEqual(self.statistics.success_count, 1)

    def test_update_success_false(self):
        # Test the update method with success = False
        self.statistics.update(success=False)
        self.assertEqual(self.statistics.total_count, 1)
        self.assertEqual(self.statistics.success_count, 0)

    def test_update_multiple_calls(self):
        # Test the update method with multiple calls
        for _ in range(3):
            self.statistics.update(success=True)
        for _ in range(2):
            self.statistics.update(success=False)
        self.assertEqual(self.statistics.total_count, 5)
        self.assertEqual(self.statistics.success_count, 3)
class TestStatisticsGetStats(unittest.TestCase):

    def setUp(self):
        self.statistics = Statistics()
        self.statistics.success_count = 80
        self.statistics.total_count = 100

    def test_get_stats_with_non_zero_total(self):
        expected_stats = {'success_rate': 0.8}
        actual_stats = self.statistics.get_stats()
        self.assertEqual(expected_stats, actual_stats)

    def test_get_stats_with_zero_total(self):
        self.statistics.total_count = 0
        expected_stats = {'success_rate': 0}
        actual_stats = self.statistics.get_stats()
        self.assertEqual(expected_stats, actual_stats)

def test_get_stats_with_half_success_rate(self):
        self.statistics.success_count = 50
        self.statistics.total_count = 100
        expected_stats = {'success_rate': 0.5}
        actual_stats = self.statistics.get_stats()
        self.assertEqual(expected_stats, actual_stats)

    def test_get_stats_with_three_quarters_success_rate(self):
        self.statistics.success_count = 30
        self.statistics.total_count = 40
        expected_stats = {'success_rate': 0.75}
        actual_stats = self.statistics.get_stats()
        self.assertEqual(expected_stats, actual_stats)

    def test_get_stats_with_zero_success_rate(self):
        self.statistics.success_count = 0
        self.statistics.total_count = 50
        expected_stats = {'success_rate': 0}
        actual_stats = self.statistics.get_stats()
        self.assertEqual(expected_stats, actual_stats)

if __name__ == '__main__':
    unittest.main()
