from django.conf.urls import patterns, include, url
from schedule.views import dbTest, updateGroups, insertGroup

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
)
