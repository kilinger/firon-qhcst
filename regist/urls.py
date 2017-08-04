#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'regist.views',
    url(r'^index/$', 'regist_index', name="regist_index"),
    url(r'^info_basis/$', 'regist_info_basis', name="regist_info_basis"),
    url(r'^info_demand/$', 'regist_info_demand', name="regist_info_demand"),
    url(r'^info_educate/$', 'regist_info_educate', name="regist_info_educate"),
    url(r'^info_occupation/$', 'regist_info_occupation', name="regist_info_occupation"),#创业
    url(r'^info_previews/$', 'regist_info_preview', name="regist_info_preview"),
    url(r'^finish/$', 'regist_finish', name="regist_finish"),

    url(r'^edit/info_basis/$', 'edit_info_basis', name="edit_info_basis"),
    url(r'^edit/info_educate/$', 'edit_info_educate', name="edit_info_educate"),
    url(r'^edit/info_occupation/$', 'edit_info_occupation', name="edit_info_occupation"),
    url(r'^edit/info_demand/$', 'edit_info_demand', name="edit_info_demand"),
)