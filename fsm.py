from transitions.extensions import GraphMachine
import pymysql
from dbHandler import DBHandler

from utils import send_text_message, send_image_url, send_button_message, send_book_list, send_private_list


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )
        self.account = ""
        self.nickname = ""
        self.newPassword = ""
        self.viewPos = 0
        self.privateViewPos = 0

#----------------------------------------------------------------#


    def to_login(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'login'
        return False

    def to_accountOK(self, event):
        if event.get("message"):
            account = event['message']['text']
            db = self.accessDB()
            if db.confirmAccount(account) :
                self.account = account
                return True
            else :
                return False

    def to_loginSucceed(self, event):
        if event.get("message"):
            psd = event['message']['text']
            db = self.accessDB()
            return db.confirmPassword(psd)

    def to_register(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'register'
        return False

    def to_newAccountOK(self,  event):
        if event.get("message"):
            account = event['message']['text']
            db = self.accessDB()
            if db.confirmAccount(account) :
                return False
            else :
                self.account = account
                return True

    def to_newPasswordOK(self, event):
        if event.get("message"):
            password = event['message']['text']
            db = self.accessDB()
            return db.registerAccount(self.account, password)

    def make_new_nickname(self, event) :
        if event.get("message"):
            nickname = event['message']['text']
            db = self.accessDB()
            db.updateNickName(self.account, nickname)

    def to_changeNickName(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'change nickname'

    def change_nickname(self, event) :
        if event.get("message"):
            nickname = event['message']['text']
            db = self.accessDB()
            db.updateNickName(self.account, nickname)
            self.nickname = nickname
    
    def to_changePassword(self, event) :
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'change password'

    def before_confirmNewPassword(self, event) :
        if event.get("message"):
            self.newPassword = event['message']['text']

    def to_makeSureP(self, event) :
        if event.get("message"):
            return self.newPassword == event['message']['text']

    def to_viewList(self, event) :
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'recommend'

    def to_viewPrivateList(self, event) :
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'my books'

#----------------------------------------------------------------#

    def on_enter_user(self, event):
        self.account = ""
        self.nickname = ""
        sender_id = event['sender']['id']
        send_text_message(sender_id, "Back To HOME~")

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

    def on_enter_register(self, event) :
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "Your New Account :")

    def on_enter_newAccountOK(self, event) :
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "Your Account is : " + self.account + "\nYour Password :")

    def on_enter_newAccountFail(self, event) :
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "the account has been registered")
        self.back_register(event)

    def on_enter_newPasswordOK(self, event) :
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "register succeed!\nPlease set your nickname(can change later) :")
        self.goto_makeNickName(event)

    def on_enter_hall(self, event) :
        sender_id = event['sender']['id']
        responese = send_image_url(sender_id, "https://i.imgur.com/YH8h4dY.png")
        db = self.accessDB()
        self.nickname = db.getNickName(self.account)
        responese = send_text_message(sender_id, self.nickname + ", welcome to the hall :D")
        self.newPassword = ""
        self.viewPos = 0
        self.privateViewPos = 0

    def on_enter_changeNickName(self, event) :
        sender_id = event['sender']['id']
        msg = "your nickname is : \" %s \",\nPlease input a new nickname :" % (self.nickname)
        responese = send_text_message(sender_id, msg)

    def on_enter_changeNickNameSucceed(self, event) :
        sender_id = event['sender']['id']
        msg = "your new nickname is : \" %s \""% (self.nickname)
        responese = send_text_message(sender_id, msg)
        self.back_hall(event)

    def on_enter_changePassword(self, event) :
        sender_id = event['sender']['id']
        msg = "Please input your new password :"
        responese = send_text_message(sender_id, msg)

    def on_enter_confirmNewPassword(self, event) :
        sender_id = event['sender']['id']
        msg = "Please input your new password again:"
        responese = send_text_message(sender_id, msg)

    def on_enter_confirmNewPasswordFail(self, event) :
        sender_id = event['sender']['id']
        msg = "WRONG! :("
        responese = send_text_message(sender_id, msg)
        self.back_confirmNewPassword(event)

    def on_enter_makeSureP(self, event) :
        sender_id = event['sender']['id']
        text = "make sure change password"
        buttons = [
            {
                "type" : "postback",
                "title" : "Yes",
                "payload" : "MSP/Yes"
            },
            {
                "type" : "postback",
                "title" : "No",
                "payload" : "MSP/No"
            }
        ]
        send_button_message(sender_id, text, buttons)
        

    def on_enter_updatePassword(self, event) :
        db = self.accessDB()
        db.updatePassword(self.account, self.newPassword)
        sender_id = event['sender']['id']
        msg = "Change password succeed! :D"
        responese = send_text_message(sender_id, msg)
        self.back_hall(event)

    def on_enter_viewList(self, event) :
        sender_id = event['sender']['id']
        db = self.accessDB()
        books = db.getList(self.viewPos)
        if books :
            send_book_list(sender_id, books)
        else :
            send_text_message(sender_id, "no more recommended books!")

    def on_enter_viewPrivateList(self, event) :
        sender_id = event['sender']['id']
        db = self.accessDB()
        books = db.getPrivatebooks(self.account, self.privateViewPos)
        if books :
            send_private_list(sender_id, books)
        else :
            send_text_message(sender_id, "no more books in your list!")


    


#----------------------------------------------------------------#
       



#----------------------------------------------------------------#

    def accessDB(self):
        conn = DBHandler.connect()
        cursor = conn.cursor()
        db = DBHandler(conn, cursor)
        return db

    def userAdd(self, payload) :
        db = self.accessDB()
        db.addBook(self.account, payload)

    def userDelete(self, sender_id, PK) :
        db = self.accessDB()
        if db.deleteBook(self.account, PK) :
            send_text_message(sender_id, "delete succeed :)")
            self.privateViewPos -= 1
        else :
            send_text_message(sender_id, "Oops! there are some error")
    
    def badThing(self, sender_id) :
        db = self.accessDB()
        if db.deleteAllBook(self.account) :
            send_text_message(sender_id, "Vanishment This World!!!")
        else :
            send_text_message(sender_id, "Today is your day :D")

