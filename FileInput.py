"""
This file manage auto inputs for differents files types
"""

import pandas as pd


def OpenFile(FilePath):
    FileType = IdentifyFile(FilePath)
    match FileType:
        case "xlsx":
            data = OpenXLSX(FilePath)
        case "csv":
            data = OpenCSV(FilePath)
    return data


def IdentifyFile(FilePath):
    extension = FilePath.split(".")[-1]
    return str(extension)


def OpenCSV(FilePath):
    data = pd.read_csv(FilePath)
    data = data.to_dict(orient="records")
    return data


def OpenXLSX(FilePath):
    data = pd.read_excel(FilePath)
    data = data.to_dict(orient="records")
    return data


def OrderKeys(Console, Keys: list[str]):
    """
    The goal is to return a list of the keys that follow the requireds fields on the DB

    The correct order is : partname - Family - Package - Type - Value - Quantity - Manufacturer - Datasheet - Seller
    """
    Keys = list(Keys)
    Output = dict()
    RemainingArgs = [
        "partname",
        "family",
        "package",
        "type",
        "value",
        "quantity",
        "manufacturer",
        "datasheet",
        "seller",
    ]

    for Key in Keys:
        RemainingArgs.append("None")
        RetVal = Console.Ask(
            f"\nWith which Database column {Key} : match ?", RemainingArgs
        )
        if RetVal != "None":
            Output[RetVal] = Key
            RemainingArgs.remove(RetVal)
        RemainingArgs.remove("None")

    return Output


def PrepareData(Console, ArgsOrder, data):
    """
    The goal of this function is to prepare a list of tuples that are ready to be imported on the database.
    Missing values will be ignored.

    Arguments :
        ArgsOrder : A dict with the correct Arguments Order to match the doc.
        data : The panda exported data
    """
    DBOrder = [
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
    Output = []

    for ref in data:
        OutTupple = []
        for Arg in DBOrder:
            try:
                ArgName = ArgsOrder[Arg]
                OutTupple.append(str(ref[ArgName]))
            except:
                Console.log(f"Cannot find a field !", "red")

        Output.append(tuple(OutTupple))
    return Output
