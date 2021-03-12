import sqlite3
import mysql.connector


class DatabaseHandler:
    current = 0

    def construct(self):
        conn = sqlite3.connect('rass.db')
        cur = conn.cursor()
        exists = cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='email'")

    def insert(self, message):
        """

        :param message:
        :return:
        """
        print()

    def retrieveNext():
        """

        :return:
        """
        print()