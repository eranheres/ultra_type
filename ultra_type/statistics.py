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

    def get_word_times(self):
        word_times = {}
        for entry in self.stats:
            word = entry['word']
            time = entry['time']
            if word in word_times:
                word_times[word]['total'] += time
                word_times[word]['count'] += 1
            else:
                word_times[word] = {'total': time, 'count': 1}
        return word_times

    def get_char_times(self, language: str):
        char_times = {}
        for entry in self.stats:
            if entry['language'] != language:
                continue
            char = entry['char']
            time = entry['time']
            if char in char_times:
                char_times[char]['total'] += time
                char_times[char]['count'] += 1
            else:
                char_times[char] = {'total': time, 'count': 1}
        return char_times

    def get_prtactices_data(self):
        df = pd.DataFrame(self.stats)

        # Convert 'input_time' to datetime and 'time' to seconds
        df['input_time'] = pd.to_datetime(df['input_time'])
        df['time'] = df['time']  # Convert microseconds to seconds

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