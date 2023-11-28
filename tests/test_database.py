from ultra_type.database import Database
import time

class TestDatabase:
    def test_init(self):
        db_name = f'ultra_type_{int(time.time())}.db'
        db = Database(db_name)
        assert db.db_name == db_name

    def test_save_stats(self):
        db_name = f'ultra_type_{int(time.time())}.db'
        db = Database(db_name)
        stats = [
            {
                "input_time": "2021-01-01 00:00:00",
                "word": "hello",
                "char": "h",
                "user_input": "h",
                "time": 0.1,
            },
            {
                "input_time": "2021-01-01 00:00:01",
                "word": "hello",
                "char": "e",
                "user_input": "e",
                "time": 0.2,
            },
            {
                "input_time": "2021-01-01 00:00:02",
                "word": "hello",
                "char": "l",
                "user_input": "l",
                "time": 0.3,
            },
            {
                "input_time": "2021-01-01 00:00:03",
                "word": "hello",
                "char": "l",
                "user_input": "l",
                "time": 0.4,
            },
            {
                "input_time": "2021-01-01 00:00:04",
                "word": "hello",
                "char": "o",
                "user_input": "o",
                "time": 0.5,
            },
        ]
        db.save_stats(stats)
        loaded_stats = db.load_stats()
        assert loaded_stats == stats
