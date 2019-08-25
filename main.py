
from response_creator import send_message
from flask import Flask, request, json
import vk


app = Flask(__name__)

key = '1e81968a155a6b554c34fd710349e7410ecd6804ff58788de3b2d1edb40e0af47cf4671546184958bc905'

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
        print(data)
        user_id = data['object']['from_id']
        user_message = data['object']['text']
        send_message(user_id, user_message)  # отсылает ответ
        # Сообщение о том, что обработка прошла успешно
        return 'ok'

