import sqlite3


class DataBase:
    def __init__(self, type: bool = False):
        """
        Initialize a new database. May be in memory or in disk

        Arguments :
            type : True for a RAM DB, False for a File
        """
        # Create a database in memory
        self.__db__ = sqlite3.connect(":memory:")

        # Openning the local file and dump it's content into the RAM.
        # If the file does not exist, it create a new one
        file_db = sqlite3.connect("stock.db")
        self.__db__.backup(file_db)

        # Closing the file DB
        file_db.close()

    def __del__(self):
        # Openning the file DB
        file_db = sqlite3.connect("stock.db")

        # Backup the ram DB to the file DB
        file_db.backup(self.__db__)

        # Closing both of the DB
        file_db.close()
        self.__db__.close()
