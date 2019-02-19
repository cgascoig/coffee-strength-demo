import os
import webexteamssdk
from kubernetes import client, config

webex = webexteamssdk.WebexTeamsAPI()
my_id = None

WEBHOOK_NAME="coffee-strength"

def kubernetes_get_webhook_url():
    print("Attempting to determine webhook URL from Kubernetes service ...")
    try:
        config.load_incluster_config()
        kube_client = client.CoreV1Api()

        current_namespace = open("/var/run/secrets/kubernetes.io/serviceaccount/namespace").read()
        print(f"Current Kubernetes namespace: {current_namespace}")

        lb_service = kube_client.read_namespaced_service('coffee-strength-bot-service', current_namespace)
        print(f"Got Kubernetes service details: {lb_service}")

        lb_ip = lb_service.status.load_balancer.ingress[0].ip
        port = lb_service.spec.ports[0].port

        url = f'http://{lb_ip}:{port}/webhook'

        return url
    except Exception as e:
        print(f"Error determining webhook URL from Kubernetes service: {e}")
        return None

def register_webhooks():
    if "WEBEX_TEAMS_WEBHOOK_URL" in os.environ:
        webhook_url = os.environ["WEBEX_TEAMS_WEBHOOK_URL"]
    else:
        webhook_url = kubernetes_get_webhook_url()

    if webhook_url is None:
        raise Exception("No WEBEX_TEAMS_WEBHOOK_URL environment variable and couldn't determine webhook URL from Kubernetes")
    
    print(f"Using webhook URL {webhook_url}")

    print("Deleting existing webhooks ... ")
    webhooks = webex.webhooks.list()
    for webhook in webhooks:
        print(webhook)
        webex.webhooks.delete(webhook.id)

    print("Creating webhook")
    webex.webhooks.create(
        name=WEBHOOK_NAME,
        targetUrl=webhook_url,
        resource="messages",
        event="created",
    )

def send_message(room_id, message):
    print(f"Sending message: {message}")
    webex.messages.create(roomId=room_id, text=message)

def get_message(message_id):
    return webex.messages.get(message_id)

def get_file(message):
    if message.files is None or len(message.files) < 1:
        return #no files present

    file_url = message.files[0]
    print(f"Getting file {file_url} ...")
    try:
        r = webex._session.request('GET', file_url, 200)
        if r.ok:
            print(f"Got file successfully ({len(r.content)} bytes)")
            return r.content
        else:
            print(f"Failed getting file: {r.status_code} {r.reason}")
    except Exception as e:
        print(f"Error occurred while getting file: {e}")
        return None
    
    return None

def get_my_id():
    global my_id
    if my_id is None:
        print("Getting bot's own information from WebEx")
        my_id = webex.people.me().id
    
    return my_id

if __name__ == "__main__":
    # if this module is run as a script (usually at pre-start) setup the webhooks
    register_webhooks()