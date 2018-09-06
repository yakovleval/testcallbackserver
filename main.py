
from response_creator import send_message
from flask import Flask, request, json



app = Flask(__name__)



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
        user_id = data['object']['user_id']
        user_message = data['object']['body']
        send_message(user_id, user_message)  # отсылает ответ
        # Сообщение о том, что обработка прошла успешно
        return 'ok'

