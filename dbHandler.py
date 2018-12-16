import pymysql
import sys, time, hashlib, datetime
import importlib

pymysql.install_as_MySQLdb()

class DBHandler:

    def __init__(self, conn_in, cursor_in):
        self.conn = conn_in
        self.cursor = cursor_in

    @staticmethod
    def connect():
        conn = pymysql.connect(host = "140.116.82.52",
                               port = 3306,
                               user = "tos2018_FB_bot",
                               password = "fb_ChatBot",
                               db = "tosFBot",
                               charset = "utf8")
        return conn

    def re_connect(self):
        try :
            sql = "SELECT null FROM foo"
            self.cursor.execute(sql)
        except pymysql.err.OperationalError as e :
            if 'MySQL server has gone away' in str(e) :
                self.conn = DBHandler.connect()
                self.cursor = self.conn.cursor()
            else :
                raise e

    def confirmAccount(self, account):
        self.re_connect()
        result = False
        sql = "SELECT account FROM user WHERE account = '%s'" % (account)
        self.cursor.execute(sql)
        if self.cursor.rowcount == 1:
            result = True

        return result

    def confirmPassword(self, password):
        self.re_connect()
        result = False
        code = self.SHA256(password)
        sql = "SELECT password FROM user WHERE password = '%s'" % (code)
        self.cursor.execute(sql)
        if self.cursor.rowcount == 1:
            result = True

        return result

    def SHA256(self, string):
        encoder = hashlib.sha256()
        encoder.update(string.encode('utf-8'))
        code = encoder.hexdigest().upper()
        return code

"""
conn = DBHandler.connect()
c = conn.cursor()
db = DBHandler(conn, c)
print(db.confirmAccount("account"))
"""