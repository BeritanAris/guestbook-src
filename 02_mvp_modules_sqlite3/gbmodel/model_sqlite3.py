"""
A simple guestbook flask app.
Data is stored in a SQLite database that looks something like the following:

+------------+------------------+---------------------+----------------+
| Name       | Email            | signed_on           | message        |
+============+==================+=====================+================+
| John Doe   | jdoe@example.com | 2012-05-28 12:00:22 | Hello world    |
+------------+------------------+---------------------+----------------+

This can be created with the following SQL (see bottom of this file):

    create table guestbook (name text, email text, signed_on datetime, message);

"""
from datetime import datetime
from .Model import Model
import sqlite3
DB_FILE = 'entries.db'    # file for our Database

class model(Model):
    def __init__(self):
        # Make sure our database exists
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT count(rowid) FROM guestbook")
        except sqlite3.OperationalError:
            cursor.execute("CREATE TABLE guestbook (name text, email text, signed_on timestamp, message)")
        cursor.close()

    def select(self):
        """
        Gets all rows from the database
        Each row contains: name, email, date, message
        :return: List of lists containing all rows of database
        """
        # We use PARSE_DECLTYPES to get the datetime object instead of a string
        # see https://docs.python.org/3/library/sqlite3.html#default-adapters-and-converters
        connection = sqlite3.connect(DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM guestbook")
        return cursor.fetchall()

    def insert(self, name, email, message):
        """
        Inserts entry into database
        :param name: String
        :param email: String
        :param message: String
        :return: True
        :raises: Database errors on connection and insertion
        """
        params = {'name':name, 'email':email, 'datetime':datetime.now(), 'message':message}
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO guestbook (name, email, signed_on, message) VALUES (:name, :email, :datetime, :message)", params)

        connection.commit()
        cursor.close()
        return True
