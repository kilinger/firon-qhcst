# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'regist.views.regist_index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('accounts.urls')),
    url(r'^regist/', include('regist.urls')),
    url(r'^member/', include('member.urls')),
    url(r'^message/', include('message.urls')),
    url(r'^wechat/', include('wechat.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^i18n/setlang/$', 'django.views.i18n.set_language', name='set_language'),
)


from django.conf import settings

if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns

    from django.views.generic import TemplateView
    urlpatterns += patterns('',
        url(r'', include('doodoll_kit.magicpages.urls')),
        url(r'^$', TemplateView.as_view(template_name='index.html')),
    )


if 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
