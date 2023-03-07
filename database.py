import sqlite3


class Database:
    def __init__(self):
        self.connect = sqlite3.connect('database.db')
        self.cursor = self.connect.cursor()

        self.cursor.execute('CREATE TABLE IF NOT EXISTS weekday (' +
                            'id INTEGER PRIMARY KEY AUTOINCREMENT,' +
                            'name TEXT NOT NULL,' +
                            'day TEXT NOT NULL)')

        self.cursor.execute('CREATE TABLE IF NOT EXISTS klass (' +
                            'id INTEGER PRIMARY KEY AUTOINCREMENT,' +
                            'weekday_id INTEGER NOT NULL,' +
                            'name TEXT NOT NULL,' +
                            'type TEXT NOT NULL,' +
                            'teacher TEXT NOT NULL,' +
                            'room TEXT NOT NULL,' +
                            'start_time TEXT NOT NULL,' +
                            'end_time TEXT NOT NULL,' +

                            'FOREIGN KEY(weekday_id) REFERENCES weekday(id))')

        self.connect.commit()
