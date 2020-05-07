#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ==============================================================================
#
#       File Name : letsconfig.py
#
#       Creation Date : Fri 01 May 2020 09:01:10 PM EEST (21:01)
#
#       Last Modified : Sun 03 May 2020 02:12:03 PM EEST (14:12)
#
# ==============================================================================

import os
import random

from configobj import ConfigObj
from django.core.exceptions import ImproperlyConfigured
from importlib import import_module


class Config:
    def __init__(
        self,
        config_path,
        default_module,
        cache_path=None,
        celery=False,
        email_backend=None,
        project_path=None,
        log_path=None,
        media_root=None,
        static_path=None,
        static_root=None,
        project_template_dir=None,
        timezone="Europe/Athens",
        configuration_name=None,
        db_password=None,
        db_user=None,
        db_name=None,
        db_engine=None,
    ):
        if os.path.exists(config_path):
            raise ImproperlyConfigured(
                "Configuration file '{0}', already exists".format(config_path)
            )
        config = ConfigObj()
        config.filename = config_path
        config.indent_type = "    "
        config.interpolation = False
        config.unrepr = True
        self.config = config
        self.defaults = default_module
        self.cache_path = cache_path or os.environ.get("DJANGO_CACHE_PATH")
        self.include_celery = False
        self.email_backend = (
            email_backend or "django.core.mail.backends.console.EmailBackend"
        )
        self.project_path = project_path or os.environ.get("DJANGO_PROJECT_PATH")
        self.project_name = self.project_path.split(os.sep)[-1]
        self.log_path = log_path or os.environ.get("DJANGO_LOG_PATH")
        self.media_root = media_root or os.environ.get("DJANGO_MEDIA_ROOT")
        self.static_path = static_path or os.environ.get("DJANGO_STATIC_PATH")
        self.static_root = static_root or os.environ.get("DJANGO_STATIC_ROOT")
        self.project_template_dir = project_template_dir or os.environ.get(
            "DJANGO_PROJECT_TEMPLATES_PATH"
        )
        self.timezone = timezone
        self.configuration_name = configuration_name or os.environ.get(
            "DJANGO_CONFIGURATION_DESC"
        )
        self.db_password = db_password or os.environ.get("DEFAULT_DATABASE_PASSWORD")
        self.db_user = db_user or os.environ.get("DEFAULT_DATABASE_USER")
        self.db_name = db_name or os.environ.get("DEFAULT_DATABASE_NAME")
        self.db_engine = db_engine or os.environ.get("DATABASE_ENGINE")
        if not all(
            (
                self.cache_path,
                self.email_backend,
                self.project_path,
                self.project_name,
                self.log_path,
                self.media_root,
                self.static_path,
                self.static_root,
                self.project_template_dir,
                self.configuration_name,
                self.db_password,
                self.db_user,
                self.db_name,
                self.db_engine,
            )
        ):
            raise ImproperlyConfigured(
                "You did not enter a value for {0}".format(
                    ",".join(
                        [
                            str(x)
                            for x, val in enumerate(
                                (
                                    self.cache_path,  # 0
                                    self.email_backend,  # 1
                                    self.project_path,  # 2
                                    self.project_name,  # 3
                                    self.log_path,  # 4
                                    self.media_root,  # 5
                                    self.static_path,  # 6
                                    self.static_root,  # 7
                                    self.project_template_dir,  # 8
                                    self.configuration_name,  # 9
                                    self.db_password,  # 10
                                    self.db_user,  # 11
                                    self.db_name,  # 12
                                    self.db_engine,  # 13
                                )
                            )
                            if not val
                        ]
                    )
                )
            )

    def build(self):
        module = import_module(self.defaults)
        for key, value in module.__dict__.items():
            if key.isupper():
                self.config.update({key: value})

        self.config.update(
            {
                "ADMINS": [("George", "tantiras@yandex.com")],
                "ALLOWED_HOSTS": ["127.0.0.1", "localhost"],
                "AUTH_USER_MODEL": "people.User",
                "BASE_DIR": self.project_path,
                "CACHES": {
                    "default": {
                        "BACKEND": "diskcache.DjangoCache",
                        "LOCATION": self.cache_path,
                        "SHARDS": 8,
                        "DATABASE_TIMEOUT": 1.0,
                        "TIMEOUT": 43200,
                        "VERSION": 1,
                        "OPTIONS": {
                            "size_limit": 4294967296,
                            "MAX_ENTRIES": 15000,
                            "CULL_FREQUENCY": 3,
                        },
                    }
                },
                "DATABASES": {
                    "default": {
                        "NAME": self.db_name,
                        "USER": self.db_user,
                        "PASSWORD": self.db_password,
                        "HOST": "localhost",
                        "PORT": 5432,
                        "CONN_MAX_AGE": 0,
                        "ENGINE": self.db_engine,
                        "ATOMIC_REQUESTS": False,
                        "AUTOCOMMIT": True,
                        "OPTIONS": {},
                        "TIME_ZONE": None,
                        "TEST": {
                            "CHARSET": None,
                            "COLLATION": None,
                            "NAME": None,
                            "MIRROR": None,
                        },
                    }
                },
                "DEBUG": False,
                "EMAIL_BACKEND": self.email_backend,
                "FORMAT_MODULE_PATH": "{0}.formats".format(
                    os.environ.get("DJANGO_PROJECT")
                ),
                "INSTALLED_APPS": [
                    "django.contrib.admin",
                    "django.contrib.auth",
                    "django.contrib.contenttypes",
                    "django.contrib.sessions",
                    "django.contrib.messages",
                    "django.contrib.staticfiles",
                    "people.apps.PeopleConfig",
                ],
                "INTERNAL_IPS": ("127.0.0.1", "localhost"),
                "LANGUAGES": [("en", "English"), ("el", "Greek")],
                "LANGUAGE_CODE": "en",
                "LOCALE_PATHS": [os.path.join(self.project_path, "00", "locale")],
                "LOGGING": {
                    "version": 1,
                    "disable_existing_loggers": False,
                    "formatters": {
                        "verbose": {
                            "format": "{levelname} {asctime} {process:d} {thread:d} {name} {lineno} {message}",
                            "style": "{",
                        },
                        "simple": {
                            "format": "{levelname} {name} {lineno} {message}",
                            "style": "{",
                        },
                    },
                    "filters": {
                        "require_debug_false": {
                            "()": "django.utils.log.RequireDebugFalse"
                        },
                        "require_debug_true": {
                            "()": "django.utils.log.RequireDebugTrue"
                        },
                    },
                    "handlers": {
                        "console": {
                            "level": "INFO",
                            "filters": ["require_debug_true"],
                            "class": "logging.StreamHandler",
                            "formatter": "simple",
                        },
                        "file": {
                            "level": "ERROR",
                            "filters": ["require_debug_false"],
                            "class": "logging.FileHandler",
                            "filename": os.path.join(self.log_path, "django.log"),
                            "formatter": "verbose",
                        },
                        "celery.file": {
                            "level": "INFO",
                            "filters": ["require_debug_false"],
                            "class": "logging.FileHandler",
                            "filename": os.path.join(self.log_path, "celery.log"),
                        },
                    },
                    "loggers": {
                        "config_placeholder": {
                            "handlers": ["file", "console"],
                            "level": "INFO",
                            "propagate": True,
                        },
                        "django": {
                            "handlers": ["file", "console"],
                            "level": "INFO",
                            "propagate": True,
                        },
                        "celery": {
                            "handlers": ["celery.file", "console"],
                            "level": "INFO",
                            "propagate": False,
                        },
                    },
                },
                "MANAGERS": [("George", "tantiras@yandex.com")],
                "MEDIA_ROOT": self.media_root,
                "MEDIA_URL": "/media/",
                "MIDDLEWARE": [
                    "debug_toolbar.middleware.DebugToolbarMiddleware",
                    "django.middleware.security.SecurityMiddleware",
                    "django.middleware.http.ConditionalGetMiddleware",
                    "django.contrib.sessions.middleware.SessionMiddleware",
                    "django.middleware.locale.LocaleMiddleware",
                    "django.middleware.common.CommonMiddleware",
                    "django.middleware.csrf.CsrfViewMiddleware",
                    "django.contrib.auth.middleware.AuthenticationMiddleware",
                    "django.contrib.messages.middleware.MessageMiddleware",
                    "django.middleware.clickjacking.XFrameOptionsMiddleware",
                    "django.contrib.sites.middleware.CurrentSiteMiddleware",
                ],
                "PASSWORD_HASHERS": [
                    "django.contrib.auth.hashers.Argon2PasswordHasher",
                    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
                    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
                    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
                ],
                "ROOT_URLCONF": "{0}.urls".format(self.project_name),
                "SECRET_KEY": "".join(
                    random.SystemRandom().choice(
                        "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
                    )
                    for _ in range(75)
                ),
                "SESSION_EXPIRE_AT_BROWSER_CLOSE": True,
                "SITE_ID": 1,
                "STATICFILES_DIRS": [self.static_path],
                "STATIC_ROOT": self.static_root,
                "STATIC_URL": "/static/",
                "TEMPLATES": [
                    {
                        "BACKEND": "django.template.backends.django.DjangoTemplates",
                        "DIRS": [self.project_template_dir],
                        "APP_DIRS": True,
                        "OPTIONS": {
                            "context_processors": [
                                "django.template.context_processors.debug",
                                "django.template.context_processors.request",
                                "django.contrib.auth.context_processors.auth",
                                "django.contrib.messages.context_processors.messages",
                                "django.template.context_processors.i18n",
                                "django.template.context_processors.media",
                                "django.template.context_processors.static",
                                "django.template.context_processors.tz",
                            ]
                        },
                    }
                ],
                "TIME_ZONE": self.timezone,
                "USE_L10N": True,
                "USE_TZ": True,
                "WSGI_APPLICATION": "{0}.wsgi.application".format(self.project_name),
            }
        )
        if self.configuration_name != "Prod":
            self.config["INSTALLED_APPS"].append("debug_toolbar")
            self.config["DEBUG"] = True
        else:
            self.config.update(
                {
                    "CSRF_COOKIE_HTTPONLY": True,
                    "CSRF_COOKIE_SECURE": True,
                    "EMAIL_USE_TLS": True,
                    "PREPEND_WWW": False,
                    "SECURE_BROWSER_XSS_FILTER": True,
                    "SECURE_CONTENT_TYPE_NOSNIFF": True,
                    "SECURE_HSTS_INCLUDE_SUBDOMAINS": True,
                    "SECURE_HSTS_PRELOAD": True,
                    "SECURE_HSTS_SECONDS": 31536000,
                    "SECURE_SSL_REDIRECT": True,
                    "SESSION_COOKIE_AGE": 43200,
                    "SESSION_COOKIE_SECURE": True,
                    "X_FRAME_OPTIONS": "DENY",
                }
            )

        if self.include_celery:
            self.config.update(
                {
                    "BROKER_CONNECTION_TIMEOUT": 30,
                    "BROKER_HEARTBEAT": None,
                    "BROKER_POOL_LIMIT": 1,
                    "BROKER_USE_SSL": True,
                    "CELERYBEAT_SCHEDULER": "djcelery.schedulers.DatabaseScheduler",
                    "CELERYD_CONCURRENCY": 50,
                    "CELERYD_PREFETCH_MULTIPLIER": 1,
                    "CELERYD_TASK_SOFT_TIME_LIMIT": 60,
                    "CELERY_ACCEPT_CONTENT": ["json"],
                    "CELERY_BROKER_URL": None,
                    "CELERY_ENABLE_UTC": False,
                    "CELERY_EVENT_QUEUE_EXPIRES": 60,
                    "CELERY_RESULT_BACKEND": "rpc",
                    "CELERY_RESULT_SERIALIZER": "json",
                    "CELERY_SEND_EVENTS": False,
                    "CELERY_SEND_TASK_ERROR_EMAILS": True,
                    "CELERY_TASK_SERIALIZER": "json",
                    "CELERY_TIMEZONE": "Europe/Athens",
                }
            )
        self.config.write()
