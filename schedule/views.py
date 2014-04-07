# -*- coding: utf-8 -*-

__author__ = 'shyr1punk'

from django.shortcuts import render_to_response
from django.http import HttpResponse
import updater
import requests


def update_groups(request):
    upd = updater.Updater()
    groups = upd.get_groups_list()
    return render_to_response('updategroups.html', locals())


def insert_group(request, group_id):
    upd = updater.Updater()
    table = upd.parse_group(group_id, upd.get_url(group_id))
    return render_to_response('insertgroup.html', locals())


def get_schedule(request, group_id, year, month, day):
    req = requests.GetSchedule(group_id, day, month, year)
    data = req.response()
    return HttpResponse(data, content_type="application/json")


def get_json(request):
    return render_to_response('json.html', locals())


def auto_updater(request):
    updater_class = updater.Updater()
    result = updater_class.auto_updater()
    return render_to_response('autoupdateresult.html', locals())


def index(request):
    return render_to_response('index.html')


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