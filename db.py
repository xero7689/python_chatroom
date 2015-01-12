__author__ = 'Peter'

import sqlite3
import time
import datetime


class ChatDB:

    def __init__(self, dbname):
        # Don't forget to add timeout, or sqlite3 will raise database locked error!
        self.con = sqlite3.connect(dbname, timeout=10)
        self.cur = self.con.cursor()

        self.init_table("user", "(account text primary key, pwd text)")

    def init_table(self, tn, tattr):
        try:
            self.cur.execute("CREATE TABLE {} {}".format(tn, tattr))
        except sqlite3.Error as e:
            print e.args[0]

    def add_new_user(self, account, pwd):
        try:
            self.cur.execute("INSERT INTO user(account, pwd) VALUES(?, ?)", (account, pwd))
            self.con.commit()
            print "User {} sign up success.".format(account)
            return True
        except sqlite3.Error as e:
            print e.args[0]
            return False

    def check_account(self, account, password):
        try:
            dbdata = self.cur.execute("SELECT * FROM user WHERE account=?", (account,))
            user = dbdata.next()
            if password == user[1]:
                return True
            else:
                return False

        except StopIteration:
            msg = "[StopIteration]:Account Doesn't Exists."
            print msg
            return msg

        except sqlite3.Error as e:
            print e.message
            return e.message

    def add_today_chat(self):
        tn = self.get_today()
        try:
            self.cur.execute("CREATE TABLE {} (ptime text, account text, content text)".format(tn))
        except sqlite3.Error as e:
            print e.args[0]

    def add_new_post(self, user, send_time, content):
        tn = self.get_today()
        while True:
            try:
                self.cur.execute("INSERT INTO " + tn + " VALUES(?, ?, ?)", (send_time, user, content))
                self.con.commit()
                break
            except sqlite3.Error as e:
                self.add_today_chat()

    def get_today(self):
        today = datetime.date.today()
        return "d{}m{}y{}".format(str(today.day), str(today.month), str(today.year))
