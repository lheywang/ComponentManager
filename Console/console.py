""""
This file define a class that is used as standard IO for the whole project
"""

from rich.console import Console
from rich.prompt import Prompt


class ConsolePrinter:
    def __init__(self):
        self.__Console__ = Console()

    def Ask(self, PresentationString, Choices: list[str]):
        self.__Console__.print(f"[bold yellow]{PresentationString}[/]")
        ChoiceList = []

        for index, choice in enumerate(Choices):
            self.__Console__.print(f"[bold orange]{index + 1} : [/]{choice}")
            ChoiceList.append(f"{index + 1}")

        PPrompt = Prompt.ask(
            console=None,
            choices=ChoiceList,
            show_default=False,
        )
        return PPrompt

    def log(self, Message):
        self.__Console__.log(Message)
        return
