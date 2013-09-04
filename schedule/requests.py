# -*- coding: utf-8 -*-
from __builtin__ import str

__author__ = 'shyr1punk'

import datetime
from schedule.models import Lesson
import json


class Response:
    def __init__(self, group, day, month, year):
        self.group = int(group)
        self.day = int(day)
        self.month = int(month)
        self.year = int(year)

    def response(self):
        start_date = datetime.date(self.year, self.month, self.day)
        end_date = start_date + datetime.timedelta(days=7)
        rows = Lesson.objects.filter(group_id=self.group, date__range=(start_date, end_date))
        data = []
        for row in rows:
            data.append({
                'number': row.number,
                'title': row.subject.subj_full,
                'teacher': row.teacher.name,
                'auditory': row.auditory.title,
                'type': row.lesson_type.type_full,
                'date': str(row.date),
            })

        return json.dumps(data)