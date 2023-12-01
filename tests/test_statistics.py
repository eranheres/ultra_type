import unittest

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
                "word": "hello",
                "char": "l",
                "user_input": "l",
                "time": 0.3,
            },
            {
                "input_time": "2021-01-01 00:00:03",
                "practice_name": "pice1",
                "practice_guid": "5678",
                "word": "hello",
                "char": "l",
                "user_input": "l",
                "time": 0.4,
            },
        ]
        import pandas as pd
        df = pd.DataFrame(data)

        # Convert 'input_time' to datetime and 'time' to seconds
        df['input_time'] = pd.to_datetime(df['input_time'])
        df['time'] = df['time'] / 1e6  # Convert microseconds to seconds
        #print(df)
        # Calculate character count and accuracy for each practice
        df['char_count'] = df['user_input'].apply(len)
        df['correct_chars'] = df.apply(lambda x: sum(a == b for a, b in zip(x['user_input'], x['char'])), axis=1)
        char_counts = df.groupby('practice_guid').agg({
            'char_count': 'sum',
            'correct_chars': 'sum'
        }).reset_index()

        #print(char_counts)
        import pandas

        pass

if __name__ == '__main__':
    unittest.main()
