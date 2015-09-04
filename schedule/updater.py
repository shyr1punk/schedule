# -*- coding: utf-8 -*-
from datetime import datetime
from schedule.models import Group, Lesson, Speciality
from bs4 import BeautifulSoup
import parser
import urllib2
from django.utils.encoding import iri_to_uri
from django.utils.http import urlquote
import re


class Updater:
    def __init__(self):
        self.specialities = Speciality.objects.all()
        self.xls_files_page_urls = []
        self.groups = []
        self.site_name = 'http://mstuca.ru'

    @staticmethod
    def get_absolute_url(url):
        return iri_to_uri(urlquote(url))

    def get_xls_files_page_urls(self):
        base_url = '/students/schedule/'
        for speciality in self.specialities:
            if speciality.faculty.id == 1:
                faculty_url = speciality.faculty.fac_full
            else:
                faculty_url = speciality.faculty.fac_full + " (" + speciality.faculty.fac_short + ")"
            page_url = base_url + faculty_url + '/' + speciality.spec_short
            self.xls_files_page_urls.append({
                'url': page_url,
                'spec_id': speciality.id,
                'faculty_id': speciality.faculty_id
            })
        return self.xls_files_page_urls

    def get_xls_files_url(self):
        for xls_files_page in self.get_xls_files_page_urls():
            self.parse_schedule_html_page(xls_files_page)

    @staticmethod
    def get_group(group_id):
        return Group.objects.get(id=group_id)

    def get_groups_list(self):
        self.get_xls_files_url()
        return self.groups

    def parse_schedule_html_page(self, xls_files_page):
        url = xls_files_page['url']

        while 1:
            absolute_url = self.site_name + self.get_absolute_url(url)
            html = BeautifulSoup(urllib2.urlopen(absolute_url))
            for link in html.find_all(class_='element-title'):
                if re.search('.xls', link['data-bx-title'].encode('utf-8')):
                    self.groups.append({
                        'title': link['data-bx-title'].encode('utf-8').replace('.xls', ''),
                        'url': link['data-bx-src'].encode('utf-8').replace('?showInViewer=1', '')
                    })
            next_page = html.find(class_='modern-page-next')
            if next_page:
                url = self.site_name + next_page.get('href')
            else:
                break
    pass
    # for group in groups:
    #     group_id = self.find_group(group[0])
    #     if group_id != -1:
    #         self.parse_group(group_id, group[1])
    #     else:
    #         Group(
    #             title=group[0],
    #             course=self.detect_course(group[1]),
    #             group_num=self.detect_group(group[1]),
    #             spec=Speciality.objects.get(id=self.detect_spec(group[1])),
    #             updated=datetime.now(),
    #             link=group[1],
    #         ).save()
    #
    # return 0

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
    def detect_group(url):
        return int(url[url.find('-') + 1])

    @staticmethod
    def get_url(group_id):
        return Group.objects.get(id=group_id).link