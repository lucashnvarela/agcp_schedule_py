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
            'CREATE TABLE IF NOT EXISTS weekday (' +
            'id INTEGER PRIMARY KEY AUTOINCREMENT, ' +
            'week_id INTEGER NOT NULL, ' +
            'name TEXT NOT NULL, ' +
            'day TEXT NULL, '

            'FOREIGN KEY(week_id) REFERENCES week(id))')

        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS klass (' +
            'id INTEGER PRIMARY KEY AUTOINCREMENT, ' +
            'weekday_id INTEGER NOT NULL, ' +
            'name TEXT NOT NULL, ' +
            'type TEXT NOT NULL, ' +
            'teacher TEXT NOT NULL, ' +
            'room TEXT NOT NULL, ' +
            'start_time TEXT NOT NULL, ' +
            'end_time TEXT NOT NULL, ' +

            'FOREIGN KEY(weekday_id) REFERENCES weekday(id))')

        self.connect.commit()

    def insert_week(self):
        self.cursor.execute(
            'INSERT INTO week (start_date, end_date) ' +
            'VALUES (?, ?)',
            (None, None))

        week_id = self.cursor.lastrowid

        for weekday in WEEKDAYS:
            self.insert_weekday(week_id, weekday, None)

        self.connect.commit()
        return week_id

    def insert_weekday(self, week_id, name, day):
        self.cursor.execute(
            'INSERT INTO weekday (week_id, name, day) ' +
            'VALUES (?, ?, ?)',
            (week_id, name, day))

        self.connect.commit()

    def insert_klass(self, weekday_id, name, type, teacher, room, start_time, end_time):
        self.cursor.execute(
            'INSERT INTO klass (weekday_id, name, type, teacher, room, start_time, end_time) ' +
            'VALUES (?, ?, ?, ?, ?, ?, ?)',
            (weekday_id, name, type, teacher, room, start_time, end_time))

        self.connect.commit()

    def get_weeks(self):
        self.cursor.execute('SELECT * FROM week')

        return self.cursor.fetchall()

    def get_weekdays(self, week_id):
        self.cursor.execute(
            'SELECT * FROM weekday ' +
            'WHERE week_id = ?',
            (week_id,))

        return self.cursor.fetchall()

    def get_klasses(self, weekday_id):
        self.cursor.execute(
            'SELECT * FROM klass ' +
            'WHERE weekday_id = ?',
            (weekday_id,))

        return self.cursor.fetchall()

    def show_database(self):
        for week in self.get_weeks():
            print("week: ", week)

            for weekday in self.get_weekdays(week[0]):
                print("weekday: ", weekday)

                for klass in self.get_klasses(weekday[0]):
                    print("klass: ", klass)

                print()

            print()
