class Statistics:
    def __init__(self, stats):
        self.stats = stats

    def update(self, record):
        self.stats.append(record)

    def get_stats(self):
        return self.stats
