# -*- coding: utf-8 -*-
__author__ = 'shyr1punk'


from schedule.models import Group, Lesson
import parser


class Updater:
    def __init__(self):
        pass

    def getGroup(self, groupID):
        self.currentGroup = Group.objects.get(id=groupID)
        return self.currentGroup

    def getGroupsList(self):
        self.groups = Group.objects.all()
        return self.groups

    def parseGroup(self, group, url):
        Lesson.objects.filter(group_id=group).delete()
        parserFile = parser.Parser(group, url)
        return parserFile.parse()

    def deleteGroup(self):
        Lesson.objects.filter(id=id).delete()
        return 0

    def insertGroup(self):
        return 0

    def updateGroup(self):
        self.deleteGroup()
        self.insertGroup()
