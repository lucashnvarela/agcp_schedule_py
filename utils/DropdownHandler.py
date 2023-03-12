from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class DropdownHandler:
    """
    A class to handle the dropdowns in the AGCP webpage.
    """

    def __init__(self, webpage: str):
        """
        Constructor to initialise the class.
        Initialises the webdriver and loads the webpage.

        :param webpage: The url of the webpage to scrape data from.
        """

        self.dropdowns = {
            "campus": "ctl00$PlaceHolderAGCPUO$ddlUO",
            "semester": "PlaceHolderAGCPUO_ddlPeriodos",
            "course": "ctl00$PlaceHolderMain$ddlCursos",
            "year": "ctl00$PlaceHolderMain$ddlAnosCurr",
            "week": "ctl00$PlaceHolderMain$ddlSemanas"
        }

        self.webdriver_options = webdriver.ChromeOptions()
        """ run selenium in headless mode """
        self.webdriver_options.add_argument(argument="--headless")
        """ hide console logs """
        self.webdriver_options.add_experimental_option(
            name="excludeSwitches", value=["enable-logging"])
        self.webdriver = webdriver.Chrome(options=self.webdriver_options)

        self.webdriver.get(url=webpage)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.webdriver.quit()

    def get_page_source(self):
        """
        Returns the page source of the current webpage.
        """

        page_source = self.webdriver.page_source
        return page_source

    def select_dropdown_value(self, name: str, value: str):
        """
        Selects a value in a dropdown menu.

        :param name: The name of the dropdown menu to select a value from.
        :param value: The value to select in the dropdown menu.
        """

        select = Select(self.webdriver.find_element(
            by=By.NAME, value=self.dropdowns[name]))
        select.select_by_value(value=value)
