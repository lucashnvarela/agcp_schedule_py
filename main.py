from utils.Database import Database
from utils.UserInterface import UserInterface
from utils.Scraper import Scraper


def main():
    with UserInterface() as interface:

        with Scraper() as scraper:
            user_choices = interface.prompt_user_info(bypass=True)

            html_content = scraper.fetch_course_schedule(
                choices=user_choices)

            start_date, end_date, schedule = scraper.scrape_course_schedule(
                html_content=html_content)

            with Database() as database:
                database.insert_schedule(
                    start_date=start_date, end_date=end_date, schedule=schedule)
                scraper.console.log(
                    "[green]Schedule data has been saved[/]\n")


if __name__ == "__main__":
    main()
