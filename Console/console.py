""""
This file define a class that is used as standard IO for the whole project
"""

from rich.console import Console
from rich.prompt import Prompt


class ConsolePrinter:
    def __init__(self):
        self.__Console__ = Console()

    def print(self):
        with self.__Console__.capture() as capture:
            self.__Console__.print("[bold magenta]Hello World[/]")

        print(capture.get())

    def Ask(self):
        self.__Console__.print("1 : Import from a CSV file")
        self.__Console__.print("2 : Import from Excel file")
        self.__Console__.print("3 : Type references by your own")
        PPrompt = Prompt.ask(
            prompt="Choose what to do : ",
            console=None,
            choices=["1", "2", "3"],
            show_default=False,
        )
        return PPrompt


if __name__ == "__main__":
    ConsoleP = ConsolePrinter()
    ConsoleP.print()
    ret = ConsoleP.Ask()
    print(ret)
