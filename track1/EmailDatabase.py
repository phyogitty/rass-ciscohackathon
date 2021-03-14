import sqlite3
import mysql.connector

# TODO: Write proper documentation
class DatabaseHandler:

    def __init__(self):
        self.index = 0
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
        labs = ','.join(message['labelIds'])
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

    def retrieveNext(self):
        """
        TODO: Make this operation safer to perform
        TODO: Make this operation less reliant on fixed sets
        Get the next email in line
        :return: A dictionary with a single row's information
        """
        results = {}
        for row in self.cur.execute("SELECT * FROM emails WHERE rowid = ? limit 1", self.index):
            results['id'] = row[0]
            results['label'] = row[1]
            results['date'] = row[2]
            results['from'] = row[3]
            results['to'] = row[4]
            results['subject'] = row[5]
            results['body'] = row[6]
        self.index += 1
        if results:
            return results
        return None

    def point(self, id=0):
        """
        Change the row we're accessing with self.retrieveNext()
        :param id: Row id, 0 for start of the table
        """
        self.index = id