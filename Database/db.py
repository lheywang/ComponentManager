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
            partname text,
            package text,
            type text,
            value text,
            quantity int,
            FOREIGN KEY (family) REFERENCES ReferencesList (reference)
            UNIQUE (partname, package, type)
        );
        """

        # Creating tables if needed
        self.__db__.execute(create_table1)
        self.__db__.execute(create_table2)
        self.__db__.commit()

        return

    def SaveAndClose(self):
        """
        Shall be called right before closing the class. Save all of the modifications to the database to file system.
        """
        # Openning the file DB
        file_db = sqlite3.connect("stock.db")

        # Backup the ram DB to the file DB
        self.__db__.backup(file_db)

        # Closing both of the DB
        file_db.close()
        self.__db__.close()

        return

    def PrintDB(self):
        """
        Print all of tables
        """
        ret = self.__db__.execute("SELECT * FROM ComponentsReferences")
        print(ret.fetchall())
        ret = self.__db__.execute("SELECT * FROM Components")
        print(ret.fetchall())

        return

    def AddComponentToStock(self, partname, Family, Package, Type, Value, Quantity):
        """
        This function add a component to the stock.

        Arguments :
            PartName : The EXACT reference of a part : Example : KX603J105 or NE555PB
            Family : The family of the part : Example : 100nF or NE555
            Package : The Package for the stock : Example : 0603 or SOIC8
            Type : A type of the components : Example : Capacitor or Timers
            Value : Reserved for pasive components. This is TEXT !! Example : '100nF'
            Quantity : The number of components in stock.

        Returns :
            retval : True | False : The field has been added or not
        """

        retval = True

        ret = self.__db__.execute(
            f"SELECT * FROM ComponentsReferences WHERE reference = '{Family}'"
        )
        ret = ret.fetchall()

        if len(ret) == 0:
            self.__db__.execute(
                f"INSERT INTO ComponentsReferences (reference) VALUES ('{Family}')"
            )
            self.__db__.commit()

        try:
            self.__db__.execute(
                f"INSERT INTO Components (family, partname, package, type, value, quantity) VALUES ('{Family}','{partname}', '{Package}', '{Type}', '{Value}', {Quantity})"
            )

        except Exception as e:
            retval = False

        finally:
            self.__db__.commit()

        return retval
