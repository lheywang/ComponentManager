"""
This is the entry point of the program.
"""

from Database import DataBase

import pandas as pd


def main():
    print("Hello Worlds !")

    DB = DataBase()
    print(DB.AddComponentToStock("NE555P", "NE555", "SOIC8", "Timers", "", 1000))
    DB.PrintDB()

    print(DB.SeekOnDB(family="NE555", package="SOIC16"))

    DB.SaveAndClose()


if __name__ == "__main__":
    data = pd.read_csv("PCBA_3128D2_4.csv")
    print(data)
    main()
