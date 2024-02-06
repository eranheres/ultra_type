import pandas as pd

class Statistics:
    FIELD_STRACTURE = {
        "input_time": "datetime",
        "practice_name": "text",
        "practice_guid": "text",
        "language": "text",
        "word": "text",
        "char": "text",
        "user_input": "text",
        "time": "real",
    }

    def __init__(self, stats):
        self.stats = stats

    def update(self, record):
        self.stats.append(record)

    def get_stats(self):
        return self.stats

    def word_data(self):
        if len(self.stats) == 0:
            return []
        # Convert the list of dictionaries into a pandas DataFrame
        df_errors = pd.DataFrame(self.stats)
        df_errors['errors'] = df_errors.apply(lambda x: sum(a != b for a, b in zip(x['user_input'], x['char'])), axis=1)
        df_errors = df_errors.groupby('word').agg({
            'word': 'count',
            'errors': 'sum'
        }).rename(columns={'word': 'count'}).reset_index()
        df_errors['avg_error_rate'] = df_errors['errors'] / df_errors['count']

        df_wpm = pd.DataFrame(self.stats)
        df_wpm['wpm'] = 1 / ((df_wpm['time']/60) * 5)
        df_wpm = df_wpm.groupby('word').agg({
            'wpm': 'mean',
        }).rename(columns={'word': 'count'}).reset_index()

        df = pd.merge(df_errors, df_wpm, on='word')
        df.columns = ['word', 'count', 'error_count', 'error_rate', 'wpm']
        sorted_word_stats = df.sort_values(by=['wpm', 'error_rate'], ascending=[True, False])

        return list(df.columns), sorted_word_stats.values.tolist()

    def word_data_old(self):
        if len(self.stats) == 0:
            return []
        # Convert the list of dictionaries into a pandas DataFrame
        df = pd.DataFrame(self.stats)

        # Convert 'input_time' to datetime and 'time' to minutes
        df['input_time'] = pd.to_datetime(df['input_time'])
        df['time'] = df['time'] / 60  # Convert seconds to minutes

        # Calculate WPM for each entry (assuming 5 characters per word)
        df['wpm'] = df['user_input'].apply(len) / (df['time'] * 5)

        # Calculate error rate for each entry
        df['errors'] = df.apply(lambda x: sum(a != b for a, b in zip(x['user_input'], x['char'])), axis=1)
        df['error_rate'] = df['errors'] / df['user_input'].apply(len)

        # Group by word and calculate average WPM, error rate, and count
        word_stats = df.groupby('word').agg({
            'wpm': 'mean',
            'error_rate': 'mean',
            'word': 'count'
        }).rename(columns={'word': 'count'}).reset_index()
        word_stats['count'] = word_stats['count'] / word_stats['word'].apply(len)
        # Rename columns for clarity
        word_stats.columns = ['word', 'average_wpm', 'avg_error_rate', 'count']
        sorted_word_stats = word_stats.sort_values(by=['avg_error_rate','average_wpm'], ascending=[False,True])
        return sorted_word_stats.to_dict('records')

    def letters_data(self):
        if len(self.stats) == 0:
            return []
        # Convert the list of dictionaries into a pandas DataFrame
        df = pd.DataFrame(self.stats)
        if df.empty:
            return {"records": []}

        # Convert 'input_time' to datetime and 'time' to minutes
        df['input_time'] = pd.to_datetime(df['input_time'])

        # Calculate WPM for each entry (assuming 5 characters per word)
        df['wpm'] = 1 / ((df['time'] / 60) * 5)

        # Calculate error rate for each entry
        df['errors'] = df.apply(lambda x: sum(a != b for a, b in zip(x['user_input'], x['char'])), axis=1)
        df['error_rate'] = df['errors'] / df['user_input'].apply(len)

        # Group by word and calculate average WPM, error rate, and count
        word_stats = df.groupby('char').agg({
            'wpm': 'mean',
            'error_rate': 'mean',
            'char': 'count'
        }).rename(columns={'char': 'count'}).reset_index()

        # Rename columns for clarity
        word_stats.columns = ['char', 'wpm', 'error_rate', 'count']
        sorted_word_stats = word_stats.sort_values(by=['error_rate','wpm'], ascending=[False,True])
        return word_stats.columns, sorted_word_stats.values.tolist()

    def practices_data(self):
        if len(self.stats) == 0:
            return {"records": []}
        df = pd.DataFrame(self.stats)

        # Convert 'input_time' to datetime and 'time' to seconds
        df['input_time'] = pd.to_datetime(df['input_time'])
        df['time'] = df['time'] / 60 # Convert microseconds to seconds

        # Calculate the duration and start time for each practice
        practice_times = df.groupby('practice_guid').agg({
            'input_time': ['min', 'max']
        }).reset_index()
        practice_times.columns = ['practice_guid', 'start_time', 'end_time']
        practice_times['duration'] = (practice_times['end_time'] - practice_times[
            'start_time']).dt.total_seconds() / 60  # Duration in minutes

        # Calculate character count and accuracy for each practice
        df['char_count'] = df['user_input'].apply(len)
        df['correct_chars'] = df.apply(lambda x: sum(a == b for a, b in zip(x['user_input'], x['char'])), axis=1)
        char_counts = df.groupby('practice_guid').agg({
            'char_count': 'sum',
            'correct_chars': 'sum'
        }).reset_index()

        result = pd.merge(practice_times, char_counts, on='practice_guid')
        result['wpm'] = result['char_count'] / (result['duration'] * 5)  # Assuming 5 characters per word
        result['accuracy'] = result['correct_chars'] / result['char_count'] * 100

        columns = ['start_time', 'char_count', 'wpm', 'accuracy']
        return columns,result[columns].sort_values(by='start_time', ascending=False).values.tolist()

    def daily_data(self):
        if len(self.stats) == 0:
            return {"records": []}
        df = pd.DataFrame(self.stats)

        df['date'] = df['input_time'].apply(lambda x: x[0:10])
        df = df.groupby('date').agg({'time': sum})
        df['time'] = df['time'] / 60
        return ['date','time'], df.sort_values(by='date', ascending=False).values.tolist()