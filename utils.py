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

def send_book_list(id, books) :
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
                            "title" : books[0].title,
                            "subtitle" : books[0].subtitle,
                            "image_url" : books[0].image_url,
                            "buttons" : [
                                {
                                    "type" : "postback",
                                    "title" : "ADD",
                                    "payload" : books[0].payload
                                }
                            ]
                        },
                        {
                            "title" : books[1].title,
                            "subtitle" : books[1].subtitle,
                            "image_url" : books[1].image_url,
                            "buttons" : [
                                {
                                    "type" : "postback",
                                    "title" : "ADD",
                                    "payload" : books[1].payload
                                }
                            ]
                        },
                        {
                            "title" : books[2].title,
                            "subtitle" : books[2].subtitle,
                            "image_url" : books[2].image_url,
                            "buttons" : [
                                {
                                    "type" : "postback",
                                    "title" : "ADD",
                                    "payload" : books[2].payload
                                }
                            ]
                        },
                    ],
                    "buttons" : [
                        {
                            "type" : "postback",
                            "title" : "view more",
                            "payload" : "VBL/more"
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

def send_private_list(id, books) :
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient" : {"id":id},
        "message" : {
            "attachment" : {
                "type" : "template",
                "payload" : {
                    "template_type": "list",
                    "top_element_style": "compact",
                    "elements": [
                        {
                            "title" : books[0].title,
                            "subtitle" : books[0].subtitle,
                            "image_url" : books[0].image_url,
                            "buttons" : [
                                {
                                    "type" : "postback",
                                    "title" : "DELETE",
                                    "payload" : "DELETE"
                                }
                            ]
                        },
                        {
                            "title" : books[1].title,
                            "subtitle" : books[1].subtitle,
                            "image_url" : books[1].image_url,
                            "buttons" : [
                                {
                                    "type" : "postback",
                                    "title" : "DELETE",
                                    "payload" : "DELETE"
                                }
                            ]
                        },
                        {
                            "title" : books[2].title,
                            "subtitle" : books[2].subtitle,
                            "image_url" : books[2].image_url,
                            "buttons" : [
                                {
                                    "type" : "postback",
                                    "title" : "DELETE",
                                    "payload" : "DELETE"
                                }
                            ]
                        },
                    ],
                    "buttons" : [
                        {
                            "type" : "postback",
                            "title" : "view more",
                            "payload" : "VPBL/more"
                        }
                    ]
                }
            }
        }
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Unable to send private list: \n" + response.text)
    return response

