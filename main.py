"""
This is the entry point of the program.
"""

from Database import DataBase
from Console import ConsolePrinter
from FileInput import OpenFile, OrderKeys, PrepareData

from difflib import SequenceMatcher


def main():
    Console = ConsolePrinter()
    Console.clear()
    DB = DataBase()
    Console.log("Openned DB")

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
    # Exit the loop only if requested.
    # Every inputs are a blocking step.
    while Status == True:

        # First, ask what do we want : Add, Remove or See
        # Theses will be named in the comment as actions choices.
        RetVal_Action = Console.Ask(
            "Please choose what to do :",
            [
                "Add or Remove elements to the database",
                "Consult the database",
                "Exit the program",
            ],
        )

        # Then we handle all of the actions choices
        if RetVal_Action == "Add or Remove elements to the database":
            RetVal_AddOrRemove = Console.Ask(
                "What action do you want to do ?",
                [
                    "Add references / Increase stocks to the database",
                    "Remove elements / decrease stocks to the database",
                ],
            )
            RetVal_Mode = Console.Confirm(
                "Do you want to do it by hand ? If no, a tab file will be needed (CSV, XLSX...)"
            )

            # if file operation mode is choosen; ask for it
            if RetVal_Mode == False:
                RetVal_File = Console.TextInput(
                    "Pass a absolute path to the file that contain the references "
                )
                # Open the file and ask for the user to sort the differents columns found
                # This boring step is required to ensure compatibility with any file that may be exported by any software or seller.
                data = OpenFile(RetVal_File)
                ArgsOrder = OrderKeys(Console, data[0].keys())
                DataToExecute = PrepareData(Console, ArgsOrder, data)

            # Manual operation
            else:
                if (
                    RetVal_AddOrRemove
                    == "Add references / Increase stocks to the database"
                ):
                    Fields = [
                        "partname",
                        "quantity",
                        "package",
                        "type",
                        "value",
                        "family",
                        "manufacturer",
                        "datasheet",
                        "seller",
                    ]

                    DataToExecute = []
                    for Key in Fields:
                        RetVal_ManualAdd = Console.TextInput(
                            f"Enter the value for {Key}"
                        )
                        DataToExecute.append(RetVal_ManualAdd)
                    DataToExecute = [tuple(DataToExecute)]

                elif (
                    RetVal_AddOrRemove
                    == "Remove elements / decrease stocks to the database"
                ):
                    RetVal_DeleteAction = Console.Ask(
                        "What are you wanting to do ?",
                        [
                            "Delete a full row on the database ?",
                            "Decrese the stock of a reference ?",
                        ],
                    )
                    data = None
                    while True:
                        RetVal_ManualRemove = Console.TextInput(
                            f"Enter the id of the row which shall be edited"
                        )
                        data = DB.SeekOnDB(id=int(RetVal_ManualRemove))
                        Console.PrintElements(
                            "",
                            data,
                        )
                        if Console.Confirm("Did you want to edit this line ?") == True:
                            break

                    if RetVal_DeleteAction == "Delete a full row on the database ?":
                        if Console.Confirm("Are you sure ?") == True:
                            DB.DeleteFromDB(data[0][0])
                            RetVal_AddOrRemove = ""

                    elif RetVal_DeleteAction == "Decrese the stock of a reference ?":
                        RetVal_ManualRemove = Console.TextInput(
                            f"How many items shall be decreased "
                        )
                        ret = DB.UpdateQuantity(data[0][0], -int(RetVal_ManualRemove))
                        Console.log(f"There is now {ret} elements in stock.")
                        RetVal_AddOrRemove = ""

            # Add elements :
            if RetVal_AddOrRemove == "Add references / Increase stocks to the database":
                for Reference in DataToExecute:
                    RetVal_Add = DB.AddComponentToStock(*Reference)

                    if RetVal_Add == False:
                        Console.log(
                            f"{Reference[0]} already exists. Increased quantity."
                        )
            # Remove elements
            elif (
                RetVal_AddOrRemove
                == "Remove elements / decrease stocks to the database"
            ):
                for Reference in DataToExecute:
                    ret = DB.SeekOnDB(partname=Reference[0])
                    Row = ret[0][0]
                    DB.UpdateQuantity(Row, -Reference[0])

        # Or we handle the Consultation mode.
        elif RetVal_Action == "Consult the database":

            # Ask if we want to print the whole database or just a few parts (that will match a research patter)
            RetVal_Search = Console.Confirm(
                "Do you want to search for a specific reference ?"
            )

            # If a matching patter is required
            # We ask for elements, with the option to stop after each one.
            # Then we update ou dict, and pass it the the seek function.
            if RetVal_Search:
                Search = True
                Arguments = dict()
                while True:
                    # Parameters selection
                    RetVal_Column = Console.Ask(
                        "Select settings you want to add. Any reselection will overhide the previous one.",
                        [
                            "family",
                            "partname",
                            "package",
                            "value",
                            "manufacturer",
                            "type",
                        ],
                    )
                    RetVal_ColumnValue = Console.TextInput(
                        f"Enter the value for the field {RetVal_Column}"
                    )

                    # Dict update
                    Arguments[RetVal_Column] = RetVal_ColumnValue

                    # Ask for a new arguments
                    RetVal_SearchStatus = Console.Confirm(
                        "Do you want to add another parameter ?"
                    )
                    if RetVal_SearchStatus == False:
                        break

                # Seek and print
                data = DB.SeekOnDB(**Arguments)
                Console.PrintElements(
                    "Here the components that match your request. Make sure to note the RowID if an edit will be needed.",
                    data,
                )

            # Printing the whole database file.
            else:
                data = DB.SeekOnDB()
                Console.PrintElements(
                    "Here all of the components stored Make sure to note the RowID if an edit will be needed.",
                    data,
                )

        # Handling the exit action.
        elif RetVal_Action == "Exit the program":
            Status = False
            break

    DB.SaveAndClose()
    Console.log("Saved and closed DB.")


if __name__ == "__main__":
    main()
