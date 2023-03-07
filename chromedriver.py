from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


URL = "https://publico.agcp.ipleiria.pt/paginas/ScheduleRptCursosSemanalPublico.aspx"

CAMPUS_DROPDOWN = "ctl00$PlaceHolderAGCPUO$ddlUO"
COURSE_DROPDOWN = "ctl00$PlaceHolderMain$ddlCursos"
YEAR_DROPDOWN = "ctl00$PlaceHolderMain$ddlAnosCurr"
WEEK_DROPDOWN = "ctl00$PlaceHolderMain$ddlSemanas"


class selenium:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # run selenium in headless mode
        self.options.add_argument("--headless")
        self.webdriver = webdriver.Chrome(options=self.options)

        self.webdriver.get(URL)

    def source(self):
        source = self.webdriver.page_source
        self.webdriver.quit()
        return source

    def select(self, name, value):
        select = Select(self.webdriver.find_element(By.NAME, name))
        select.select_by_value(value)

    def select_campus(self, value):
        self.select(CAMPUS_DROPDOWN, value)

    def select_course(self, value):
        self.select(COURSE_DROPDOWN, value)

    def select_year(self, value):
        self.select(YEAR_DROPDOWN, value)

    def select_week(self, value):
        self.select(WEEK_DROPDOWN, value)
