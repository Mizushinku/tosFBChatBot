import requests
import os


GRAPH_URL = "https://graph.facebook.com/v2.6"
ACCESS_TOKEN = os.environ.get("Bot_ACCESS_TOKEN")


def send_text_message(id, text):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {"text": text}
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response



def send_image_url(id, img_url):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient" : {"id": id},
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": img_url,
                    "is_reusable": True
                }
            }
        }
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send image: \n" + response.text)
    return response


def send_button_message(id, text, buttons):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient" : {"id": id},
        "message" : {
            "attachment" : {
                "type" : "template",
                "payload" : {
                    "template_type" : "button",
                    "text" : text,
                    "buttons" : buttons
                }
            }
        }
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Unable to send button: \n" + response.text)
    return response

def send_book_list(id) :
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient" : {"id":id},
        "message" : {
            "attachment" : {
                "type" : "template",
                "payload" : {
                    "template_type": "list",
                    "top_element_style": "large",
                    "elements": [
                        {
                            "title" : "Recommend",
                            "subtitle" : "books recommended for you ~",
                            "image_url" : "https://i.imgur.com/gcUT5vZ.png",
                        },
                        {
                            "title" : "果青",
                            "subtitle" : "果然我的青春戀愛喜劇搞錯了",
                            "image_url" : "https://i.imgur.com/bLyJEYK.jpg",
                            "buttons" : [
                                {
                                    "type" : "postback",
                                    "title" : "ADD",
                                    "payload" : "VBL/hamachi"
                                }
                            ]
                        },
                    ],
                    "buttons" : [
                        {
                            "type" : "postback",
                            "title" : "view more",
                            "payload" : "VBS/more"
                        }
                    ]
                }
            }
        }
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Unable to send list: \n" + response.text)
    return response

