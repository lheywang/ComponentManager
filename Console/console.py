""""
This file define a class that is used as standard IO for the whole project
"""

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table


class ConsolePrinter:
    def __init__(self):
        """
        Init and clear the console for future usage.
        """
        self.__Console__ = Console()
        self.clear()

    def Ask(self, PresentationString, Choices: list[str]):
        """
        Enable the ability to manage a prompt for a choice.

        Arguments :
            PresentationString : Text that will be printed in top of the choices
            Choices : A list of string that may be choosen

        Returns :
            Result : A string with the ID of the choice.
        """
        self.__Console__.print(f"[bold yellow]{PresentationString}[/]")
        ChoiceList = []

        for index, choice in enumerate(Choices):
            self.__Console__.print(f"[bold orange]{index + 1} : [/]{choice}")
            ChoiceList.append(f"{index + 1}")

        Result = Prompt.ask(
            console=None,
            choices=ChoiceList,
            show_default=False,
        )
        return Choices[ChoiceList.index(Result)]
    
    def Confirm(self, Message):
        """
        This function ask for a Y/N question :
        """
        return Confirm.ask(Message)
    
    def TextInput(self, Message):
        """
        This function input a standard string
        """
        return Prompt.ask(Message)

    def log(self, Message, istyle:str = "blue"):
        self.__Console__.log(Message, style=istyle)
        return

    def HeadMessage(self, Message: str):
        """
        Print a message accentuated by lines and stars.

        Arguments : 
            Message : The text to print. Will be splitted in half if the lengh > 100 or when a !,? char is found.

        Returns :
            None
        """
        splitted = Message.replace("?", "?=")
        splitted = splitted.replace("!", "!=")
        splitted = splitted.replace(".", ".=")
        splitted = splitted.replace("\n", "=")
        splitted = splitted.split("=")

        size = []
        out = []
        for index, split in enumerate(splitted):
            slen = len(splitted[index])
            if slen != 0 :
                if slen > 100:
                    mid = split.find(" ", int(slen / 2))
                    out.append(split[:mid].strip())
                    size.append(len(split[:mid].strip()))
                    out.append(split[mid:].strip())
                    size.append(len(split[mid:].strip()))
                else:
                    out.append(split.strip())
                    size.append(slen)

        self.__Console__.print(
            f"[bold white]{"_" * 100}[/]"
        )
        for s_out in out:
            next = "{:<96}".format(s_out)
            self.__Console__.print(
                f"[bold white]* {next} *[/]"
            )
        self.__Console__.print(
            f"[bold white]{"_" * 100}[/]"
        )

    def clear(self):
        """
        Clear the console
        """
        self.__Console__.clear()
        return
    
    def PrintElements(self, TableTitle,List):
        """
        This function print into a table the output of the DB.seek, or more generally a tuple of values.
        The parameters are printed in this order : 
        1) ID in the database
        2) Family
        3) Partname
        4) Package
        5) value
        6) Quantity stored
        7) Type
        8) Manufacturer
        9) Datasheet
        10) Seller

        Arguments : 
            TableTitle : The tile given to this output
            List : A tuple or a list of tuples.

        Returns :
            None
        """
        if type(List) is not list : List = [List] # If a single tuple is passed, then convert it to a list.

        # Create the Table
        table = Table(title=TableTitle)

        # Add the differents columns
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Family", justify="right", style="white", no_wrap=True)
        table.add_column("Partname", justify="right", style="white", no_wrap=True)
        table.add_column("Package", justify="right", style="white", no_wrap=True)
        table.add_column("Value", justify="right", style="white", no_wrap=True)
        table.add_column("Quantity", justify="right", style="yellow", no_wrap=True)
        table.add_column("Type", justify="right", style="white", no_wrap=True)
        table.add_column("Manufacturer", justify="right", style="blue underline", no_wrap=True)
        table.add_column("Datasheet", justify="right", style="blue underline", no_wrap=True)
        table.add_column("Seller", justify="right", style="blue underline", no_wrap=True)
        
        # To make the presentation cleaner, the DB order and print order are different.
        # This list make easier the code.
        ElementOrder = [0, 1, 2, 3, 5, 6, 4, 7, 8, 9]         
        
        for Element in List:
            elements = []
            for Index in ElementOrder:
                elements.append(str(Element[Index]))

            table.add_row(*elements)

        self.__Console__.print(table)
        return
