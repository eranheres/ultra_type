class Statistics:
    def __init__(self):
        self.success_count = 0
        self.total_count = 0

    def update(self, success: bool):
        self.total_count += 1
        if success:
            self.success_count += 1

    def get_stats(self):
        return {
            'success_rate': self.success_count / self.total_count if self.total_count > 0 else 0
        }
