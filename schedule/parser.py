# -*- coding: utf-8 -*-
__author__ = 'shyr1punk'

import datetime
import xlrd
import urllib
from schedule.models import Group, Lesson, Subject, Teacher, Type


class Parser():

    def __init__(self, groupID, url):
        self.id = groupID
        self.url = url

    def parse(self):
        xls = urllib.urlopen(self.url)
        f = open('/var/www/shyr1punk/data/temp.xls', 'w')
        f.write(xls.read())
        f.close()
        rb = xlrd.open_workbook('/var/www/shyr1punk/data/temp.xls')
        sheets = [0, 2, 3]
        #table = []
        for sheetnum in sheets:
            sheet = rb.sheet_by_index(sheetnum)
            rows = []
            rownum = 0
            for rownum in range(sheet.nrows):  # считываем строки Excel файла
                rows.append(sheet.row_values(rownum))
            # подготавливаем к записи в БД
            for i in range(1, rownum):
                # ищем занятия
                if rows[i][2] == u'Лекция' or rows[i][2] == u'Пр.Зан.' or rows[i][2] == u'Лаб.раб.' or rows[i][2] == u'Семинар':
                    if rows[i - 1][0] != '':
                        number = int(rows[i - 1][0])   # номер пары
                        week = rows[i - 1][1]
                    if rows[i - 1][1] != '':
                        week = rows[i - 1][1]     # день недели
                    lestype = rows[i][2]  # тип пары
                    prep = rows[i][4]     # преподаватель
                    audit = rows[i][6]    # аудитория
                    predmet = rows[i - 1][2]  # название предмета
                    sdays = rows[i + 1][2]  # строка дни проведения занятий
                    days = []  # массив с днями проведения занятий
                    excluded = []  # временный массив для хранения исключаемых занятий
                    # ищем дни проведения
                    # когда есть пары "только"
                    if sdays.find(u'только') != -1:
                        for j in range(6, len(sdays)):
                            if sdays[j] == u'.':
                                d = sdays[j - 2: j + 3]
                                days.append(datetime.date(2013, int(d[3:5]), int(d[0:2])))
                    else:
                        # когда есть "с xx.xx по xx.xx"
                        frm = sdays.find(u'с ')
                        if frm != -1:
                            begin = sdays[frm + 2:frm + 7]  # начало периода пар
                            datebegin = datetime.date(2013, int(begin[3:5]), int(begin[0:2]))  # приводим к формату даты
                            end = sdays[frm + 11:frm + 16]  # конец периода
                            dateend = datetime.date(2013, int(end[3:5]), int(end[0:2]))
                            exclude = sdays.find(u'кроме ')
                            if exclude != -1:   # если есть слово "кроме" в строке
                                for j in range(exclude + 6, len(sdays)):
                                    if sdays[j] == u'.':
                                        e = sdays[j - 2: j + 3]
                                        ex = datetime.date(2013, int(e[3:5]), int(e[0:2]))
                                        excluded.append(ex)
                                        # вычисляем шаг проведения пар (7 или 14 дней)
                            if week == '':  # если чётность недели пустая - пара на каждой неделе
                                step = 7
                            else:
                                step = 14
                                # записываем все дни в список дней
                            d = datebegin
                            while d <= dateend:
                                days.append(d)
                                d += datetime.timedelta(days=step)
                                # исключаем дни из списка "кроме"
                            for e in excluded:
                                for ds in days:
                                    if e == ds:
                                        days.remove(ds)
                    #tablerow = [lestype, predmet, prep, days, number, audit]
                    #table.append(tablerow)
                    self.writeLesson(lestype, predmet, prep, days, number, audit)
        #return table

    def writeLesson(self, lestype, predmet, prep, days, number, audit):
    # Определяем индекс типа занятия (их 3, поэтому определяем их заранее)
        if lestype == u'Лекция':
            dblestype = 1
        else:
            if lestype == u'Пр.Зан.':
                dblestype = 2
            else:
                if lestype == u'Лаб.раб.':
                    dblestype = 3
                else:
                    if lestype == u'Семинар':
                        dblestype = 4
                    else:
                        dblestype = 1

        #Ищем предмет в БД или создаём новый
        try:
            subj = Subject.objects.get(subj_full=predmet)
        except Subject.DoesNotExist:
            dbSubject = Subject(
                subj_full=predmet,
                subj_short='',
            )
            dbSubject.save()
            subj = dbSubject

        #Преподаватель
        try:
            teacher = Teacher.objects.get(name=prep)
        except Teacher.DoesNotExist:
            dbTeacher = Teacher(
                name=prep,
            )
            dbTeacher.save()
            teacher = dbTeacher

        for day in days:
            dbLesson = Lesson(
                number=number,
                date=day,
                subject=subj,
                teacher=teacher,
                lesson_type=Type.objects.get(id=dblestype),
                group=Group.objects.get(id=self.id),
                auditory=audit,
            )
            dbLesson.save()
