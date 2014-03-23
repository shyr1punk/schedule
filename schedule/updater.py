# -*- coding: utf-8 -*-
__author__ = 'shyr1punk'


from schedule.models import Group, Lesson
from bs4 import BeautifulSoup
import parser
import urllib2


class Updater:
    def __init__(self):
        pass

    def get_group(self, group_id):
        self.current_group = Group.objects.get(id=group_id)
        return self.current_group

    def get_groups_list(self):
        self.groups = Group.objects.all()
        return self.groups

    def auto_updater(self):
        groups = []

        site_name = 'http://www.mstuca.ru'
        url = '/students/schedule/?content=.xls&timestamp_datesel=&timestamp_days=&timestamp_from=&timestamp_to=&doctype=acf489b4&%3FTAGS=&user_user_input=&user_user_input=&FILE_SIZE_from=&FILE_SIZE_to=&FILE_SIZE_multiply=b&WF_LOCK_STATUS=&filter=%CD%E0%E9%F2%E8&clear_filter='

        while 1:

            html = urllib2.urlopen(site_name + url)

            soup = BeautifulSoup(html)

            for link in soup.find_all(class_="element-title"):
                groups.append([link['data-bx-title'].replace('.xls', ''), link['data-bx-download']])
            next_page = soup.find(class_='modern-page-next')
            if next_page:
                url = next_page.get('href')
            else:
                break
        for group in groups:
            try:
                group_id = self.find_group(group[0].encode('utf-8'))
            except Group.DoesNotExist:
                continue
            if group_id != -1:
                self.delete_group(group_id)
                self.parse_group(group_id, site_name + group[1].encode('utf-8'))

        return 0

    def parse_group(self, group, url):
        Lesson.objects.filter(group_id=group).delete()
        parserFile = parser.Parser(group, url)
        return parserFile.parse()

    def delete_group(self, group_id):
        Lesson.objects.filter(id=group_id).delete()
        return 0

    def insert_group(self):
        return 0

    def update_group(self):
        self.insert_group()

    def find_group(self, group_title):
        try:
            group = Group.objects.get(title=group_title)
        except ValueError:
            return -1
        return group.id