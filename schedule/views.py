# -*- coding: utf-8 -*-

__author__ = 'shyr1punk'

#from django.template.loader import get_template
#from django.template import Context
from django.shortcuts import render_to_response
#from django.http import HttpResponse, Http404

import datetime
import xlrd


def excel_reader(request):
    """

    :param request:
    :return:
    """
    rb = xlrd.open_workbook("static/evm.xls", formatting_info=True)
    sheet = rb.sheet_by_index(0)
    rows = []
    rownum = 0
    for rownum in range(sheet.nrows):  # считываем строки Excel файла
        rows.append(sheet.row_values(rownum))
    dayofweek = ''  # текущий день недели
    week = ''  # текущая неделя (В/Н)
    lestype = ''  # тип занятия (Лекция, Пр.Зан, Лаб.раб.)
    i = 0
    find = []
    array = []

    # записываем в объединённые ячейки их значения
    for crange in sheet.merged_cells:
        rlo, rhi, clo, chi = crange
        for rowx in xrange(rlo, rhi):
            for colx in xrange(clo, chi):
                rows[rowx][colx] = rows[rlo][clo]

    # подготавливаем к записи в БД
    for i in range(1, rownum):
        # ищем занятия
        if rows[i][2] == u'Лекция' or rows[i][2] == u'Пр.Зан.' or rows[i][2] == u'Лаб.раб.':
            number = int(rows[i][0])   # номер пары
            week = rows[i][1]     # день недели
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

            daystr = u''
            for d in days:
                daystr += str(d) + '   '
            array.append([str(number), week, predmet, lestype, prep, audit, days])
            find.append(str(number) + week + predmet + lestype + prep + audit + sdays)
            find.append(daystr)

    return render_to_response('xls.html', locals())