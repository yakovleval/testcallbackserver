import datetime

from flask import Flask, request, json

import vk

app = Flask(__name__)


token = 'a6ce7f02770d6f1c1ccbfc042bd349f9b208338ad1a2314612f5790e51e2f4e085fb6baf45f8f43857f4d'
confirmation_token = '6071d7c2'

@app.route('/', methods=['POST'])
def processing():
    #Распаковываем json из пришедшего POST-запроса
    data = json.loads(request.data)
    #Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        session = vk.Session()
        api = vk.API(session, v=5.50)
        user_id = data['object']['user_id']
        api.messages.send(access_token=token, user_id=str(user_id), message='Привет, я новый бот!' + datetime.datetime.now() )
        # Сообщение о том, что обработка прошла успешно
        return 'ok'
