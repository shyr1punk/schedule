# -*- coding: utf-8 -*-

__author__ = 'shyr1punk'

from django.shortcuts import render_to_response
from django.http import HttpResponse#, Http404
import updater  # Синтаксический анализатор
import requests


def updateGroups(request):
    upd = updater.Updater()
    groups = upd.getGroupsList()
    return render_to_response('updategroups.html', locals())


def insertGroup(request, groupID):
    upd = updater.Updater()
    table = upd.parseGroup(groupID, upd.getUrl(groupID))
    return render_to_response('insertgroup.html', locals())


def getSchedule(request, groupID, day, month, year):
    req = requests.Response(groupID, day, month, year)
    data = req.response()
    return HttpResponse(data, content_type="application/json")


def getJSON(request):
    return render_to_response('json.html', locals())


def autoUpdater(request):
    updaterClass = updater.Updater()
    result = updaterClass.autoUpdater()
    return render_to_response('autoupdateresult.html', locals())


def index(request):
    return render_to_response('index.html')