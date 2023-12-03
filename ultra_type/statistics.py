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

        # Rename columns for clarity
        word_stats.columns = ['word', 'average_wpm', 'avg_error_rate', 'count']
        sorted_word_stats = word_stats.sort_values(by=['avg_error_rate','average_wpm'], ascending=[False,True])
        return sorted_word_stats.to_dict('records')

    def letters_data(self):
        # Convert the list of dictionaries into a pandas DataFrame
        df = pd.DataFrame(self.stats)
        if df.empty:
            return {"records": []}

        # Convert 'input_time' to datetime and 'time' to minutes
        df['input_time'] = pd.to_datetime(df['input_time'])

        # Calculate WPM for each entry (assuming 5 characters per word)
        df['wpm'] = 1 / (df['time'] * 5) / 60

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
        word_stats.columns = ['char', 'average_wpm', 'avg_error_rate', 'count']
        sorted_word_stats = word_stats.sort_values(by=['avg_error_rate','average_wpm'], ascending=[False,True])
        return sorted_word_stats.to_dict('records')

    def prtactices_data(self):
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

        print(practice_times)

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

        return result[['practice_guid', 'start_time', 'char_count', 'wpm', 'accuracy']].to_dict('records')