#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'accounts.views',

    url(r'^auth/login/$', 'auth_login', name="auth_login"),
    url(r'^auth/reset/password/$', 'auth_reset_password', name="auth_reset_password"),
    url(r'^auth/find/password/$', 'auth_find_password', name='auth_find_password'),
    url(r'^auth/logout/$', 'auth_logout', name='auth_logout'),
)