from flask import Flask, request, render_template
from webexteams import register_webhooks, send_message, get_my_id

app = Flask(__name__)

@app.route('/webhook', methods=["POST"])
def webhook():
    message_event_data = request.json['data']
    print(f"Message data: {message_event_data}")
    message_id = message_event_data["id"]
    room_id    = message_event_data["roomId"]
    
    if message_event_data["personId"] == get_my_id():
        print("Message from myself, ignoring")
        return ""

    send_message(room_id, "Hello")

    return "Webhook"

@app.route('/')                                                                 
def index():                                                                    
    return "Welcome" 

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)