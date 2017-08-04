#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'wechat.views',
    url(r'^openid/$', 'openid', name="openid"),
    url(r'^verification_code/$', 'verification_code', name="verification_code"),
    url(r'^bind/$', 'bind', name="bind"),
)