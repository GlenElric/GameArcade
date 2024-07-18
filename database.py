import mysql.connector

class Database:
    def __init__(self):
        self.host = 'localhost'
        self.username = 'root'
        self.password = 'glenelric'
        self.database = 'games_arcade'

        # Create a connection to the MySQL server
        self.cnx = mysql.connector.connect(
            user=self.username,
            password=self.password,
            host=self.host
        )

        # Create a cursor object
        self.cursor = self.cnx.cursor()

        # Create the database if it doesn't exist
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(self.database))

        # Close the cursor
        self.cursor.close()

        # Reconnect to MySQL server using the new database
        self.cnx.close()
        self.cnx = mysql.connector.connect(
            user=self.username,
            password=self.password,
            host=self.host,
            database=self.database
        )

        # Reinitialize cursor for the new connection
        self.cursor = self.cnx.cursor()

# Usage
db_manager = Database()