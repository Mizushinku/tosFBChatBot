import pymysql
import sys, time, hashlib, datetime
import importlib
from bookInfo import BookInfo

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
        if account == 'foo' or account == 'user' or account == 'recommends' :
            return True
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

    def registerAccount(self, account, passowrd) :
        self.re_connect()
        result = False
        code = self.SHA256(passowrd)
        try :
            sql = "INSERT INTO user(account, nickname, password) VALUES('%s', 'guest', '%s')" % (account, code)
            self.cursor.execute(sql)
            self.conn.commit()
            result = True
        except :
            self.conn.rollback()
        return result

    def updateNickName(self, account, newName) :
        self.re_connect()
        result = False
        try :
            sql = "UPDATE user SET nickname = '%s' WHERE account = '%s'" % (newName, account)
            self.cursor.execute(sql)
            self.conn.commit()
            result = True
        except :
            self.conn.rollback()
        return result

    def getNickName(self, account) :
        self.re_connect()
        sql = "SELECT nickname FROM user WHERE account = '%s'" % (account)
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        return row[0]

    def updatePassword(self, account, newPassword) :
        self.re_connect()
        new_code = self.SHA256(newPassword)
        try :
            sql = "UPDATE user SET password = '%s' WHERE account = '%s'" % (new_code, account)
            self.cursor.execute(sql)
            self.conn.commit()
        except :
            self.conn.rollback()

    def getList(self, pos) :
        self.re_connect()
        #sql = "SELECT title, subtitle, image_url, payload FROM recommends WHERE PK > %d AND PK <= (%d + 3)" % (pos, pos)
        sql = "SELECT title, subtitle, image_url, payload FROM recommends ORDER BY PK ASC LIMIT %d, 3" % (pos)
        self.cursor.execute(sql)
        books = list(())
        if self.cursor.rowcount > 0 :
            for i in range(0, self.cursor.rowcount) :
                row = self.cursor.fetchone()
                books.append(BookInfo(row[0], row[1], row[2], row[3]))
        return books

    def addBook(self, account, payload) :
        self.re_connect()
        try :
            sql = "SELECT title, subtitle, image_url FROM recommends WHERE payload = '%s'" % (payload)
            self.cursor.execute(sql)
            row = self.cursor.fetchone()

            sql = "CREATE TABLE IF NOT EXISTS %s (PK INT auto_increment PRIMARY KEY,title VARCHAR(50),subtitle VARCHAR(80),image_url VARCHAR(200))ENGINE=innodb DEFAULT CHARSET=utf8" % (account)
            self.cursor.execute(sql)

            sql = "INSERT INTO %s(title,subtitle,image_url) VALUES('%s','%s','%s')" % (account, row[0], row[1], row[2])
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()

    def deleteBook(self, account, PK) :
        self.re_connect()
        result = False
        try :
            sql = "DELETE FROM %s WHERE PK = %s" % (account, PK)
            self.cursor.execute(sql)
            self.conn.commit()
            result = True
        except :
            self.conn.rollback()
        return result

    def deleteAllBook(self, account) :
        self.re_connect()
        result = False
        try :
            sql = "DELETE FROM %s WHERE 1" % (account)
            self.cursor.execute(sql)
            self.conn.commit()
            result = True
        except :
            self.conn.rollback()
        return result

    def getPrivatebooks(self, account, pos) :
        sql = "CREATE TABLE IF NOT EXISTS %s (PK INT auto_increment PRIMARY KEY,title VARCHAR(50),subtitle VARCHAR(80),image_url VARCHAR(200))ENGINE=innodb DEFAULT CHARSET=utf8" % (account)
        self.cursor.execute(sql)

        sql = "SELECT title, subtitle, image_url, PK FROM %s ORDER BY PK ASC LIMIT %d, 3" % (account, pos)
        self.cursor.execute(sql)
        books = list(())
        if self.cursor.rowcount > 0:
            for i in range(0, self.cursor.rowcount) :
                row = self.cursor.fetchone()
                books.append(BookInfo(row[0], row[1], row[2], row[3]))
        return books


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