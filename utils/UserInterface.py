import time
import datetime

from rich.console import Console
from rich.prompt import Prompt

from utils.AGCPLibrary import AGCPLibrary


class UserInterface:
    def __init__(self):
        self.console = Console()

        self.question_title = "\n  [steel_blue]QUESTION[/]"

        self.default_choices = dict({
            "campus": "2",
            "course": "4515",
            "year": "1",
            "week": "19-09-2022"
        })

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def validate_prompt_confirm(self, value: str):
        if value.casefold() in ["y", "yes"]:
            return True

        elif value.casefold() in ["n", "no"]:
            return False

        else:
            return None

    def prompt_user_info(self, bypass: bool = False):
        self.console.clear()

        user_choices = dict()

        if bypass:
            self.console.log(
                "[dark_orange]Bypass enabled[/]: using default values")
            time.sleep(1)
            return self.default_choices

        def get_week_start(date: datetime.date):
            start_week = date - datetime.timedelta(days=date.weekday())
            return start_week.strftime('%d-%m-%Y')

        with AGCPLibrary() as agcp_library:

            """ Prompt the user to select a campus """
            while True:
                user_choices.update({"campus": agcp_library.get_key(
                    options=agcp_library.selection_list["campus"],
                    choice=Prompt.ask(
                        prompt=self.question_title + "\n  What campus are you in?"))
                })

                if user_choices["campus"] is not None:
                    break
                else:
                    self.console.clear()
                    self.console.log(
                        "[red]ERROR[/]: Invalid input or not yet implemented, please try again")

            self.console.clear()

            """ Prompt the user to select a course """
            while True:
                user_choices.update({"course": agcp_library.get_key(
                    options=agcp_library.selection_list["course"],
                    choice=Prompt.ask(
                        prompt=self.question_title + "\n  What course are you in?"))
                })

                if user_choices["course"] is not None:
                    break
                else:
                    self.console.clear()
                    self.console.log(
                        "[red]ERROR[/]: Invalid input or not yet implemented, please try again")

            self.console.clear()

            """ Prompt the user to enter their current year """
            while True:
                user_choices.update({"year": Prompt.ask(
                    prompt=self.question_title + "\n  What year are you in?")
                })

                if user_choices["year"] in agcp_library.selection_list["year"]:
                    break
                else:
                    self.console.clear()
                    self.console.log(
                        "[red]ERROR[/]: Invalid input, please try again")

            self.console.clear()

            if get_week_start(datetime.date.today()) in agcp_library.selection_list["week"]:

                """ Prompt the user to select whether to see the schedule for the current week """
                while True:
                    current_week_choice = Prompt.ask(
                        prompt=self.question_title +
                        "\n  Whould you like to see the schedule for the current week? [medium_orchid]\[y/n][/]")

                    current_week_choice = self.validate_prompt_confirm(
                        value=current_week_choice)

                    if current_week_choice is not None:
                        if current_week_choice:
                            user_choices.update(
                                {"week": get_week_start(datetime.date.today())})
                            break

                    else:
                        self.console.clear()
                        self.console.log(
                            "[red]ERROR[/]: Invalid input, please try again")

            self.console.clear()
            return user_choices
