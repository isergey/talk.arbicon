# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^', include('accounts.frontend.urls', namespace='frontend')),
    (r'^admin/', include('accounts.administration.urls', namespace='administration')),
)

