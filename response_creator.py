import vk
import os
import importlib
from command_system import command_list


token = 'a6ce7f02770d6f1c1ccbfc042bd349f9b208338ad1a2314612f5790e51e2f4e085fb6baf45f8f43857f4d'


def load_modules():
   # путь от рабочей директории, ее можно изменить в настройках приложения
   files = os.listdir('commands')
   modules = filter(lambda x: x.endswith('.py'), files)
   for m in modules:
       importlib.import_module("commands." + m[0:-3])

def send_message(user_id, user_message):
    '''отправляет сообщение юзеру'''
    session = vk.Session()
    api = vk.API(session, v=5.50)
    load_modules()
    msg = create_message(user_id, user_message)
    api.messages.send(access_token=token, user_id=str(user_id), message= msg)


def create_message(user_id, user_message):
    '''ищет сообщение юзера в списке команд, в зависимости от того, что он написал,
    сгенерируется соответствующее сообщение
    '''
    message = "Прости, не понимаю тебя."
    for c in command_list:
        if user_message in c.keys:
            message = c.process(user_id, user_message)
    return message
