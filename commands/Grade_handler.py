import command_system
import psycopg2

list_with_double_classes = ['11г', '11к', '11л', '10в', '10к']


#users = {}

def klass_change(user_id, user_message):
    user_msg = user_message[0] + user_message[1] + user_message[-1].lower()
    conn = psycopg2.connect(host='ec2-54-217-235-137.eu-west-1.compute.amazonaws.com', port='5432', database='dbi9dq212bg4sq',
                            user='yvyloqfqwtebtk',
                            password='64092c34e652d59ef86eb0863fe845a4e1cd8f43444d06c25f2024de3e825f1d')
    cur = conn.cursor()

    cur.execute('select * from users')
    rows = cur.fetchall()
    message = 'класс, для которого отслыается расписание, изменён на' + '"' + user_msg + '"' + '.'
    for row in rows:
        if row[0] == user_id:
            cur.execute('update users set grade = %s where user_id = %s;', (user_msg, user_id))
            conn.commit()
            conn.close()
            return message
    cur.execute('insert into users(user_id, grade) values(%s, %s);', (user_id, user_msg))
    conn.commit()
    conn.close()
    return message




def klass_of_user(user_id):
    conn = psycopg2.connect(host='ec2-54-217-235-137.eu-west-1.compute.amazonaws.com', port='5432', database='dbi9dq212bg4sq',
                            user='yvyloqfqwtebtk',
                            password='64092c34e652d59ef86eb0863fe845a4e1cd8f43444d06c25f2024de3e825f1d')
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
                            '11 м', '11-м', '11м', '11-с', '11 с', '11с', '11л', '11 л', '11-л']
grade.process = klass_change

