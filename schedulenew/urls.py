from django.conf.urls import patterns, include, url
from schedule.views import updateGroups, insertGroup, getSchedule, getJSON
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'schedulenew.views.home', name='home'),
    # url(r'^schedulenew/', include('schedulenew.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^updategroups/$', updateGroups),
    url(r'^insertGroup/id(\d{1,2})/$', insertGroup),
    url(r'^schedule/group(\d{1,2})/(\d{1,2})/(\d{1,2})/(\d{2,4})/$', getSchedule),
    url(r'^json/$', getJSON),
)

urlpatterns += staticfiles_urlpatterns()
