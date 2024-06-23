"""
This is the entry point of the program.
"""

from Database import DataBase
from Console import ConsolePrinter
from FileInput import OpenFile


def main():
    Console = ConsolePrinter()
    Console.log("Openning Database ...")
    DB = DataBase()

    Console.log("Done !")
    print(DB.AddComponentToStock("NE555P", "NE555", "SOIC8", "Timers", "", 1000))
    DB.PrintDB()

    print(DB.SeekOnDB(family="NE555", package="SOIC16"))

    DB.SaveAndClose()

    ret = Console.Ask(
        "Choose what action to do : ",
        [
            "Import from a CSV file",
            "Import from Excel file",
            "Type references by your own",
        ],
    )


if __name__ == "__main__":
    print(OpenFile("PCBA_3128D2_4.csv"))
    main()
