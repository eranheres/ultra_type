import unittest

from ultra_type.statistics import Statistics


class TestStatisticsGetStats(unittest.TestCase):
    def setUp(self):
        self.statistics = Statistics()
        self.statistics.success_count = 10
        self.statistics.total_count = 20

    def test_get_stats_success_rate(self):
        expected_success_rate = (
            self.statistics.success_count / self.statistics.total_count
        )
        stats = self.statistics.get_stats()
        self.assertEqual(stats["success_rate"], expected_success_rate)

    def test_get_stats_success_rate_zero_total(self):
        self.statistics.total_count = 0
        stats = self.statistics.get_stats()
        self.assertEqual(stats["success_rate"], 0)


def test_get_stats_success_rate_zero_success(self):
    stats = self.statistics.get_stats()
    self.assertEqual(stats["success_rate"], 0)


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


def test_multiple_updates_success_true(self):
    # Test the update method with multiple updates where success = True
    num_updates = 5
    for _ in range(num_updates):
        self.statistics.update(success=True)
    self.assertEqual(self.statistics.total_count, num_updates)
    self.assertEqual(self.statistics.success_count, num_updates)


if __name__ == "__main__":
    unittest.main()

