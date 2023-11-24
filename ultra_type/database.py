import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('typing_practice.db')

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY,
                language TEXT,
                speed REAL,
                success_rate REAL
            )
        """)
        self.conn.commit()

    def insert_data(self, language: str, speed: float, success_rate: float):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO stats (language, speed, success_rate)
            VALUES (?, ?, ?)
        """, (language, speed, success_rate))
        self.conn.commit()

    def get_data(self, language: str):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM stats
            WHERE language = ?
        """, (language,))
        return cursor.fetchall()
