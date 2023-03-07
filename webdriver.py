from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class selenium:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")
        self.webdriver = webdriver.Chrome(options=self.options)

    def get(self, url):
        self.webdriver.get(url)

    def source(self):
        source = self.webdriver.page_source
        self.webdriver.quit()
        return source

    def select(self, name, value):
        select = Select(self.webdriver.find_element(By.NAME, name))
        select.select_by_value(value)
