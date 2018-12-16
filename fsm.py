from transitions.extensions import GraphMachine
import pymysql
from dbHandler import DBHandler

from utils import send_text_message, send_image_url


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )

#----------------------------------------------------------------#

    def to_home(self):
        if self.state == 'user':
            return False
        return True

    def to_login(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'login'
        return False

    def to_accountOK(self, event):
        if event.get("message"):
            account = event['message']['text']
            db = self.accessDB()
            return db.confirmAccount(account)

    def to_loginSucceed(self, event):
        if event.get("message"):
            psd = event['message']['text']
            db = self.accessDB()
            return db.confirmPassword(psd)


#----------------------------------------------------------------#

    def on_enter_user(self):
        print("I'm starting form initial state!")

    def on_enter_login(self, event):
        print("I'm login...")

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "Your Account :")
    
    def on_enter_accountOK(self, event):
        print("Account confirm")
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "Your Password :")

    def on_enter_accountFail(self, event):
        print("Account Fail")
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "wrong account!")
        self.back_login(event)

    def on_enter_loginSucceed(self, event) :
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "~~~ login succeed ~~~")
        responese = send_image_url(sender_id, "https://i.imgur.com/74fMPke.png")
        self.intoHall(event)

    def on_enter_loginFail(self, event) :
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "wrong password!")
        self.back_login(event)

    def on_enter_hall(self, event) :
        sender_id = event['sender']['id']
        responese = send_image_url(sender_id, "https://i.imgur.com/YH8h4dY.png")


#----------------------------------------------------------------#
       



#----------------------------------------------------------------#

    def accessDB(self):
        conn = DBHandler.connect()
        cursor = conn.cursor()
        db = DBHandler(conn, cursor)
        return db
