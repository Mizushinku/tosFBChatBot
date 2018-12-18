from bottle import route, run, request, abort, static_file

from fsm import TocMachine
from utils import send_text_message, send_button_message, send_book_list


VERIFY_TOKEN = "12399987"
machine = TocMachine(
    states=[
        'user',
        'login',
        'accountOK',
        'accountFail',
        'loginSucceed',
        'loginFail',
        'register',
        'newAccountOK',
        'newAccountFail',
        'newPasswordOK',
        'makeNickName',
        'hall',
        'changeNickName',
        'changeNickNameSucceed',
        'changePassword',
        'confirmNewPassword',
        'makeSureP',
        'updatePassword',
        'confirmNewPasswordFail',
        'viewList',
    ],
    transitions=[
        {
            'trigger': 'back_home',
            'source': [
                'login',
                'accountOK',
                'loginSucceed',
                'register',
                'newAccountOK',
                'hall',
            ],
            'dest':'user',
        },
        {
            'trigger' : 'back_hall',
            'source' : [
                'changeNickName',
                'changeNickNameSucceed',
                'changePassword',
                'confirmNewPassword',
                'makeSureP',
                'updatePassword',
                'viewList',
            ],
            'dest' : 'hall'
        },
        #-- view book list ------------
        {
            'trigger' : 'advance',
            'source' : 'hall',
            'dest' : 'viewList',
            'conditions' : 'to_viewList'
        },
        #-- change password -----------
        {
            'trigger' : 'advance',
            'source' : 'hall',
            'dest' : 'changePassword',
            'conditions' : 'to_changePassword'
        },
        {
            'trigger' : 'advance',
            'source' : 'changePassword',
            'dest' : 'confirmNewPassword',
            'before' : 'before_confirmNewPassword'
        },
        {
            'trigger' : 'advance',
            'source' : 'confirmNewPassword',
            'dest' : 'makeSureP',
            'conditions' : 'to_makeSureP'
        },
        {
            'trigger' : 'advance',
            'source' : 'confirmNewPassword',
            'dest' : 'confirmNewPasswordFail',
            'unless' : 'to_makeSureP'
        },
        {
            'trigger' : 'back_confirmNewPassword',
            'source' : 'confirmNewPasswordFail',
            'dest' : 'confirmNewPassword',
        },
        {
            'trigger' : 'goto_updatePassword',
            'source' : 'makeSureP',
            'dest' : 'updatePassword',
        },
        #-- change nickname -----------
        {
            'trigger' : 'advance',
            'source' : 'hall',
            'dest' : 'changeNickName',
            'conditions' : 'to_changeNickName'
        },
        {
            'trigger' : 'advance',
            'source' : 'changeNickName',
            'dest' : 'changeNickNameSucceed',
            'before' : 'change_nickname'
        },
        #-- login ---------------------
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'login',
            'conditions': 'to_login'
        },
        #-------- account -------------
        {
            'trigger': 'advance',
            'source': 'login',
            'dest':'accountOK',
            'conditions': 'to_accountOK',
        },
        {
            'trigger': 'advance',
            'source': 'login',
            'dest':'accountFail',
            'unless': 'to_accountOK',
        },
        {
            'trigger': 'back_login',
            'source': 'accountFail',
            'dest':'login',
        },
        #-------- password -------------
        {
            'trigger': 'advance',
            'source': 'accountOK',
            'dest':'loginSucceed',
            'conditions' : 'to_loginSucceed'
        },
        {
            'trigger': 'advance',
            'source': 'accountOK',
            'dest':'loginFail',
            'unless' : 'to_loginSucceed'
        },
        {
            'trigger': 'back_login',
            'source': 'loginFail',
            'dest':'accountOK',
        },
        {
            'trigger' : 'intoHall',
            'source' : 'loginSucceed',
            'dest' : 'hall',
        },
        #-- register ---------------------
        {
            'trigger' : 'advance',
            'source' : 'user',
            'dest' : 'register',
            'conditions' : 'to_register'
        },
        #-------- newAccount --------------
        {
            'trigger' : 'advance',
            'source' : 'register',
            'dest' : 'newAccountOK',
            'conditions' : 'to_newAccountOK'
        },
        {
            'trigger' : 'advance',
            'source' : 'register',
            'dest' : 'newAccountFail',
            'unless' : 'to_newAccountOK'
        },
        {
            'trigger' : 'back_register',
            'source' : 'newAccountFail',
            'dest' : 'register'
        },
        #-------- newPassword --------------
        {
            'trigger' : 'advance',
            'source' : 'newAccountOK',
            'dest' : 'newPasswordOK',
            'conditions' : 'to_newPasswordOK'
        },
        {
            'trigger' : 'goto_makeNickName',
            'source' : 'newPasswordOK',
            'dest' : 'makeNickName',
        },
        #-------- newNickName --------------
        {
            'trigger' : 'advance',
            'source' : 'makeNickName',
            'dest' : 'hall',
            'before' : 'make_new_nickname'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
    ignore_invalid_triggers=True
)



@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

    else:
        abort(403)

post_cnt = 0
@route("/webhook", method="POST")
def webhook_handler():
    global post_cnt
    post_cnt += 1
    body = request.json
    print('\nFSM STATE: ' + machine.state)
    print('REQUEST BODY: ')
    print(body)

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        if 'postback' in event  :
            handle_postback(event)
        else :
            handle_text(event)
        

        print("\n\n----***-------***-----***----***----***---  %d\n\n" % (post_cnt))
        return 'OK'


@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return static_file('fsm.png', root='./', mimetype='image/png')


def handle_text(event) :
    text = event['message']['text']
    sender_id = event['sender']['id']
    if text.lower() == '!state':
        send_text_message(sender_id, 'FSM SATTE = ' + machine.state)
    elif text.lower() == '!who' :
        if(machine.account == "") :
            send_text_message(sender_id, "* not login *")
        else :
            msg = "Hi, %s (%s)" % (machine.nickname, machine.account)
            send_text_message(sender_id, msg)
    elif text.lower() == '!home':
        machine.back_home(event)
    elif text.lower() == '!hall' :
        machine.back_hall(event)
    elif text.lower() == '!list' :
        send_book_list(sender_id)
    else:
        machine.advance(event)


def handle_postback(event) :
    payload = event['postback']['payload'].split("/")
    if payload[0] == 'MSP' :
        if payload[1] == 'Yes' :
            machine.goto_updatePassword(event)
        else :
            machine.back_hall(event)
    elif False:
        pass


if __name__ == "__main__":
    run(host="localhost", port=5000, debug=True, reloader=True)
