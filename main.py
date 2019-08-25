
from response_creator import send_message
from flask import Flask, request, json
import vk
from settings import key, confirmation_token

app = Flask(__name__)





@app.route('/', methods=['POST'])
def processing():

    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        print(data)
        user_id = data['object']['from_id']
        user_message = data['object']['text']
        send_message(user_id, user_message)
        return 'ok'

