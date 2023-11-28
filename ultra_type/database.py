import sqlite3

class Database:
    def __init__(self, db_name='ultra_type.db'):
        self.db_name = db_name
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS stats
            (word text, char text, user_input text, time real)''')
        conn.commit()
        conn.close()
        pass

    def save_stats(self, stats):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS stats
            (word text, char text, user_input text, time real)''')
        for record in stats:
            c.execute("INSERT INTO stats VALUES (:word, :char, :user_input, :time)", record)
        conn.commit()
        conn.close()

    def load_stats(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM stats")
        stats = c.fetchall()
        conn.close()
        return [{
            "word": stat[0],
            "char": stat[1],
            "user_input": stat[2],
            "time": stat[3],
        } for stat in stats]