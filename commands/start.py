import command_system
def start_message(x,y):
    message = 'чтобы начать получать расписание, отправь свой класс'
    return message, False

start_command = command_system.Command()
start_command.keys = ['начать']
start_command.process = start_message