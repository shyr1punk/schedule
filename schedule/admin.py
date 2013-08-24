# -*- coding: utf-8 -*-
__author__ = 'shyr1punk'

from django.contrib import admin
from schedule.models import Faculty, Speciality, Group, Teacher, Subject, Lesson, Type

admin.site.register(Faculty)
admin.site.register(Speciality)
admin.site.register(Group)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(Type)