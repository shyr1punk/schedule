# -*- coding: utf-8 -*-
__author__ = 'shyr1punk'


from schedule.models import Group, Lesson
from BeautifulSoup import BeautifulSoup
import parser
import urllib2
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
        groups = []

        siteName = 'http://www.mstuca.ru'
        url = '/students/schedule/?content=.xls&timestamp_datesel=&timestamp_days=&timestamp_from=&timestamp_to=&doctype=acf489b4&%3FTAGS=&user_user_input=&user_user_input=&FILE_SIZE_from=&FILE_SIZE_to=&FILE_SIZE_multiply=b&WF_LOCK_STATUS=&filter=%CD%E0%E9%F2%E8&clear_filter='

        while 1:

            html = urllib2.urlopen(siteName + url)

            soup = BeautifulSoup(html)

            for link in soup.find_all(class_="element-title"):
                groups.append([link['data-bx-title'].replace('.xls', ''), link['data-bx-download']])
            nextPage = soup.find(class_='modern-page-next')
            if nextPage:
                url = nextPage.get('href')
            else:
                break
        for group in groups:
            try:
                groupId = self.findGroup(group[0].encode('utf-8'))
            except Group.DoesNotExist:
                continue
            if groupId != -1:
                self.deleteGroup(groupId)
                self.parseGroup(groupId, siteName + group[1].encode('utf-8'))

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

    def findGroup(self, groupTitle):
        try:
            group = Group.objects.get(title=groupTitle)
        except ValueError:
            return -1
        return group.id