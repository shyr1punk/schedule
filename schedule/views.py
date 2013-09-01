# -*- coding: utf-8 -*-

__author__ = 'shyr1punk'

from django.shortcuts import render_to_response
from django.http import HttpResponse#, Http404
import updater  # Синтаксический анализатор
import urllib
import requests


def updateGroups(request):
    upd = updater.Updater()
    groups = upd.getGroupsList()
    return render_to_response('updategroups.html', locals())


def insertGroup(request, groupID):
    upd = updater.Updater()
    group = upd.getGroup(groupID)
    upd = updater.Updater()
    url = 'http://www.mstuca.ru/students/schedule/' +\
          urllib.pathname2url(group.spec.faculty.fac_full.encode('utf-8'))
    if group.spec.faculty.id != 1:
        url += '%20(' + urllib.pathname2url(group.spec.faculty.fac_short.encode('utf-8')) + ')%20'
    url += '/' + urllib.pathname2url(group.spec.spec_short.encode('utf-8') + '/' + group.title.encode('utf-8')) + '.xls'
    table = upd.parseGroup(group.id, url)
    return render_to_response('insertgroup.html', locals())


def getSchedule(request, groupID, day, month, year):
    req = requests.Response(groupID, day, month, year)
    data = req.response()
    return HttpResponse(data, content_type="application/json")


def getJSON(request):
    return render_to_response('json.html', locals())