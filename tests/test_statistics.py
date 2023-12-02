import unittest
import pandas as pd

from ultra_type.statistics import Statistics


class TestStatisticsUpdate(unittest.TestCase):

    def setUp(self):
        self.statistics = Statistics([])

    def test_update_record(self):
        # Test the update method with success = True
        self.statistics.update({'val': 'hello'})
        self.assertEqual(len(self.statistics.get_stats()), 1)


class TestStatisticsGetPracticesStats():
    def setUp(self):
        pass

    def test_get_practices_stats(self):
        data = [
            {
                "input_time": "2021-01-01 00:00:00",
                "practice_name": "practice1",
                "practice_guid": "1234",
                "word": "hello",
                "char": "h",
                "user_input": "h",
                "time": 0.1,
            },
            {
                "input_time": "2021-01-01 00:00:01",
                "practice_name": "practice2",
                "practice_guid": "1234",
                "word": "hello",
                "char": "e",
                "user_input": "e",
                "time": 0.2,
            },
            {
                "input_time": "2021-01-01 00:00:02",
                "practice_name": "practice1",
                "practice_guid": "5678",
                "word": "hello2",
                "char": "l",
                "user_input": "l",
                "time": 0.3,
            },
            {
                "input_time": "2021-01-01 00:00:03",
                "practice_name": "pice1",
                "practice_guid": "5678",
                "word": "hello2",
                "char": "l",
                "user_input": "l",
                "time": 0.4,
            },
        ]
        statistics = Statistics(data)
        practice_stats = statistics.process_word_data()

        df = pd.DataFrame(practice_stats)
        tbl = df.to_string(index=False)
        print(tbl)

if __name__ == '__main__':
    unittest.main()
