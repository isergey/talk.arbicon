# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
urlpatterns = patterns('accounts.frontend.views',
    url(r'^$', 'index', name="index"),
)

urlpatterns += patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/frontend/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^password/change/$', 'django.contrib.auth.views.password_change', name='password_change'),
    url(r'^password/change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset',
        {
            'template_name': 'accounts/frontend/registration/password_reset_form.html',
            'email_template_name': 'accounts/frontend/registration/password_reset_email.html',
            'post_reset_redirect': 'accounts/password/reset/done/'
        },
        name='password_reset'
    ),
    url(r'^password/reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        {
            'template_name': 'accounts/frontend/registration/password_reset_done.html',
        },
        name='password_reset_done'
    ),
    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        {
            'template_name': 'frontend/registration/password_reset_confirm.html',
            'post_reset_redirect': '/accounts/password/reset/complete/'
        },
        name='password_reset_confirm'
    ),
    url(r'^password/reset/complete/$',
        'django.contrib.auth.views.password_reset_complete',
        {
            'template_name': 'accounts/frontend/registration/password_reset_complete.html',
        },
        name='password_reset_complete'),
)

