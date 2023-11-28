import sqlite3

class Database:
    def __init__(self):
        conn = sqlite3.connect('ultra_type.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS stats
            (word text, char text, user_input text, time real)''')
        conn.commit()
        conn.close()
        pass

    def save_stats(self, stats):
        conn = sqlite3.connect('ultra_type.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS stats
            (word text, char text, user_input text, time real)''')
        for record in stats:
            c.execute("INSERT INTO stats VALUES (:word, :char, :user_input, :time)", record)
        conn.commit()
        conn.close()

    def load_stats(self):
        conn = sqlite3.connect('ultra_type.db')
        c = conn.cursor()
        c.execute("SELECT * FROM stats")
        stats = c.fetchall()
        conn.close()
        return stats