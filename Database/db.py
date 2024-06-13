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
        file_db.backup(self.__db__)

        # Closing the file DB
        file_db.close()

        # Statements to create tables for the the database.
        # Include a IF NOT EXISTS to not overwrite any data.
        create_table1 = f"""
        CREATE TABLE IF NOT EXISTS ComponentsReferences(
            id INTEGER PRIMARY KEY,
            reference text
        );
        """

        create_table2 = f"""
        CREATE TABLE IF NOT EXISTS Components(
            id INTEGER PRIMARY KEY,
            family text,
            package text,
            type text,
            value text,
            quantity int,
            FOREIGN KEY (family) REFERENCES ReferencesList (reference)
        );
        """

        # Creating tables if needed
        self.__db__.execute(create_table1)
        self.__db__.execute(create_table2)
        self.__db__.commit()

        self.__db__.execute("INSERT INTO ComponentsReferences VALUES (1, 'NE555')")

        self.__db__.commit()

        return

    def SaveAndClose(self):
        # Openning the file DB
        file_db = sqlite3.connect("stock.db")

        # Backup the ram DB to the file DB
        self.__db__.backup(file_db)

        # Closing both of the DB
        file_db.close()
        self.__db__.close()

        return

    def PrintDB(self):
        ret = self.__db__.execute("SELECT * FROM ComponentsReferences")
        print(ret.fetchall())

        return
