#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'member.views',

    url(r'^$', 'member_index', name='member_index'),
    url(r'^upload/$', 'member_upload_excel', name='member_upload_excel'),
    url(r'^details/$', 'member_details', name="member_details"),
    url(r'^list/$', 'member_list', name="member_list"),
    url(r'^attention/$', 'member_attention', name='member_attention'),
    url(r'^examine/$', 'member_examine', name='member_examine'),
)