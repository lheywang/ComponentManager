"""
This is the entry point of the program.
"""

from Database import DataBase
from Console import ConsolePrinter
from FileInput import OpenFile


def main():
    Console = ConsolePrinter()
    Console.clear()
    DB = DataBase()

    Console.HeadMessage(
        """Welcome to Component Manager !"""
        """Here you can manage all of your stored electronics components."""
        """With this program, you will be able to :\n"""
        """- Manage your stocks\n"""
        """- Import orders from many sellers\n"""
        """- Import BOM to decreses the stocks\n"""
        """And so !"""
        """At any times, an exit menu will be available"""
    )

    Status = True
    while Status == True:
        RetVal_Action = Console.Ask(
            "Please choose what to do :",
            [
                "Add or Remove elements to the database",
                "Consult the database",
                "Exit the program",
            ],
        )

        if RetVal_Action == "Add or Remove elements to the database":
            pass
        elif RetVal_Action == "Consult the database":
            RetVal_Search = Console.Confirm(
                "Do you want to search for a specific reference ?"
            )
            if RetVal_Search:
                Search = True
                Arguments = dict()
                while True:
                    RetVal_Column = Console.Ask(
                        "Select settings you want to add. Any reselection will overhide the previous one.",
                        ["family", "partname", "package", "value", "manufacturer"],
                    )
                    RetVal_ColumnValue = Console.TextInput(
                        f"Enter the value for the field {RetVal_Column}"
                    )
                    Arguments[RetVal_Column] = RetVal_ColumnValue
                    RetVal_SearchStatus = Console.Confirm(
                        "Do you want to add another parameter ?"
                    )
                    if RetVal_SearchStatus == False:
                        break

                data = DB.SeekOnDB(**Arguments)
                Console.PrintElements(
                    "Here the components that match your request :", data
                )
            else:
                data = DB.SeekOnDB()
                Console.PrintElements("Here all of the components stored :", data)
        elif RetVal_Action == "Exit the program":
            Status = False
            continue


if __name__ == "__main__":
    # print(OpenFile("PCBA_3128D2_4.csv"))
    main()
