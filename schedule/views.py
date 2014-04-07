# -*- coding: utf-8 -*-

__author__ = 'shyr1punk'

from django.shortcuts import render_to_response
from django.http import HttpResponse#, Http404
import updater
import requests


def updateGroups(request):
    upd = updater.Updater()
    groups = upd.get_groups_list()
    return render_to_response('updategroups.html', locals())


def insert_group(request, group_id):
    upd = updater.Updater()
    table = upd.parse_group(group_id, upd.get_url(group_id))
    return render_to_response('insertgroup.html', locals())


def getSchedule(request, groupID, year, month, day):
    req = requests.GetSchedule(groupID, day, month, year)
    data = req.response()
    return HttpResponse(data, content_type="application/json")


def getJSON(request):
    return render_to_response('json.html', locals())


def autoUpdater(request):
    updaterClass = updater.Updater()
    result = updaterClass.auto_updater()
    return render_to_response('autoupdateresult.html', locals())


def index(request):
    return render_to_response('index.html')


def getFaculties(request):
    faculties = requests.GetFaculties()
    data = faculties.response()
    return HttpResponse(data, content_type="application/json")


def getSpec(request, ID):
    specialities = requests.GetSpecialities(ID)
    data = specialities.response()
    return HttpResponse(data, content_type="application/json")


def getGroups(request, ID):
    groups = requests.GetGroups(ID)
    data = groups.response()
    return HttpResponse(data, content_type="application/json")