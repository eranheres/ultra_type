import unittest

from ultra_type.statistics import Statistics


class TestStatisticsGetStats(unittest.TestCase):

    def setUp(self):
        self.statistics = Statistics()
        self.statistics.success_count = 0
        self.statistics.total_count = 0

    def test_get_stats_zero_total(self):
        stats = self.statistics.get_stats()
        self.assertEqual(stats['success_rate'], 0)

    def test_get_stats_non_zero_total(self):
        self.statistics.success_count = 80
        self.statistics.total_count = 100
        stats = self.statistics.get_stats()
        self.assertEqual(stats['success_rate'], 0.8)

def test_get_stats_zero_total(self):
        stats = self.statistics.get_stats()
        self.assertEqual(stats['success_rate'], 0)

    def test_get_stats_non_zero_total(self):
        self.statistics.success_count = 80
        self.statistics.total_count = 100
        stats = self.statistics.get_stats()
        self.assertEqual(stats['success_rate'], 0.8)

    def test_get_stats_success_greater_than_total(self):
        self.statistics.success_count = 120
        self.statistics.total_count = 100
        with self.assertRaises(ValueError):
            self.statistics.get_stats()
class TestStatisticsUpdate(unittest.TestCase):

    def setUp(self):
        self.statistics = Statistics()

    def test_update_success_true(self):
        # Test the update method with success=True
        self.statistics.update(success=True)
        self.assertEqual(self.statistics.total_count, 1)
        self.assertEqual(self.statistics.success_count, 1)

    def test_update_success_false(self):
        # Test the update method with success=False
        self.statistics.update(success=False)
        self.assertEqual(self.statistics.total_count, 1)
        self.assertEqual(self.statistics.success_count, 0)

def test_update_multiple_calls(self):
        # Test the update method with multiple calls
        self.statistics.update(success=True)
        self.statistics.update(success=False)
        self.statistics.update(success=True)
        self.statistics.update(success=False)
        self.statistics.update(success=True)
        self.assertEqual(self.statistics.total_count, 5)
        self.assertEqual(self.statistics.success_count, 3)

if __name__ == '__main__':
    unittest.main()
