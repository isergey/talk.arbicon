# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import views
urlpatterns = patterns(views,
    url(r'^$', views.index , name="index"),
    url(r'^(?P<id>\d+)/$', views.show , name="show"),
    url(r'^journal/(?P<id>\d+)/$', views.journal , name="journal"),
)
