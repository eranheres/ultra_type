import sqlite3
import json

class Database:
    def __init__(self, db_name, stats_fields):
        self.db_name = db_name
        self._fields = stats_fields
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute(f'CREATE TABLE IF NOT EXISTS stats ({self._field_stracture_to_field_names()})')
        conn.commit()
        conn.close()
        pass

    def _field_stracture_to_field_names(self):
        # return the following string 'input_time datetime, word text, char text, user_input text, speed real'
        return ', '.join([f'{field_name} {field_type}' for field_name, field_type in self._fields.items()])

    def _field_stracture_to_field_types(self):
        # return the following string ':input :text, char text, user_input text, speed real'
        return ': '.join([f'{field_name}' for field_name in self._fields.items()[0]])

    def _fields_to_db_record(self, field_stracture_dict):
        # returns the following tuple ('2021-01-01 00:00:00', 'hello', 'h', 'h', 0.1)
        return tuple([field_stracture_dict[field_name] for field_name in self._fields.keys()])

    def _db_recors_to_fields(self, field_stracture_tuple):
        # returns the following dict {'input_time': '2021-01-01 00:00:00', 'word': 'hello', 'char': 'h', 'user_input': 'h', 'time': 0.1}
        return {field_name: field_stracture_tuple[index] for index, field_name in enumerate(self._fields.keys())}

    def _validate_stats(self, statistics: []):
        for stat in statistics:
            for field_name, field_type in self._fields.items():
                if field_name not in stat:
                    raise Exception(f"field '{field_name}' is missing in stat")
            for field_name, field_type in stat.items():
                if field_name not in self._fields:
                    raise Exception(f"field '{field_name}' is not in the field structure")


    def clear_stats(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute(f'DROP TABLE IF EXISTS stats')
        conn.commit()
        conn.close()

    def save_stats(self, statistics: []):
        self.clear_stats()
        self._validate_stats(statistics)
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute(f'CREATE TABLE IF NOT EXISTS stats ({self._field_stracture_to_field_names()})')
        for stat in statistics:
            record = self._fields_to_db_record(stat)
            fields_names = ', '.join([f':{field_name}' for field_name in self._fields.keys()])
            c.execute(f"INSERT INTO stats VALUES ({fields_names})", record)
        conn.commit()
        conn.close()

    def load_stats(self, language: str):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM stats WHERE language = :language", {"language": language})
        stats = c.fetchall()
        conn.close()
        return [self._db_recors_to_fields(stat) for stat in stats]

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