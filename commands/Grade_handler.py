import command_system
import psycopg2
from settings import host, port, database, user, password

list_with_double_classes = ['11г', '11к', '11л', '10в', '10к']


#users = {}

def klass_change(user_id, user_message):
    user_msg = user_message[0] + user_message[1] + user_message[-1].lower()
    conn = psycopg2.connect(host=host, port=port, database=database,
                            user=user,
                            password=password)
    cur = conn.cursor()

    cur.execute('select * from users')
    rows = cur.fetchall()
    message = 'класс, для которого отсылается расписание, изменён на ' + '"' + user_msg + '"' + '.' + '\n' + 'теперь, отправив команду сегодня/завтра/неделя, ты получишь соответствующее расписание. Чтобы изменить класс, ты можешь отправить мне новый в любой момент'
    for row in rows:
        if row[0] == user_id:
            cur.execute('update users set grade = %s where user_id = %s;', (user_msg, user_id))
            conn.commit()
            conn.close()
            return message
    cur.execute('insert into users(user_id, grade) values(%s, %s);', (user_id, user_msg))
    conn.commit()
    conn.close()
    return message, True




def klass_of_user(user_id):
    conn = psycopg2.connect(host=host, port=port, database=database,
                            user=user,
                            password=password)
    cur = conn.cursor()
    cur.execute('select * from users')
    rows = cur.fetchall()
    conn.close()
    for row in rows:
        if row[0] == user_id:
            return row[1]
    return ''






grade = command_system.Command()
grade.keys = ['10 а', '10-а','10а','10-б', '10 б','10б',
              '10 в', '10-в', '10в', '10-г', '10 г', '10г',
              '10 и', '10-и', '10и', '10-к', '10 к', '10к',
              '10 м', '10-м', '10м', '10-с', '10 с', '10с',
              '11 а', '11-а', '11а', '11-б', '11 б', '11б',
              '11 в', '11-в', '11в', '11-г', '11 г', '11г',
              '11 и', '11-и', '11и', '11-к', '11 к', '11к',
              '11 м', '11-м', '11м', '11-с', '11 с', '11с', '11л', '11 л', '11-л',
              '10 А', '10-А', '10А', '10-Б', '10 Б', '10Б',
              '10 В', '10-В', '10В', '10-Г', '10 Г', '10Г',
              '10 И', '10-И', '10И', '10-К', '10 К', '10К',
              '10 М', '10-М', '10М', '10-С', '10 С', '10С',
              '11 А', '11-А', '11А', '11-Б', '11 Б', '11Б',
              '11 В', '11-В', '11В', '11-Г', '11 Г', '11Г',
              '11 И', '11-И', '11И', '11-К', '11 К', '11К',
              '11 М', '11-М', '11М', '11-С', '11 С', '11С', '11Л', '11 Л', '11-Л'
              ]
grade.process = klass_change

