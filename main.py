"""
This is the entry point of the program.
"""

from Database import DataBase


def main():
    print("Hello Worlds !")

    DB = DataBase()
    DB.PrintDB()
    DB.SaveAndClose()


if __name__ == "__main__":
    main()