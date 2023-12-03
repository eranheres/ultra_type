import unittest
import pandas as pd
import json

from tabulate import tabulate
from ultra_type.statistics import Statistics



class TestStatisticsUpdate(unittest.TestCase):

    def setUp(self):
        self.statistics = Statistics([])

    def test_update_record(self):
        # Test the update method with success = True
        self.statistics.update({'val': 'hello'})
        self.assertEqual(len(self.statistics.get_stats()), 1)


class TestStatisticsGetPracticesStats(unittest.TestCase):
    def setUp(self):
        self.data = [
            {
                "input_time": "2021-01-01 00:00:00",
                "practice_name": "practice1",
                "practice_guid": "1234",
                "word": "hello",
                "char": "ר",
                "user_input": "ר",
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


    def test_get_practices_stats(self):
        statistics = Statistics(self.data)
        practice_stats = statistics.prtactices_data()

        df = pd.DataFrame(practice_stats)
        df.style.format({'avg_error_rate': '{:.2%}'})
        #df.style.set_properties({'text-align': 'left'})
        print("\n\n\n")
        print(df)

    def test_process_word_data(self):
        statistics = Statistics(self.data)
        practice_stats = statistics.word_data()

        df = pd.DataFrame(practice_stats)
        print("\n\n\n")
        txt = str(tabulate(df, headers=df.columns,tablefmt='github'))
        print(txt)

    def test_get_letters_stats(self):
        statistics = Statistics(self.data)
        practice_stats = statistics.letters_data()

        df = pd.DataFrame(practice_stats)
        txt = str(tabulate(df, headers=df.columns,tablefmt='github'))
        print("\n"+txt)

    def test_get_letters_hebrew(self):
        # load hebrew data
        with open('tests/hebrew_test_data.json') as f:
            data = json.load(f)

        statistics = Statistics(data)
        practice_stats = statistics.letters_data()

        df = pd.DataFrame(practice_stats)
        txt = str(tabulate(df, headers=df.columns,tablefmt='github'))
        print("\n"+txt)


if __name__ == '__main__':
    unittest.main()
