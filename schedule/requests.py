# -*- coding: utf-8 -*-
from __builtin__ import str

__author__ = 'shyr1punk'

import datetime
from schedule.models import Lesson, Faculty, Speciality, Group
import json


class GetSchedule:
    def __init__(self, group, day, month, year):
        self.group = int(group)
        self.day = int(day)
        self.month = int(month)
        self.year = int(year)

    def response(self):
        response_date = datetime.date(self.year, self.month, self.day)
        start_date = response_date - datetime.timedelta(days=response_date.weekday())
        end_date = start_date + datetime.timedelta(days=6)
        rows = Lesson.objects.filter(group_id=self.group, date__range=(start_date, end_date))
        data = [[[] for x in xrange(7)] for x in xrange(7)]
        for row in rows:
            data[row.date.weekday()][row.number - 1].append({
                'title': row.subject.subj_full,
                'teacher': row.teacher.name,
                'auditory': row.auditory.title,
                'type': row.lesson_type_id,
                'date': str(row.date),
            })
        return json.dumps(data)


class GetFaculties:
    def __init__(self):
        pass

    def response(self):
        rows = Faculty.objects.all()
        data = []
        for row in rows:
            data.append({
                'id': row.id,
                'full': row.fac_full,
                'short': row.fac_short
            })
        return json.dumps(data)


class GetSpecialities:
    def __init__(self, ID):
        self.id = int(ID)

    def response(self):
        rows = Speciality.objects.filter(faculty_id=self.id)
        data = []
        for row in rows:
            data.append({
                'id': row.id,
                'full': row.spec_full,
                'short': row.spec_short
            })
        return json.dumps(data)


class GetGroups:
    def __init__(self, ID):
        self.id = int(ID)

    def response(self):
        rows = Group.objects.filter(spec_id=self.id)
        data = []
        for row in rows:
            data.append({
                'id': row.id,
                'title': row.title
            })

        return json.dumps(data)