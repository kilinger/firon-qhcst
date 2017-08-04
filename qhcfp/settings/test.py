# -*- coding: utf-8 -*-
from .dev import *


BROWSER_DRIVER_NAME = env('BROWSER_DRIVER_NAME', default='django')


CACHES = {
    'default': env.cache_url(default='locmemcache://'),
}


DATABASES = {
    'default': env.db_url(default='sqlite://:memory:'),
}


DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'


PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)


INSTALLED_APPS += ('discover_runner', )
TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = root('../')
