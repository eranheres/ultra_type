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
        "input_time": "2021-01-01 00:01:00",
        "practice_name": "practice1",
        "practice_guid": "1234",
        "word": "hello",
        "char": "e",
        "user_input": "r",
        "time": 0.2,
    },
    {
        "input_time": "2021-01-01 00:11:00",
        "practice_name": "practice1",
        "practice_guid": "5678",
        "word": "hello",
        "char": "l",
        "user_input": "l",
        "time": 0.3,
    },
    {
        "input_time": "2021-01-01 00:00:02",
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
df['time'] = df['time']   # Convert microseconds to seconds

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


print(char_counts)
result = pd.merge(practice_times, char_counts, on='practice_guid')
print(result)

result['wpm'] = result['char_count'] / (result['duration'] * 5)  # Assuming 5 characters per word
result['accuracy'] = result['correct_chars'] / result['char_count'] * 100

#print(result[['practice_guid', 'start_time', 'char_count', 'wpm', 'accuracy']])

# nicely print the dataframe
print(result.to_string(index=False))

