import unittest

from ultra_type.statistics import Statistics


class TestStatisticsUpdate(unittest.TestCase):

    def setUp(self):
        self.statistics = Statistics([])

    def test_update_record(self):
        # Test the update method with success = True
        self.statistics.update({'val': 'hello'})
        self.assertEqual(len(self.statistics.get_stats()), 1)



if __name__ == '__main__':
    unittest.main()
