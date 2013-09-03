# -*- coding: utf-8 -*-
__author__ = 'shyr1punk'


from schedule.models import Group, Lesson
import parser
import urllib


class Updater:
    def __init__(self):
        pass

    def getGroup(self, groupID):
        self.currentGroup = Group.objects.get(id=groupID)
        return self.currentGroup

    def getGroupsList(self):
        self.groups = Group.objects.all()
        return self.groups

    def autoUpdater(self):
        groups = self.getGroupsList()
        for group in groups:
            self.deleteGroup(group.id)
            self.parseGroup(group.id, self.getUrl(group.id))
        return 0

    def parseGroup(self, group, url):
        Lesson.objects.filter(group_id=group).delete()
        parserFile = parser.Parser(group, url)
        return parserFile.parse()

    def deleteGroup(self, groupID):
        Lesson.objects.filter(id=groupID).delete()
        return 0

    def insertGroup(self):
        return 0

    def updateGroup(self):
        #self.deleteGroup(groupID)
        self.insertGroup()

    def getUrl(self, groupID):
        group = self.getGroup(groupID)
        url = 'http://www.mstuca.ru/students/schedule/' + \
              urllib.pathname2url(group.spec.faculty.fac_full.encode('utf-8'))
        if group.spec.faculty.id != 1:
            url += '%20(' + urllib.pathname2url(group.spec.faculty.fac_short.encode('utf-8')) + ')%20'
        url += '/' + urllib.pathname2url(group.spec.spec_short.encode('utf-8') + '/' + group.title.encode('utf-8')) + '.xls'
        return url