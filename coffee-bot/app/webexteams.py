import os
import webexteamssdk
from flask import g

webex = webexteamssdk.WebexTeamsAPI()
my_id = None

def register_webhooks():
    print("Deleting existing webhooks")
    webhooks = webex.webhooks.list()
    for webhook in webhooks:
        print(webhook)
        webex.webhooks.delete(webhook.id)

    print("Creating webhook")
    webex.webhooks.create(
        name="coffee-strength",
        targetUrl=os.environ["WEBEX_TEAMS_WEBHOOK_URL"],
        resource="messages",
        event="created",
    )

def send_message(room_id, message):
    print(f"Sending message: {message}")
    webex.messages.create(roomId=room_id, text=message)

def get_message(message_id):
    webex.messages.get(message_id)

def get_my_id():
    global my_id
    if my_id is None:
        print("Getting bot's own information from WebEx")
        my_id = webex.people.me().id
    
    return my_id

if __name__ == "__main__":
    # if this module is run as a script (usually at pre-start) setup the webhooks
    register_webhooks()