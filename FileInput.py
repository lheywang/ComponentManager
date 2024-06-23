"""
This file manage auto inputs for differents files types
"""

import pandas as pd


def OpenFile(FilePath):
    FileType = IdentifyFile(FilePath)
    match FileType:
        case "xlsx":
            data = OpenXLSX(FilePath)
            return data
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
