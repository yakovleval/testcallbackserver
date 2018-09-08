import xlrd
import datetime
import time
import pytz
import commands.Grade_handler as klass
import command_system as command_system
from commands.Grade_handler import list_with_double_classes as list







rb = xlrd.open_workbook('r.xlsx')




def tomorrow_day_number():
    '''

    :return: подряковый номер завтрашнего дня недели (отсчёт с нуля)
    '''
    now_date = datetime.date.today()


    utcmoment_naive = datetime.datetime.utcnow()
    utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc)
    localDatetime = utcmoment.astimezone(pytz.timezone('Asia/Ashkhabad'))

    if int(str(utcmoment)[11]+ str(utcmoment)[12]) > int(str(localDatetime)[11]+str(localDatetime)[12]):
        return (now_date.isoweekday() % 7 + 1) % 7
    else:
        return now_date.isoweekday() % 7



weekdays = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
#
def klass_column_in_spreadsheet(body, user_id):
    '''
    ищет номер столбца, в котором располагается требуемый класс
    :param body: номер и буква класса
    :param user_id: айди пользователя, чтобы по списку юзеров определить он в 11 классе или в 10, и в зависимости от этого переключиться на нужный лист экселя
    :return: номер столбца, в котором нужный класс
    '''
    global sheet
    userklass = klass.klass_of_user(user_id)
    if userklass[0] + userklass[1] == '11':
        sheet = rb.sheet_by_index(1)
    else:
        sheet = rb.sheet_by_index(0)
    klass_index = 2
    while str((sheet.row_values(0)[klass_index])).lower() != body:
        klass_index += 1
    return klass_index





def subjects_list(user_id, body):
    '''
    возвращает список уроков на завтраший день
    :param user_id: нужен, чтобы заюзать функции klass_of_user и klass_column_in_spreadsheet
    :param body: здесь бесполезен, нужен чтобы не нарушать логику вызова c.process, в ктр передаётся два аргумента
    :return:список уроков на некст день
    '''
    #if klass.klass_of_user(user_id) == '':
        #return 'Тебе необходимо отправить свой класс, чтобы получать расписание'
    t_day_number = tomorrow_day_number()#номер строчки, где начинается завтрашний день
    klassname = klass.klass_of_user(user_id)#цифра и буква класса
    if klassname == '':
        return 'тебе необходимо отправить свой класс, чтобы получать расписание'
    if weekdays[t_day_number] == 'воскресенье':
        return 'завтра выходной :>', True
    klassnumber = klass_column_in_spreadsheet(klassname, user_id)#номер столбца класса
    daynumber = 2#счётчик, ищущий строку дня недели в таблице
    subj_number = 1#нумератор выдаваемых уроков (для красоты)
    message = ''
    if klassname in klass.list_with_double_classes:
        while sheet.row_values(daynumber)[0].lower() != weekdays[t_day_number]: #ищет строку дня недели в таблице
            daynumber += 1
        if weekdays[t_day_number] == 'суббота':
            while sheet.row_values(daynumber - 1)[klassnumber - 1] != sheet.row_values(-1)[klassnumber - 1]:
                if str((sheet.row_values(daynumber)[klassnumber + 1])).lower() != '':
                    message += str(subj_number) + '.' + str((sheet.row_values(daynumber)[klassnumber])).lower() + '/' + str((sheet.row_values(daynumber)[klassnumber + 1])).lower() + '\n'
                    daynumber += 1
                    subj_number += 1
                else:
                    message += str(subj_number) + '.' + str((sheet.row_values(daynumber)[klassnumber])).lower() + '\n'
                    daynumber += 1
                    subj_number += 1

        else:
            while sheet.row_values(daynumber)[0].lower() != weekdays[t_day_number + 1]:
                if str((sheet.row_values(daynumber)[klassnumber + 1])).lower() != '':
                    message += str(subj_number) + '.' + str((sheet.row_values(daynumber)[klassnumber])).lower() + '/' + str((sheet.row_values(daynumber)[klassnumber + 1])).lower() + '\n'
                    daynumber += 1
                    subj_number += 1
                else:
                    message += str(subj_number) + '.' + str((sheet.row_values(daynumber)[klassnumber])).lower() + '\n'
                    daynumber += 1
                    subj_number += 1
    else:
        while sheet.row_values(daynumber)[0].lower() != weekdays[t_day_number]: #ищет строку дня недели в таблице
            daynumber += 1
        if weekdays[t_day_number] == 'суббота':
            while sheet.row_values(daynumber - 1)[klassnumber - 1] != sheet.row_values(-1)[klassnumber - 1]:
                message += str(subj_number) + '.' + str((sheet.row_values(daynumber)[klassnumber])).lower() + '\n'
                daynumber += 1
                subj_number += 1
        else:
            while sheet.row_values(daynumber)[0].lower() != weekdays[t_day_number + 1]:
                message += str(subj_number) + '.' + str((sheet.row_values(daynumber)[klassnumber])).lower() + '\n'
                daynumber += 1
                subj_number += 1



    '''
    for subject_line in range(daynumber, daynumber + 7):#прибавляет к message новый урок
        message += sheet.row_values(subject_line)[0].lower() + str(subj_number) + '.' + str((sheet.row_values(subject_line)[klassnumber])).lower() + '\n'
        subj_number += 1
    '''
    return message, True


tomorrow_command = command_system.Command()

tomorrow_command.keys = ['завтра', 'Завтра']
tomorrow_command.process = subjects_list