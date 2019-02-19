import requests
import os

def IFTTT_make_coffee(strength):
    payload = {
      'value1' : strength
    }

    url = f"https://maker.ifttt.com/trigger/{os.environ['IFTTT_BASE_WEBHOOK_NAME']}_{strength}/with/key/{os.environ['IFTTT_KEY']}"

    print("IFTTT URL: '%s'" % url)
    r = requests.post(url, json=payload)
    return True

