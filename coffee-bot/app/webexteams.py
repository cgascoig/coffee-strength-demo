import os
import webexteamssdk
from flask import g

webex = webexteamssdk.WebexTeamsAPI()

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

def get_my_id():
    if 'my_id' not in g:
        print("Getting bot's own information from WebEx")
        g.my_id = webex.people.me().id
    
    return g.my_id

if __name__ == "__main__":
    # if this module is run as a script (usually at pre-start) setup the webhooks
    register_webhooks()