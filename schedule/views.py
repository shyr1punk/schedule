# -*- coding: utf-8 -*-
from schedule.updater import Updater

__author__ = 'shyr1punk'

#from django.template.loader import get_template
#from django.template import Context
from django.shortcuts import render_to_response
#from django.http import HttpResponse, Http404
import updater  # Синтаксический анализатор


def updateGroups(request):
    upd = updater.Updater()
    groups = upd.getGroupsList()
    return render_to_response('updategroups.html', locals())


def insertGroup(request, groupID):
    upd = updater.Updater()
    group = upd.getGroup(groupID)
    url = group.url
    return render_to_response('insertgroup.html', locals())
