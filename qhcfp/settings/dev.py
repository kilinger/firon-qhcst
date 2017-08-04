# -*- coding: utf-8 -*-
from .base import *


SITE_TITLE = SITE_TITLE + gettext_noop(u'(开发版)')


CACHES = {
    'default': env.cache_url(default='memcache://127.0.0.1:11211')
}


DATABASES = {
    'default': env.db_url(default='mysql://root:@127.0.0.1:3306/qhcfp')
}


MEDIA_URL = env('MEDIA_URL', default='/media/')


STATIC_URL = env('STATIC_URL', default='/static/')


INSTALLED_APPS += ('debug_toolbar', 'template_timings_panel')
DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = [env('INTERNAL_IPS', default='127.0.0.1')]
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',

    'template_timings_panel.panels.TemplateTimings.TemplateTimings',
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

