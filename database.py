import sqlite3


WEEKDAYS = ["Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado"]


class sql:
    def __init__(self):
        self.connect = sqlite3.connect('database.sqlite')
        self.cursor = self.connect.cursor()

        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS week (' +
            'id INTEGER PRIMARY KEY AUTOINCREMENT, ' +
            'start_date TEXT NULL, ' +
            'end_date TEXT NULL)')

        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS weekday_week (' +
            'id INTEGER PRIMARY KEY AUTOINCREMENT, ' +
            'weekday_id INTEGER NOT NULL, ' +
            'week_id INTEGER NOT NULL, ' +

            'FOREIGN KEY(weekday_id) REFERENCES weekday(id), ' +
            'FOREIGN KEY(week_id) REFERENCES week(id))')

        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS weekday (' +
            'id INTEGER PRIMARY KEY AUTOINCREMENT, ' +
            'name TEXT NOT NULL)')

        self.cursor.executemany(
            'INSERT INTO weekday (name) ' +
            'VALUES (?)',
            [(weekday_name,) for weekday_name in WEEKDAYS])

        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS klass (' +
            'id INTEGER PRIMARY KEY AUTOINCREMENT, ' +
            'weekdayweek_id INTEGER NOT NULL, ' +
            'name TEXT NOT NULL, ' +
            'type TEXT NOT NULL, ' +
            'teacher TEXT NOT NULL, ' +
            'room TEXT NOT NULL, ' +
            'start_time TEXT NOT NULL, ' +
            'end_time TEXT NOT NULL, ' +

            'FOREIGN KEY(weekdayweek_id) REFERENCES weekday_week(id))')

        self.connect.commit()

    def insert_week(self):
        self.cursor.execute(
            'INSERT INTO week (start_date, end_date) ' +
            'VALUES (?, ?)',
            (None, None))

        week_id = self.cursor.lastrowid

        self.cursor.executemany(
            'INSERT INTO weekday_week (weekday_id, week_id) ' +
            'VALUES (?, ?)',
            [(weekday_id, week_id) for weekday_id in range(1, len(WEEKDAYS))])

        self.connect.commit()
        return week_id

    def insert_klass(self, weekdayweek_id, name, type, teacher, room, start_time, end_time):
        self.cursor.execute(
            'INSERT INTO klass (weekdayweek_id, name, type, teacher, room, start_time, end_time) ' +
            'VALUES (?, ?, ?, ?, ?, ?, ?)',
            (weekdayweek_id, name, type, teacher, room, start_time, end_time))

        self.connect.commit()

    def get_weeks(self):
        self.cursor.execute('SELECT * FROM week')

        return self.cursor.fetchall()

    def get_weekdayweek(self, week_id, weekday_id):
        self.cursor.execute(
            'SELECT * FROM weekday_week ' +
            'WHERE week_id = ? AND weekday_id = ?',
            (week_id, weekday_id))

        weekdayweek_id = self.cursor.fetchone()[0]

        return weekdayweek_id
