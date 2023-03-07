import re
from bs4 import BeautifulSoup as bs
from webdriver import selenium


class Weekday:
    def __init__(self, name):
        self.name = name
        self.classes = []

    def show(self):
        print(self.name)
        for klass in self.classes:
            klass.show()


class Klass:
    def __init__(self, string):
        self.name, self.type = re.search("(.+?)\s*\((.+?)\)", string).groups()
        self.teacher = re.search("-\s*(.+?)\s*-", string).group(1)
        self.room = re.search("-\s*(.+?)\s*-\s*(.+?)\s*-", string).group(2)
        self.start_time, self.end_time = re.search(
            "-\s*(\d{2}:\d{2})", string).groups()

    def show(self):
        print(self.name, self.type, self.teacher,
              self.room, self.start_time, self.end_time)


URL = "https://publico.agcp.ipleiria.pt/paginas/ScheduleRptCursosSemanalPublico.aspx"

CAMPUS_DROPDOWN = "ctl00$PlaceHolderAGCPUO$ddlUO"
COURSE_DROPDOWN = "ctl00$PlaceHolderMain$ddlCursos"
YEAR_DROPDOWN = "ctl00$PlaceHolderMain$ddlAnosCurr"
WEEK_DROPDOWN = "ctl00$PlaceHolderMain$ddlSemanas"

TABLE_EVENTS = "PlaceHolderMain_DayPilotCalendar1_events"

selenium = selenium()
selenium.get(URL)

selenium.select(CAMPUS_DROPDOWN, "2")
selenium.select(COURSE_DROPDOWN, "4515")
selenium.select(YEAR_DROPDOWN, "1")

html = selenium.source()
soup = bs(html, "html.parser")

weekdays = ["Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado"]
week = [Weekday(name) for name in weekdays]

for td, weekday in zip(soup.find("tr", {"id": TABLE_EVENTS}).find_all("td"), weekdays):
    if td.findChild().findChild() is not None:
        for div in td.findChild().find_all("div", recursive=False):
            div_title = div.find(
                "div", {"title": True}, recursive=False)
            div_text = div_title.find(
                "div", string=True, recursive=False).text

            #klass = Klass(s)
            # week[weekdays.index(weekday)].classes.append(klass)


for weekday in week:
    weekday.show()
