"""
Django settings for spokanetech project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
import sys
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


ENV_PATH = os.environ.get("ENV_PATH", f"{BASE_DIR.parent}/envs/.env.local")
# now load the contents of the defined .env file
env = environ.Env()
if os.path.exists(ENV_PATH):
    print(f"loading ENV vars from {ENV_PATH}")
    environ.Env.read_env(ENV_PATH)
else:
    print("NO ENV_PATH found!")  # pragma: no cover


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY", "default_key-this_is_insecure_and_should_be_changed")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", True)

ALLOWED_HOSTS = env.str("ALLOWED_HOSTS", "127.0.0.1").split(",")
INTERNAL_IPS = env.str("INTERNAL_IPS", "127.0.0.1").split(",")


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party apps
    "debug_toolbar",
    "django_extensions",
    "django_filters",
    "handyhelpers",
    # project apps
    "web",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.PstTimezoneMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "core", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "handyhelpers.context_processors.get_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env.str("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": env.str("DB_NAME", os.path.join(BASE_DIR, "db.sqlite3")),
        "TEST_NAME": env.str("DB_TEST_NAME", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": env.str("DB_USER", "core"),
        "PASSWORD": env.str("DB_PASSWORD", "core"),
        "HOST": env.str("DB_HOST", "localhost"),
        "PORT": env.str("DB_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(str(BASE_DIR), "staticroot")
STATIC_URL = "/static/"

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (os.path.join(str(BASE_DIR), "core/static"),)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


BASE_TEMPLATE = "base.htm"
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/userextensions/user_login_redirect"
LOGIN_REDIRECT_URL_DEFAULT = "/"
SESSION_COOKIE_AGE = env.int("SESSION_COOKIE_AGE", 28800)
SKIP_FIXED_URL_LIST = ["/userextensions/list_recents/", "/userextensions/user_login_redirect/", "/"]
REQUIRED_LOGIN_IGNORE_PATHS = [
    "/accounts/login/",
    "/accounts/logout/",
    "/logout",
    "/admin/",
    "/admin/login/",
    "/handyhelpers/live",
    "/handyhelpers/ready",
    "/handyhelpers/starttime",
    "/handyhelpers/uptime",
]


# logging configuration
LOG_PATH = env.str("LOG_PATH", os.path.join(BASE_DIR, "django_logs"))
DEFAULT_LOG_LEVEL = env.str("DEFAULT_LOG_LEVEL", "INFO")
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH, exist_ok=True)  # pragma: no cover
    print(f"INFO: created log path: {LOG_PATH}")  # pragma: no cover
else:
    print(f"INFO: using log path: {LOG_PATH}")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s",
            "datefmt": "%Y/%b/%d %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "django": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(str(LOG_PATH), "django.log"),
            "maxBytes": 1024 * 1024 * 15,
            "backupCount": 10,
            "formatter": "verbose",
        },
        "user": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(str(LOG_PATH), "user.log"),
            "maxBytes": 1024 * 1024 * 15,
            "backupCount": 10,
            "formatter": "verbose",
        },
        "console": {
            "level": DEFAULT_LOG_LEVEL,
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["django", "console"],
            "level": "INFO",
        },
        "user": {
            "handlers": ["user", "console"],
            "level": "INFO",
        },
        "": {
            "handlers": ["console"],
            "level": DEFAULT_LOG_LEVEL,
        },
    },
}


PROJECT_NAME = "spokanetech"
PROJECT_DESCRIPTION = """Home of the Spokane tech community."""
PROJECT_VERSION = env.str("PROJECT_VERSION", "")
PROJECT_SOURCE = "https://github.com/SpokaneTech/SpokaneTechWeb"


# celery settings
broker_url = env.str("CELERY_BROKER_URL", None)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_BEAT_SCHEDULER = env.str("BEAT_SCHEDULER", "django_celery_beat.schedulers:DatabaseScheduler")
CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", None)
CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND", None)
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_TASK_SERIALIZER = "json"
CELERY_USE_SSL = env.bool("CELERY_USE_SSL", True)
