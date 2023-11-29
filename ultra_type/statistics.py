class Statistics:
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
