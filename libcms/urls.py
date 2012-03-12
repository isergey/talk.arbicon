# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', include('index.urls', namespace='index')),
    (r'^core/', include('core.urls', namespace='core')),
    (r'^accounts/', include('accounts.urls', namespace='accounts')),
    (r'^pages/', include('pages.urls', namespace='pages')),

    (r'^forum/', include('forum.urls', namespace='forum')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sauth/', include('social_auth.urls')),
)
