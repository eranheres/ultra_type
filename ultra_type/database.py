import sqlite3
import json

class Database:
    FIELD_STRACTURE = {
        "input_time": "datetime",
        "language": "text",
        "word": "text",
        "char": "text",
        "user_input": "text",
        "time": "real",
    }
    def __init__(self, db_name='ultra_type.db'):
        self.db_name = db_name
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute(f'CREATE TABLE IF NOT EXISTS stats ({self._field_stracture_to_field_names()})')
        conn.commit()
        conn.close()
        pass

    def _field_stracture_to_field_names(self):
        # return the following string 'input_time datetime, word text, char text, user_input text, speed real'
        return ', '.join([f'{field_name} {field_type}' for field_name, field_type in self.FIELD_STRACTURE.items()])

    def _field_stracture_dict_to_tuple(self, field_stracture_dict):
        # returns the following tuple ('2021-01-01 00:00:00', 'hello', 'h', 'h', 0.1)
        return tuple([field_stracture_dict[field_name] for field_name in self.FIELD_STRACTURE.keys()])

    def _field_stracture_tuple_to_dict(self, field_stracture_tuple):
        # returns the following dict {'input_time': '2021-01-01 00:00:00', 'word': 'hello', 'char': 'h', 'user_input': 'h', 'time': 0.1}
        return {field_name: field_stracture_tuple[index] for index, field_name in enumerate(self.FIELD_STRACTURE.keys())}

    def save_stats(self, stats):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute(f'CREATE TABLE IF NOT EXISTS stats ({self._field_stracture_to_field_names()})')
        for stat in stats:
            record = self._field_stracture_dict_to_tuple(stat)
            c.execute("INSERT INTO stats VALUES (:datetime, :word, :char, :user_input, :time)", record)
        conn.commit()
        conn.close()

    def load_stats(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM stats")
        stats = c.fetchall()
        conn.close()
        return [self._field_stracture_tuple_to_dict(stat) for stat in stats]

    def save_settings(self, settings):
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    def load_settings(self, default_settings):
        try:
            with open('settings.json') as f:
                settings = json.load(f)
        except:
            settings = default_settings
        return settings