import sqlite3


class Database:
    def __init__(self):
        self.weekdays = [
            "Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado"]

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
            [(weekday_name,) for weekday_name in self.weekdays])

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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_traceback):
        self.connect.close()

    def get_weekdayweek(self, week_id: str, weekday_id: str):
        self.cursor.execute(
            'SELECT * FROM weekday_week ' +
            'WHERE week_id = ? AND weekday_id = ?',
            (week_id, weekday_id))

        weekdayweek_id = self.cursor.fetchone()[0]

        return weekdayweek_id

    def insert_week(self, start_date: str, end_date: str):
        self.cursor.execute(
            'INSERT INTO week (start_date, end_date) ' +
            'VALUES (?, ?)',
            (start_date, end_date))

        week_id = self.cursor.lastrowid

        self.cursor.executemany(
            'INSERT INTO weekday_week (weekday_id, week_id) ' +
            'VALUES (?, ?)',
            [(weekday_id, week_id) for weekday_id in range(1, len(self.weekdays))])

        self.connect.commit()
        return week_id

    def insert_klass(self, weekdayweek_id: str, klass: tuple):
        self.cursor.execute(
            'INSERT INTO klass (weekdayweek_id, name, type, teacher, room, start_time, end_time) ' +
            'VALUES (?, ?, ?, ?, ?, ?, ?)',
            (weekdayweek_id, *klass))

        self.connect.commit()

    def insert_schedule(self, start_date: str, end_date: str, schedule: dict):
        week_id = self.insert_week(start_date=start_date, end_date=end_date)

        for weekday_id in range(1, len(self.weekdays)):

            weekdayweek_id = self.get_weekdayweek(
                week_id=week_id, weekday_id=weekday_id)

            for klass in schedule[weekday_id]:
                self.insert_klass(weekdayweek_id=weekdayweek_id, klass=klass)
