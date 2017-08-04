#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'message.views',

    url(r'^details/$', 'message_details', name="message_details"),
    url(r'^list/$', 'message_list', name="message_list"),
)