"""
This is the entry point of the program.
"""

from Database import DataBase


def main():
    print("Hello Worlds !")

    DB = DataBase()
    print(DB.AddComponentToStock("NE555P", "NE555", "SOIC16", "Timers", "", 1000))
    DB.PrintDB()
    DB.SaveAndClose()


if __name__ == "__main__":
    main()
