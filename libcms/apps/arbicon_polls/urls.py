# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^', include('arbicon_polls.frontend.urls', namespace='frontend')),
#    (r'^admin/', include('pages.administration.urls', namespace='administration')),
)

