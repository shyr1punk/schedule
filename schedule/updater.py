# -*- coding: utf-8 -*-
__author__ = 'shyr1punk'

from datetime import datetime
from schedule.models import Group, Lesson, Speciality
from bs4 import BeautifulSoup
import parser
import urllib2


class Updater:
    def __init__(self):
        pass

    @staticmethod
    def get_group(group_id):
        return Group.objects.get(id=group_id)

    @staticmethod
    def get_groups_list():
        return Group.objects.all()

    def auto_updater(self):
        groups = []

        site_name = 'http://www.mstuca.ru'
        url = site_name + '/students/schedule/?content=.xls&timestamp_datesel=&timestamp_days=&timestamp_from=' \
            '&timestamp_to=&doctype=acf489b4&%3FTAGS=&user_user_input=&user_user_input=&FILE_SIZE_from=&FILE_SIZE_to=' \
            '&FILE_SIZE_multiply=b&WF_LOCK_STATUS=&filter=%CD%E0%E9%F2%E8&clear_filter='

        while 1:

            html = BeautifulSoup(urllib2.urlopen(url))

            for link in html.find_all(class_='element-title'):
                groups.append([link['data-bx-title'].encode('utf-8').replace('.xls', ''),
                               link['data-bx-src'].encode('utf-8').replace('?showInViewer=1', '')])
            next_page = html.find(class_='modern-page-next')
            if next_page:
                url = site_name + next_page.get('href')
            else:
                break
        for group in groups:
            group_id = self.find_group(group[0])
            if group_id != -1:
                self.parse_group(group_id, group[1])
            else:
                Group(
                    title=group[0],
                    course=self.detect_course(group[1]),
                    spec=Speciality.objects.get(id=self.detect_spec(group[1])),
                    updated=datetime.now(),
                    link=group[1],
                ).save()

        return 0

    @staticmethod
    def parse_group(group_id, url):
        Lesson.objects.filter(group_id=group_id).delete()
        return parser.Parser(group_id, url).parse()

    @staticmethod
    def find_group(group_title):
        try:
            group = Group.objects.get(title=group_title)
        except Group.DoesNotExist:
            return -1
        return group.id

    @staticmethod
    def detect_spec(url):
        if url.find('/М/') != -1:
            return 1
        if url.find('/БТП/') != -1:
            return 2
        if url.find('/УВД/') != -1:
            return 3
        if url.find('/АК/') != -1:
            return 4
        if url.find('/РС/') != -1:
            return 5
        if url.find('/ОП/') != -1:
            return 6
        if url.find('/ЭК/') != -1:
            return 7
        if url.find('/СО/') != -1:
            return 8
        if url.find('/ПМ/') != -1:
            return 9
        if url.find('/ЭВМ/') != -1:
            return 10
        if url.find('/БИ/') != -1:
            return 11

    @staticmethod
    def detect_course(url):
        return int(url[url.find('-') - 1])

    @staticmethod
    def get_url(group_id):
        return Group.objects.get(id=group_id).link