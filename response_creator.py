import vk
import os
import importlib
from settings import token
from command_system import command_list

#keyboard = 'keyboard:{"one_time": false,"buttons": [[{"action": {"type": "text","payload": "{\"button\": \"1\"}","label": "Red"},"color": "negative"},{"action": {"type": "text","payload": "{\"button\": \"2\"}","label": "Green"},"color": "positive"}],[{"action": {"type": "text","payload": "{\"button\": \"3\"}","label": "White"},\
#"color": "default"},{"action": {"type": "text","payload": "{\"button\": \"4\"}","label": "Blue"},"color": "primary"}]]}'

keyboard_test = 'keyboard: \
{ \
    "one_time": false, \
    "buttons": [ \
      [{ \
        "action": { \
          "type": "text", \
          "payload": "{"button": "1"}", \
          "label": "Red" \
        }, \
        "color": "negative" \
      }, \
     { \
        "action": { \
          "type": "text", \
          "payload": "{\"button\": \"2\"}", \
          "label": "Green" \
        }, \
        "color": "positive" \
      }], \
      [{ \
        "action": { \
          "type": "text", \
          "payload": "{"button": "3"}", \
          "label": "White" \
        }, \
        "color": "default" \
      }, \
     { \
        "action": { \
          "type": "text", \
          "payload": "{"button": "4"}", \
          "label": "Blue" \
        }, \
        "color": "primary" \
      }] \
    ] \
  }'

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
    api.messages.send(access_token=token, user_id=str(user_id), message=msg, keyboard=keyboard_test)


def create_message(user_id, user_message):
    '''ищет сообщение юзера в списке команд, в зависимости от того, что он написал,
    сгенерируется соответствующее сообщение
    '''
    message = "Прости, не понимаю тебя."
    for c in command_list:
        if user_message.lower() in c.keys:
            message = c.process(user_id, user_message)
    return message
