# -*- coding: utf-8 -*-
from __builtin__ import str

__author__ = 'shyr1punk'

import datetime
from schedule_app.models import Lesson, Faculty, Speciality, Group, Teacher
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


def get_faculties():
    rows = Faculty.objects.all()
    data = []
    for row in rows:
        data.append({
            'id': row.id,
            'full': row.fac_full,
            'short': row.fac_short
        })
    return data


def get_specialities(faculty_id):
    if faculty_id == None:
        rows = Speciality.objects.all()
    else:
        rows = Speciality.objects.filter(faculty_id=faculty_id)
    data = []
    for row in rows:
        data.append({
            'id': row.id,
            'full': row.spec_full,
            'short': row.spec_short,
            'facultyId': row.faculty_id
        })
    return data



def get_groups(speciality_id):
    if speciality_id == None:
        rows = Group.objects.all().order_by('spec', 'course', 'group_num')
    else:
        rows = Group.objects.filter(spec_id=speciality_id).order_by('course', 'group_num')
    data = []
    for row in rows:
        data.append({
            'id': row.id,
            'title': row.title,
            'specialityId': row.spec.id
        })
    return data


def get_teachers_list():
    rows = Teacher.objects.all().order_by("name")
    data = []
    for row in rows:
        data.append({
            'id': row.id,
            'name': row.name
        })
    return data


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
