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
    url(r'^updategroups/$', view.update_groups),
    url(r'^insertGroup/id(\d{1,4})/$', view.insert_group),
    url(r'^schedule/group(\d{1,4})/(\d{2,4})/(\d{1,2})/(\d{1,2})/$', view.get_schedule),
    url(r'^json/$', view.get_json),
    url(r'^autoupdate/$', view.auto_updater),
    url(r'^getfaculties/$', view.get_faculties),
    url(r'^getspec/faculty(\d{1,2})/$', view.get_spec),
    url(r'^getgroups/spec(\d{1,2})/$', view.get_groups),
    url(r'^$', view.index),
)

urlpatterns += staticfiles_urlpatterns()
