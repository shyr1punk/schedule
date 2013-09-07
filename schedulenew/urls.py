from django.conf.urls import patterns, include, url
import schedule.views as view
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
    url(r'^updategroups/$', view.updateGroups),
    url(r'^insertGroup/id(\d{1,3})/$', view.insertGroup),
    url(r'^schedule/group(\d{1,2})/(\d{2,4})/(\d{1,2})/(\d{1,2})/$', view.getSchedule),
    url(r'^json/$', view.getJSON),
    url(r'^autoupdate/$', view.autoUpdater),
    url(r'^getfaculties/$', view.getFaculties),
    url(r'^getspec/faculty(\d{1,2})/$', view.getSpec),
    url(r'^getgroups/spec(\d{1,2})/$', view.getGroups),
    url(r'^$', view.index),
)

urlpatterns += staticfiles_urlpatterns()
