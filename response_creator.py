import vk
import os
import importlib
import json
from settings import token
from command_system import command_list

keyboard = {
    'one_time': True,
    'buttons': [[{
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '1'}),
            'label': 'Сегодня',
        },
        'color': 'primary'
    },
    {
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '2'}),
            'label': 'Завтра',
        },
        'color': 'primary'
    }],
    [{
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '2'}),
            'label': 'Неделя',
        },
        'color': 'primary'
    }
    ]]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))
def load_modules():
   # путь от рабочей директории, ее можно изменить в настройках приложения
   files = os.listdir('commands')
   modules = filter(lambda x: x.endswith('.py'), files)
   for m in modules:
       importlib.import_module("commands." + m[0:-3])

def send_message(user_id, user_message):
    '''отправляет сообщение юзеру'''
    session = vk.Session()
    api = vk.API(session, v=5.84)
    load_modules()
    msg = create_message(user_id, user_message)
    if msg[1]:
        api.messages.send(access_token=token, user_id=str(user_id), message=msg[0], keyboard=keyboard)
    else:
        api.messages.send(access_token=token, user_id=str(user_id), message=msg[0])


def create_message(user_id, user_message):
    '''ищет сообщение юзера в списке команд, в зависимости от того, что он написал,
    сгенерируется соответствующее сообщение
    '''
    message = "Прости, не понимаю тебя."
    for c in command_list:
        if user_message.lower() in c.keys:
            message = c.process(user_id, user_message)
    return message
