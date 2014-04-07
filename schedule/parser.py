# -*- coding: utf-8 -*-
__author__ = 'shyr1punk'

import datetime
import xlrd
import urllib2
import urlparse
import urllib
from schedule.models import Group, Lesson, Subject, Teacher, Type, Auditory


def fixurl(url):
    # turn string into unicode
    if not isinstance(url, unicode):
        url = url.decode('utf8')

    # parse it
    parsed = urlparse.urlsplit(url)

    # divide the netloc further
    userpass, at, hostport = parsed.netloc.rpartition('@')
    user, colon1, pass_ = userpass.partition(':')
    host, colon2, port = hostport.partition(':')

    # encode each component
    scheme = parsed.scheme.encode('utf8')
    user = urllib.quote(user.encode('utf8'))
    colon1 = colon1.encode('utf8')
    pass_ = urllib.quote(pass_.encode('utf8'))
    at = at.encode('utf8')
    host = host.encode('idna')
    colon2 = colon2.encode('utf8')
    port = port.encode('utf8')
    path = '/'.join(  # could be encoded slashes!
        urllib.quote(urllib.unquote(pce).encode('utf8'),'')
        for pce in parsed.path.split('/')
    )
    query = urllib.quote(urllib.unquote(parsed.query).encode('utf8'), '=&?/')
    fragment = urllib.quote(urllib.unquote(parsed.fragment).encode('utf8'))

    # put it back together
    netloc = ''.join((user, colon1, pass_, at, host, colon2, port))
    return urlparse.urlunsplit((scheme, netloc, path, query, fragment))


#Функция возвращает верхняя или нижняя неделя у принятой даты
def week_even(year, month, day):
    return [u'В', u'Н'][datetime.date(year, month, day).isocalendar()[1] % 2]


class Parser():

    def __init__(self, group_id, url):
        self.id = group_id
        self.url = fixurl(url)
        self.year = 2014
        self.lessons_list = []

    def parse(self):
        f = open('e:/errors.txt', 'a')
        try:
            xls = urllib2.urlopen(self.url)
        except ValueError:
            f.write('Error: ID: ' + str(self.id) + 'URL: ' + self.url + '\n')
            f.close()
            return
        f.write('Success: ID: ' + str(self.id) + 'URL: ' + self.url + '\n')
        f.close()
        rb = xlrd.open_workbook(file_contents=xls.read())

        if xls.info().getheader('Content-Type') != 'application/vnd.ms-excel':
            f = open('e:\errors.txt', 'w')
            f.write('ID: ' + self.id + 'type')
            f.close()
            return

        for sheetNumber in range(0, rb.nsheets):
            if sheetNumber == 1:
                continue
            sheet = rb.sheet_by_index(sheetNumber)
            rows = []
            row_number = 0
            for row_number in range(sheet.nrows):  # считываем строки Excel файла
                rows.append(sheet.row_values(row_number))
            #return rows
            # подготавливаем к записи в БД
            for i in range(1, row_number):
                # ищем занятия
                if rows[i - 1][0] != '':
                    number = int(rows[i - 1][0])   # номер пары
                if rows[i][2] == u'Лекция' or rows[i][2] == u'Пр.Зан.' or rows[i][2] == u'Лаб.раб.' or rows[i][2] == u'Семинар':
                    if rows[i - 1][0] != '':
                        number = int(rows[i - 1][0])   # номер пары
                        week = rows[i - 1][1]
                    if rows[i - 1][1] != '':
                        week = rows[i - 1][1]     # день недели
                    lesson_type = rows[i][2]  # тип пары
                    teacher = rows[i][4]     # преподаватель
                    auditory = rows[i][6]    # аудитория
                    subject = rows[i - 1][2]  # название предмета
                    days_string = rows[i + 1][2]  # строка дни проведения занятий
                    days = []  # массив с днями проведения занятий
                    excluded = []  # временный массив для хранения исключаемых занятий
                    # ищем дни проведения
                    # когда есть пары "только"
                    if days_string.find(u'только') != -1:
                        for j in range(6, len(days_string)):
                            if days_string[j] == u'.':
                                d = days_string[j - 2: j + 3]
                                days.append(datetime.date(self.year, int(d[3:5]), int(d[0:2])))
                    else:
                        # когда есть "с xx.xx по xx.xx"
                        frm = days_string.find(u'с ')
                        if frm != -1:
                            begin = days_string[frm + 2:frm + 7]  # начало периода пар
                            datebegin = datetime.date(self.year, int(begin[3:5]), int(begin[0:2]))  # приводим к формату даты
                            end = days_string[frm + 11:frm + 16]  # конец периода
                            dateend = datetime.date(self.year, int(end[3:5]), int(end[0:2]))
                            exclude = days_string.find(u'кроме ')
                            if exclude != -1:   # если есть слово "кроме" в строке
                                for j in range(exclude + 6, len(days_string)):
                                    if days_string[j] == u'.':
                                        e = days_string[j - 2: j + 3]
                                        ex = datetime.date(self.year, int(e[3:5]), int(e[0:2]))
                                        excluded.append(ex)
                                        # вычисляем шаг проведения пар (7 или 14 дней)
                            if week == '':  # если чётность недели пустая - пара на каждой неделе
                                step = 7
                                d = datebegin
                            else:
                                step = 14
                                if week_even(self.year, int(begin[3:5]), int(begin[0:2])) == week:
                                    d = datebegin
                                else:
                                    d = datebegin + datetime.timedelta(days=7)
                            # записываем все дни в список дней
                            while d <= dateend:
                                days.append(d)
                                d += datetime.timedelta(days=step)
                                # исключаем дни из списка "кроме"
                            for e in excluded:
                                for ds in days:
                                    if e == ds:
                                        days.remove(ds)
                    self.write_lesson(lesson_type, subject, teacher, days, number, auditory)
        #Записываем одним запросом все занятия
        Lesson.objects.bulk_create(self.lessons_list)

    def write_lesson(self, lesson_type, subject, prep, days, number, audit):
    # Определяем индекс типа занятия (их 3, поэтому определяем их заранее)
        if lesson_type == u'Лекция':
            db_lesson_type = 1
        elif lesson_type == u'Пр.Зан.':
            db_lesson_type = 2
        elif lesson_type == u'Лаб.раб.':
            db_lesson_type = 3
        elif lesson_type == u'Семинар':
            db_lesson_type = 4
        else:
            db_lesson_type = 1

        #Ищем предмет в БД или создаём новый
        try:
            subj = Subject.objects.get(subj_full=subject)
        except Subject.DoesNotExist:
            db_subject = Subject(
                subj_full=subject,
                subj_short='',
            )
            db_subject.save()
            subj = db_subject

        #Аудитория
        try:
            auditory = Auditory.objects.get(title=audit)
        except Auditory.DoesNotExist:
            db_auditory = Auditory(
                title=audit,
            )
            db_auditory.save()
            auditory = db_auditory

        #Преподаватель
        try:
            teacher = Teacher.objects.get(name=prep)
        except Teacher.DoesNotExist:
            db_teacher = Teacher(
                name=prep,
            )
            db_teacher.save()
            teacher = db_teacher
        #Добавляем в список всех занятий новые
        for day in days:
            self.lessons_list.append(Lesson(
                number=number,
                date=day,
                subject=subj,
                teacher=teacher,
                lesson_type=Type.objects.get(id=db_lesson_type),
                group=Group.objects.get(id=self.id),
                auditory=auditory,
            ))
