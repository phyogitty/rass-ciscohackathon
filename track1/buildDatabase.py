import sqlite3
import mysql.connector

# TODO: Write proper documentation
class DatabaseHandler:

    def __init__(self):
        self.conn = sqlite3.connect('rass.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS emails(
            id INT PRIMARY KEY,
            label_ids TEXT,
            date TEXT,
            fro TEXT,
            recv TEXT,
            subject TEXT,
            body TEXT
        )
        """)
        self.conn.commit()
        # Checking that the table was created
        exists = self.cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='emails'")
        if not exists:
            raise Exception

    def close(self):
        self.conn.commit()
        self.conn.close()

    def insert(self, message):
        """ WARNING: Security not tested, use at your own risk! """
        labs = ''.join(message['labelIds'])
        dat = message['date']
        fro = message['from']
        recv = message['to']
        subj = message['subject']
        bod = message['body']
        self.cur.execute("""
        INSERT INTO emails (label_ids, date, fro, recv, subject, body)
        VALUES (?,?,?,?,?,?)
        """, (labs, dat, fro, recv, subj, bod));
        self.conn.commit()
        return self.cur.rowcount

    # TODO: Set up procedure for adding new emails to the machine
    def retrieveNext(self):
        """

        :return:
        """
        print()