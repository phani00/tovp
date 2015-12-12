# -*- coding: utf-8 -*-
"""
Django settings for TOVP project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from os import environ
from os.path import join, dirname

from django.core.exceptions import ImproperlyConfigured

import django_cache_url
from configurations import Configuration, values
from collections import OrderedDict


BASE_DIR = dirname(dirname(__file__))
BASE_URL = 'https://donate.tovp.org'


def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)


class Common(Configuration):

    # APP CONFIGURATION
    DJANGO_APPS = (
        # Default Django apps:
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # Useful template tags:
        # 'django.contrib.humanize',

        # Admin
        'django.contrib.admin',
    )

    THIRD_PARTY_APPS = (
        'django_jinja',
        'jinja_paginator',
        'datetimewidget',
        'reversion',
        'reversion_compare',
        'haystack',
        'hijack',
        # 'django_extensions',
    )

    # Apps specific for this project go here.
    LOCAL_APPS = (
        'ananta',
        'users',  # custom users app
        'contacts',
        'contributions',
        'promotions',
        'gifts',
        'search',
        'theme',
        'attachments',
        # Your stuff: custom apps go here
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
    # END APP CONFIGURATION

    # Flat theme needs to be loaded before admin
    INSTALLED_APPS = ('flat',) + INSTALLED_APPS

    # MIDDLEWARE CONFIGURATION
    MIDDLEWARE_CLASSES = (
        # Make sure djangosecure.middleware.SecurityMiddleware is listed first
        'djangosecure.middleware.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'audit_log.middleware.UserLoggingMiddleware',
        'reversion.middleware.RevisionMiddleware',
    )
    # END MIDDLEWARE CONFIGURATION

    # # MIGRATIONS CONFIGURATION
    MIGRATION_MODULES = {
        'sites': 'contrib.sites.migrations'
    }
    # # END MIGRATIONS CONFIGURATION

    # DEBUG
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = values.BooleanValue(False)

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
    TEMPLATE_DEBUG = DEBUG
    # END DEBUG

    # SECRET CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
    # Note: This key only used for development and testing.
    #       In production, this is changed to a values.SecretValue() setting
    SECRET_KEY = "CHANGEME!!!"
    # END SECRET CONFIGURATION

    # FIXTURE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
    FIXTURE_DIRS = (
        join(BASE_DIR, 'fixtures'),
    )
    # END FIXTURE CONFIGURATION

    # EMAIL CONFIGURATION
    EMAIL_BACKEND = values.Value('django.core.mail.backends.smtp.EmailBackend')
    # END EMAIL CONFIGURATION

    # MANAGER CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
    ADMINS = (
        ("""Prahlad Nrsimha Das (Petr Vacha) - Mayapur Media""", 'pnd@mayapurmedia.com'),
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
    MANAGERS = ADMINS
    # END MANAGER CONFIGURATION

    # DATABASE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
    DATABASES = values.DatabaseURLValue('postgres://localhost/tovp')
    # END DATABASE CONFIGURATION

    # CACHING
    # Do this here because thanks to django-pylibmc-sasl and pylibmc
    # memcacheify (used on heroku) is painful to install on windows.
    # CACHES = {
    #     'default': {
    #         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    #         'LOCATION': ''
    #     }
    # }
    CACHES = {'default': django_cache_url.config()}
    # END CACHING

    # GENERAL CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
    TIME_ZONE = 'Asia/Kolkata'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
    LANGUAGE_CODE = 'en-us'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
    SITE_ID = 1

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
    USE_I18N = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
    USE_L10N = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
    USE_TZ = None
    # END GENERAL CONFIGURATION

    # TEMPLATE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
    _TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.request',
        'ananta.context_processors.variables',
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
    TEMPLATE_DIRS = (
        join(BASE_DIR, 'theme/templates'),
        join(BASE_DIR, 'templates'),
    )

    # STATIC FILE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
    # STATIC_ROOT = join(os.path.dirname(BASE_DIR), 'staticfiles')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
    STATIC_URL = '/static/'

    # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
    STATICFILES_DIRS = (
        # join(BASE_DIR, 'static'),
    )

    # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )
    # END STATIC FILE CONFIGURATION

    # MEDIA CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
    MEDIA_ROOT = join(BASE_DIR, 'media')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
    MEDIA_URL = '/media/'
    # END MEDIA CONFIGURATION

    # URL Configuration
    ROOT_URLCONF = 'urls'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
    WSGI_APPLICATION = 'wsgi.application'
    # End URL Configuration

    # # AUTHENTICATION CONFIGURATION
    AUTHENTICATION_BACKENDS = (
        "users.backends.CaseInsensitiveModelBackend",
        "django.contrib.auth.backends.ModelBackend",
    )

    # # Custom user app defaults
    # # Select the correct user model
    AUTH_USER_MODEL = "users.User"
    LOGIN_REDIRECT_URL = "users:redirect"
    LOGIN_URL = "users:login"
    # # END Custom user app defaults

    # SLUGLIFIER
    AUTOSLUG_SLUGIFY_FUNCTION = "slugify.slugify"
    # END SLUGLIFIER

    TEMPLATES = [
        {
            "BACKEND": "django_jinja.backend.Jinja2",
            "APP_DIRS": True,
            "OPTIONS": {
                "match_extension": ".jinja",
                "extensions": [
                    "jinja2.ext.do",
                    "jinja2.ext.loopcontrols",
                    "jinja2.ext.with_",
                    "jinja2.ext.i18n",
                    "jinja2.ext.autoescape",
                    "django_jinja.builtins.extensions.CsrfExtension",
                    "django_jinja.builtins.extensions.CacheExtension",
                    "django_jinja.builtins.extensions.TimezoneExtension",
                    "django_jinja.builtins.extensions.UrlsExtension",
                    "django_jinja.builtins.extensions.StaticFilesExtension",
                    "django_jinja.builtins.extensions.DjangoFiltersExtension",
                    'ananta.templatetags.jinja2.core',
                    'attachments.templatetags.jinja2.attachments',
                    'promotions.templatetags.jinja2.promotions',
                ],
                "context_processors": _TEMPLATE_CONTEXT_PROCESSORS,
                "constants": {
                    "BASE_URL": BASE_URL,
                },
            }
        },
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": ['templates'],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": _TEMPLATE_CONTEXT_PROCESSORS,
                "debug": DEBUG,
                # 'loaders': [
                #     'django.template.loaders.filesystem.Loader',
                #     'django.template.loaders.app_directories.Loader',
                # ]
            },
        },
    ]

    # LOGGING CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
    # A sample logging configuration. The only tangible logging
    # performed by this configuration is to send an email to
    # the site admins on every HTTP 500 error when DEBUG=False.
    # See http://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.
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
    # END LOGGING CONFIGURATION

    ABSOLUTE_DOMAIN = '//donate.tovp.org'

    # Your common stuff: Below this line define 3rd party library settings
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.'
            'ElasticsearchSearchEngine',
            'URL': get_env_variable('ELASTICSEARCH_SERVER'),
            'INDEX_NAME': get_env_variable('ELASTICSEARCH_INDEX_NAME'),
        },
    }
    HAYSTACK_SIGNAL_PROCESSOR = 'search.signals.RelatedRealtimeSignalProcessor'
    HAYSTACK_DEFAULT_OPERATOR = 'AND'

    SHOW_HIJACKUSER_IN_ADMIN = False
    HIJACK_LOGIN_REDIRECT_URL = "/"

    AJAX_LOOKUP_CHANNELS = {
        'person': ('contacts.lookups', 'PersonLookup'),
        'bulk_payment': ('contributions.lookups', 'BulkPaymentLookup'),
    }

    ENABLED_CURRENCIES = OrderedDict((
        ('INR', {'word': 'rupees',
                 'symbol': '₹ (INR)'}),
        ('USD', {'word': 'american dollars',
                 'symbol': '$ (USD)'}),
        ('EUR', {'word': 'euro',
                 'symbol': '€ (EUR)'}),
        ('GBP', {'word': 'british pounds',
                 'symbol': '£ (GBP)'}),
        ('CAD', {'word': 'canadian dollars',
                 'symbol': 'C$ (CAD)'}),
        ('RUB', {'word': 'russian ruble',
                 'symbol': '₽ (RUB)'}),
    ))

    FOREIGN_CURRENCIES = OrderedDict((
        ('USD', {'word': 'american dollars',
                 'symbol': 'American Dollar $ (USD)'}),
        ('EUR', {'word': 'euro',
                 'symbol': 'Euro € (EUR)'}),
        ('GBP', {'word': 'british pounds',
                 'symbol': 'British Pounds £ (GBP)'}),
        ('CAD', {'word': 'canadian dollars',
                 'symbol': 'Canadian Dollar C$ (CAD)'}),
        ('RUB', {'word': 'russian ruble',
                 'symbol': 'Russian Ruble ₽ (RUB)'}),
        ('AUD', {'word': 'australian dollars',
                 'symbol': 'Australian Dollar A$ (AUD)'}),
        ('CNY', {'word': 'chinese yuan',
                 'symbol': 'Chinese Yuan ¥ (CNY)'}),
        ('JPY', {'word': 'yapanese yen',
                 'symbol': 'Japanase Yen ¥ (JPY)'}),
        ('THB', {'word': 'thai baht',
                 'symbol': 'Thai Baht ฿ (THB)'}),
        ('SGD', {'word': 'singaporean dollar',
                 'symbol': 'Singaporean Dollar S$ (SGD)'}),
        ('MYR', {'word': 'malaysian ringgit',
                 'symbol': 'Malaysian Ringgit RM (MYR)'}),
        ('ZAR', {'word': 'south african rand',
                 'symbol': 'South African Rand R (ZAR)'}),
    ))
