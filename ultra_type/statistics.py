class Statistics:
    def __init__(self, stats):
        self.success_count = 0
        self.total_count = 0
        self.stats = stats

    def update(self, record):
        self.stats.append(record)

    def get_stats(self):
        return self.stats
