import re
from collections import defaultdict

import requests
from bs4 import BeautifulSoup as bs
from rich.console import Console

from utils.AGCPLibrary import AGCPLibrary
from utils.DropdownHandler import DropdownHandler


class Scraper:
    def __init__(self):
        self.console = Console()

        self.webpage = "https://publico.agcp.ipleiria.pt/paginas/ScheduleRptCursosSemanalPublico.aspx"

        self.schedule_id = "PlaceHolderMain_DayPilotCalendar1_events"
        self.weekday_dates_id = "PlaceHolderMain_DayPilotCalendar1_header"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def fetch_course_schedule(self, choices: dict):
        self.console.log("Running DropdownHandler")

        with DropdownHandler(webpage=self.webpage) as dropdown_handler:
            for name, value in choices.items():
                dropdown_handler.select_dropdown_value(name=name, value=value)

            self.console.log("Requesting html content")
            source_page = dropdown_handler.get_page_source()

        return bs(source_page, "html.parser")

    def scrape_course_schedule(self, html_content: bs):

        def parse_klass(html_content: bs):
            element_title = html_content.find(
                "div", {"title": True}, recursive=False)
            element_text = element_title.find(
                "div", string=True, recursive=False).text

            name, type = re.search(r"(.+?)\s*\((.+?)\)", element_text).groups()

            teacher = re.search(r"-\s*(.+?)\s*-", element_text).group(1)
            if re.search(r"\.", teacher) is None:
                teacher = "-"

            room = element_text.split(" - ")[-1]

            start_time, end_time = element_title["title"].split(" - ")[-2:]

            return (name, type, teacher, room, start_time, end_time)

        self.console.log("Scraping schedule")
        schedule = defaultdict(list)

        weekday_elements = html_content.find(
            "tr", {"id": self.schedule_id}).find_all("td")

        for weekday_id, td in enumerate(iterable=weekday_elements, start=1):
            if td.findChild().findChild() is not None:
                for div in td.findChild().find_all("div", recursive=False):
                    schedule[weekday_id].append(parse_klass(html_content=div))

        weekday_dates = html_content.find(
            "table", {"id": self.weekday_dates_id}).find_all("td")

        start_date = weekday_dates[0].text
        end_date = weekday_dates[-1].text

        return start_date, end_date, schedule
