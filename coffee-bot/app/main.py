from flask import Flask, request, render_template
import webexteams
import imagerec
import ifttt

app = Flask(__name__)

def strength_calc(score):
    strength = ""
    if score <= 60:
        strength = 'weak'
    elif score <= 80:
        strength = 'medium'
    else:
        strength = 'strong'
    app.logger.debug("Strength :%s" % strength)
    return strength

@app.route('/webhook', methods=["POST"])
def webhook():
    message_event_data = request.json['data']
    print(f"Message data: {message_event_data}")
    message_id = message_event_data["id"]
    room_id    = message_event_data["roomId"]
    
    if message_event_data["personId"] == webexteams.get_my_id():
        print("Message from myself, ignoring")
        return ""

    message = webexteams.get_message(message_id)
    if message is None:
        print("No message")
        return ""

    image_data = webexteams.get_file(message)

    fatigue_score = imagerec.get_fatique_score(image_data)

    strength = strength_calc(fatigue_score)
    ifttt.IFTTT_make_coffee(strength)

    reply = f"""
    Fatigue score: {int(fatigue_score * 100)/100}
    I will make {strength} coffee
    """

    webexteams.send_message(room_id, reply)

    return "Webhook"

@app.route('/')                                                                 
def index():                                                                    
    return "Welcome" 

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)