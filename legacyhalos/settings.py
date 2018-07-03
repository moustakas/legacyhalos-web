"""
Django settings for unwise project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# DATA_DIR = os.path.join(BASE_DIR, 'data')
# 
# SDSSPHOT_DATA_DIR = os.path.join(BASE_DIR, 'data', 'allwise', 'unwise-phot')
# SDSSPHOT_DATA_URL = '/data/allwise/unwise-phot/'

# WINDOW_FLIST_KD = os.path.join(BASE_DIR, 'window_flist_cut.kd')

# SDSS_PASSWORDS = open(os.path.join(BASE_DIR, 'passwords.txt')).readline().strip().split(',')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pt2xc@+_+7g-pcf!4#6%z2383w-vcare05aj3-vv5hunuoq6x3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#TEMPLATE_DEBUG = True
#TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'APP_DIRS': True,
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
    },
]

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'legacyhalos',
    #'coadd', # possible subdirectories to add in 'templates'
    #'sdssphot',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    # Not in Django 1.3
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'legacyhalos.urls'

WSGI_APPLICATION = 'legacyhalos.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/databases/
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

'''
python manage.py syncdb --database=usage
python manage.py syncdb
python load.py
python load2.py
'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'django.sqlite3'),
    },
    #'usage': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': '/var/www/unwise.me/usage.sqlite3',
    #    #'NAME': os.path.join(BASE_DIR, 'usage.sqlite3'),
    #},
    #'session': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': '/var/www/unwise.me/session.sqlite3',
    #    #'NAME': os.path.join(BASE_DIR, 'session.sqlite3'),
    #},
}

# DATABASE_ROUTERS = [ 'unwise.dbrouter.UnwiseDatabaseRouter', ]

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    )
