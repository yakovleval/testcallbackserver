import xlrd
import datetime

import pytz
import commands.Grade_handler as klass
import command_system as command_system








rb = xlrd.open_workbook('r.xlsx')







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
    klassname = klass.klass_of_user(user_id)#цифра и буква класса
    klassnumber = klass_column_in_spreadsheet(klassname, user_id)#номер столбца класса
    daynumber = 2#счётчик, ищущий строку дня недели в таблице
    subj_number = 1#нумератор выдаваемых уроков (для красоты)
    message = ''
    if klassname in klass.list_with_double_classes:
        while str((sheet.row_values(daynumber)[0])).lower() != 'суббота':
            if str((sheet.row_values(daynumber)[klassnumber + 1])).lower() != '':
                message += str(subj_number) + '.' + str((sheet.row_values(daynumber)[klassnumber])).lower() + '/' + str((sheet.row_values(daynumber)[klassnumber + 1])).lower() + '\n'
                daynumber += 1
                subj_number += 1
            else:
                message += str(subj_number) + '.' + str((sheet.row_values(daynumber)[klassnumber])).lower() + '\n'
                daynumber += 1
                subj_number += 1
        while sheet.row_values(daynumber - 1)[klassnumber - 1] != sheet.row_values(-1)[klassnumber - 1]:
            if str((sheet.row_values(daynumber)[klassnumber + 1])).lower() != '':
                message += str(subj_number) + '.' + str((sheet.row_values(daynumber)[klassnumber])).lower() + '/' + str((sheet.row_values(daynumber)[klassnumber + 1])).lower() + '\n'
                daynumber += 1
                subj_number += 1

    else:
        while str((sheet.row_values(daynumber)[0])).lower() != 'суббота':
            message += str(subj_number) + '.' + str((sheet.row_values(daynumber)[klassnumber])).lower() + '\n'
            daynumber += 1
            subj_number += 1
        while sheet.row_values(daynumber - 1)[klassnumber - 1] != sheet.row_values(-1)[klassnumber - 1]:
            if str((sheet.row_values(daynumber)[klassnumber + 1])).lower() != '':
                message += str(subj_number) + '.' + str((sheet.row_values(daynumber)[klassnumber])).lower()  + '\n'
                daynumber += 1
                subj_number += 1




    return message


tomorrow_command = command_system.Command()

tomorrow_command.keys = ['неделя']
tomorrow_command.process = subjects_list