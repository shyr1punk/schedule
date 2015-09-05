# -*- coding: utf-8 -*-

__author__ = 'shyr1punk'

from django.shortcuts import render_to_response
from django.http import HttpResponse

from schedule_app.updater import Updater
from schedule_app import requests


def update_groups(request):
    upd = Updater()
    urls = upd.get_xls_files_url()
    return render_to_response('updategroups.html', locals())


def insert_group(request, group_id):
    upd = Updater()
    table = upd.parse_group(group_id, upd.get_url(group_id))
    return render_to_response('insertgroup.html', locals())


def get_schedule(request, group_id, year, month, day):
    req = requests.GetSchedule(group_id, day, month, year)
    data = req.response()
    return HttpResponse(data, content_type="application/json")


def get_json(request):
    return render_to_response('json.html', locals())


def auto_updater(request):
    upd = Updater()
    result = upd.get_groups_list()
    return render_to_response('autoupdateresult.html', locals())


def index(request):
    teachers_list = requests.get_teachers_list()
    return render_to_response('index.html', locals())


def get_faculties(request):
    faculties = requests.GetFaculties()
    data = faculties.response()
    return HttpResponse(data, content_type="application/json")


def get_spec(request, faculty_id):
    specialities = requests.GetSpecialities(faculty_id)
    data = specialities.response()
    return HttpResponse(data, content_type="application/json")


def get_groups(request, speciality_id):
    groups = requests.GetGroups(speciality_id)
    data = groups.response()
    return HttpResponse(data, content_type="application/json")


def get_teachers_list(request):
    return HttpResponse(requests.get_teachers_list_json(), content_type="application/json")


def get_teacher_schedule(request, teacher_id, year, month, day):
    return HttpResponse(requests.get_teacher_schedule_request(teacher_id, year, month, day), content_type="application/json")


def get_semester_schedule(request, group):
    return HttpResponse(requests.get_semester_schedule_request(group), content_type="application/json")


def get_groups_list(request):
    return HttpResponse(requests.get_groups_list(), content_type="application/json")
