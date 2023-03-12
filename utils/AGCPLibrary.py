import json


class AGCPLibrary:
    """
    A class to manage the AGCP Library selection list.
    """

    def __init__(self):
        """
        Constructor to initialise the class.
        Reads in the AGCP Library selection list from a JSON file.
        """

        self.file_name = "agcp_library.json"
        self.selection_list = dict()

        try:
            with open(self.file_name, "r") as file:
                self.selection_list = json.load(file)

        except FileNotFoundError:
            with open(self.file_name, "w+") as file:
                json.dump(self.selection_list, file)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def get_key(self, selection_list: dict, choice: str):
        """
        Returns the key of the given choice in the given selection list, if it exists.

        :param selection_list: The selection list to search.
        :param choice: The choice to search for.
        :return: The key of the choice, if it exists.
        """

        for key, option in selection_list.items():
            if choice.casefold() == option.casefold():
                return key

        return None

    def update_list(self, name: str, new_list: dict):
        """
        Updates the selection list with a given name with a new list.

        :param name: The name of the selection list to update.
        :param new_list: The new list to update the old one with.
        """

        for key, option in new_list.items():
            if key not in self.selection_list[name]:
                self.selection_list[name].update({key: option})

        self.update_file()

    def update_file(self):
        """
        Writes the current selection list to a JSON file.
        """

        with open(self.file_name, "w") as file:
            json.dump(self.selection_list, file)
