"""
For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

DEBUG = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if DEBUG:
	from config_debug import *
else:
	from config import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

SECRET_KEY = 'km68=u49mi9y3$_yr%6g_jtngq@i^8-1ptag&((c6002q$p&rb'

ALLOWED_HOSTS = ["*"]

WSGI_APPLICATION = 'ModmailTicketer.wsgi.application'
USE_X_FORWARDED_HOST = not DEBUG

# Logging
"""if not DEBUG:
	LOGGING = {
	'version': 1,
	'disable_existing_loggers': True,
	'formatters': {
		'verbose': {
			'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s'
		}
	},
	'handlers': {
		'error_file': {
			'level': 'DEBUG',
			'class': 'logging.handlers.RotatingFileHandler',
			'formatter': 'verbose',
			'filename': '/root/web/ModmailTicketer/logs/gunicorn_errors.log',
			'maxBytes': 1024 * 1024 * 10,  # 100 mb
		}
	},
	'loggers': {
		'gunicorn.errors': {
			'level': 'error_file',
			'handlers': ['modmailticketer'],
			'propagate': True,
		},
	}
}"""

# Application definition

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django_jinja',
	'social.apps.django_app.default',
	'main'
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.security.SecurityMiddleware',
)

AUTHENTICATION_BACKENDS = (
	'social.backends.reddit.RedditOAuth2',
)

SOCIAL_AUTH_PIPELINE = (
	'social.pipeline.social_auth.social_details',
	'social.pipeline.social_auth.social_uid',
	'social.pipeline.social_auth.auth_allowed',
	'social.pipeline.social_auth.social_user',
	'social.pipeline.user.get_username',
	'social.pipeline.user.create_user',
	'main.func.auth_util.create_user_from_oauth',
	'social.pipeline.social_auth.associate_user',
	'social.pipeline.social_auth.load_extra_data',
	'social.pipeline.user.user_details'
)

ROOT_URLCONF = 'ModmailTicketer.urls'

TEMPLATES = [
	{
		# See: http://niwinz.github.io/django-jinja/#_user_guide_for_django_1_8
		"BACKEND": "django_jinja.backend.Jinja2",
		"APP_DIRS": True,
		"DIRS": [os.path.join(BASE_DIR, 'templates'),],
		"OPTIONS": {
			"match_extension": ".jinja",
			"trim_blocks": True,
			"lstrip_blocks": True,
		}
	},
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

TEMPLATE_DIRS = (
	os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_LOADERS = (
	'django_jinja.loaders.AppLoader',
	'django_jinja.loaders.FileSystemLoader',
)


# Login configuration

LOGIN_URL = "main:login"
LOGIN_REDIRECT_URL = "/"


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if DEBUG:
	db = {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
else:
	db = {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': DB_NAME,
		'USER': DB_USER,
		'PASSWORD': DB_PASSWORD,
		'HOST': 'localhost',
		'PORT': '',
	}

DATABASES = {
	'default': db
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static_public')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
	os.path.join(BASE_DIR, "static"),
)

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
