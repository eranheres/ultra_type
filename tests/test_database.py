from ultra_type.database import Database
import time

class TestDatabase:

    # init the test
    def setup_method(self):
        self.fields = {
            "input_time": "datetime",
            "practice_name": "text",
            "practice_guid": "text",
            "word": "text",
            "char": "text",
            "user_input": "text",
            "time": "real",
        }

    def test_init(self):
        db_name = f'ultra_type_{int(time.time())}.db'
        db = Database(db_name, self.fields)
        assert db.db_name == db_name

    def test_save_stats(self):
        db_name = f'ultra_type_{int(time.time())}.db'
        db = Database(db_name, self.fields)
        stats = [
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
            {
                "input_time": "2021-01-01 00:00:04",
                "practice_name": "practice1",
                "practice_guid": "78",
                "word": "hello",
                "char": "o",
                "user_input": "o",
                "time": 0.5,
            },
        ]
        db.save_stats(stats)
        loaded_stats = db.load_stats()
        assert loaded_stats == stats

    def test_save_stats_missing_field(self):
        stats = [{
            "input_time": "2021-01-01 00:00:00",
            "practice_name": "practice1",
            "practice_guid": "1234",
            "char": "h",
            "user_input": "h",
            "time": 0.1,
            "invalid_field": "invalid"
        }]
        db_name = f'ultra_type_{int(time.time())}.db'
        db = Database(db_name, self.fields)
        try:
            db.save_stats(stats)
            assert False
        except Exception as e:
            assert str(e) == "field 'word' is missing in stat"

    def test_save_stats_unknown_field(self):
        stats = [{
            "input_time": "2021-01-01 00:00:00",
            "practice_name": "practice1",
            "practice_guid": "1234",
            "word": "hello",
            "work": "hello",
            "char": "h",
            "user_input": "h",
            "time": 0.1,
            "invalid_field": "invalid"
        }]
        db_name = f'ultra_type_{int(time.time())}.db'
        db = Database(db_name, self.fields)
        try:
            db.save_stats(stats)
            assert False
        except Exception as e:
            assert str(e) == "field 'work' is not in the field structure"

    def test_save_stats_valid(self):
        stats = [{
            "input_time": "2021-01-01 00:00:00",
            "practice_name": "practice1",
            "practice_guid": "1234",
            "word": "hello",
            "char": "h",
            "user_input": "h",
            "time": 0.1,
        }]
        db_name = f'ultra_type_{int(time.time())}.db'
        db = Database(db_name, self.fields)
        db.save_stats(stats)
