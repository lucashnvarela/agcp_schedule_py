import re
from bs4 import BeautifulSoup as bs
from chromedriver import selenium
from database import *


def auto_select():
    driver = selenium()

    driver.select_campus("2")
    driver.select_course("4515")
    driver.select_year("1")
    driver.select_week("19-09-2022")

    return bs(driver.source(), "html.parser")


def scrape_schedule():
    schedule = {}

    html = auto_select()
    tr_id = {"id": "PlaceHolderMain_DayPilotCalendar1_events"}
    td_list = html.find("tr", tr_id).find_all("td")

    for td,	weekday_id in zip(td_list, range(1, len(WEEKDAYS))):
        schedule[weekday_id] = []

        if td.findChild().findChild() is not None:
            for div in td.findChild().find_all("div", recursive=False):
                div_title = div.find(
                    "div", {"title": True}, recursive=False)
                div_text = div_title.find(
                    "div", string=True, recursive=False).text

                name, type = re.search(r"(.+?)\s*\((.+?)\)", div_text).groups()
                teacher = re.search(r"-\s*(.+?)\s*-", div_text).group(1)
                if re.search(r"\.", teacher) is None:
                    teacher = "-"
                room = div_text.split(" - ")[-1]
                start_time, end_time = div_title["title"].split(" - ")[-2:]

                schedule[weekday_id].append((
                    name, type, teacher, room, start_time, end_time))

    return schedule


def main():
    schedule = scrape_schedule()

    database = sql()
    week_id = database.insert_week()

    for weekday_id in range(1, len(WEEKDAYS)):
        weekdayweek_id = database.get_weekdayweek(week_id, weekday_id)
        for klass in schedule[weekday_id]:
            database.insert_klass(weekdayweek_id, *klass)

    database.connect.close()


main()
