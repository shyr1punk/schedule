# -*- coding: utf-8 -*-
from __builtin__ import str

__author__ = 'shyr1punk'

import datetime
from schedule.models import Lesson, Faculty, Speciality, Group, Teacher
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
        data = {}
        for row in rows:
            if not row.date.weekday() in data:
                data[row.date.weekday()] = {}
            if not row.number - 1 in data[row.date.weekday()]:
                data[row.date.weekday()][row.number - 1] = []
            data[row.date.weekday()][row.number - 1].append({
                'title': row.subject.subj_full,
                'teacher': row.teacher.name,
                'auditory': row.auditory.title,
                'type': row.lesson_type_id,
                'date': str(row.date),
                'subGroup': row.sub_group,
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
        rows = Group.objects.filter(spec_id=self.id).order_by('course', 'group_num')
        data = []
        for row in rows:
            data.append({
                'id': row.id,
                'title': row.title
            })

        return json.dumps(data)


def get_teachers_list_json():
    rows = Teacher.objects.all()
    data = []
    for row in rows:
        data.append({
            'id': row.id,
            'name': row.name
        })
    return json.dumps(data)


def get_teachers_list():
    return Teacher.objects.order_by("name")


def get_teacher_schedule_request(teacher_id, year, month, day):
    response_date = datetime.date(int(year), int(month), int(day))
    start_date = response_date - datetime.timedelta(days=response_date.weekday())
    end_date = start_date + datetime.timedelta(days=6)
    rows = Lesson.objects.filter(teacher_id=int(teacher_id), date__range=(start_date, end_date))
    data = [[[] for x in xrange(7)] for y in xrange(6)]
    for row in rows:
        data[row.date.weekday()][row.number - 1].append({
            'title': row.subject.subj_full,
            'group': row.group.title,
            'auditory': row.auditory.title,
            'type': row.lesson_type_id,
            'date': str(row.date),
        })
    return json.dumps(data)


def get_semester_schedule_request(group):
    rows = Lesson.objects.filter(group=group)
    data = []
    for row in rows:
        data.append({
            'title': row.subject.subj_full,
            'teacher': row.teacher.name,
            'auditory': row.auditory.title,
            'type': row.lesson_type_id,
            'date': str(row.date),
            'subGroup': row.sub_group,
            'weekDay': row.date.weekday(),
            'number': row.number
        })
    return json.dumps(data)


def get_groups_list():
    rows = Group.objects.all().order_by('spec', 'course', 'group_num')
    data = []
    for row in rows:
        data.append({
            'id': row.id,
            'specId': row.spec.id,
            'facId': row.spec.faculty_id,
            'course': row.course,
            'title': row.title
        })
    return json.dumps(data)