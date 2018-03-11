"""
Django settings for demosite project.

Generated by 'django-admin startproject' using Django 1.10b1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cv8bnb0(d8%e6kt!x#qyy7_me#jy=)cv!_u=f9sse^a&r2eebw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
LOGIN_REDIRECT_URL = '/'
# AUTH_USER_MODEL = 'accounts.Customer'
# AUTHENTICATION_BACKENDS = ['accounts.backends.EmailAuthBackend', ]
SITE_NAME = "LYSHOP"
META_KEYWORDS = " Telephone, Smartphone, Parfum, Parfums, parfums, chaussure, \
                Sac, sacs, android, iphone, samsung, accessoires, shop, lyshop, shopping, gabon, afrique, achats"
META_DESCRIPTION = " Marché en ligne pour chaussures, Smartphone, parfums,\
                    sacs à main pour femmes et plein d'autres accessoires."
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.11.9', 'testserver','192.168.11.10','192.168.11.5', ]

handler404 = 'demosite.views.page_not_found'
handler500 = 'demosite.views.server_error'
handler403 = 'demosite.views.permission_denied'
handler400 = 'demosite.views.bad_request'
# EMAIL SETTINGS
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 465  # SSL REQUIRED
# EMAIL_PORT = 587  # TLS REQUIRED
EMAIL_HOST_PASSWORD = "Engineering0"
EMAIL_HOST_USER = "contact.gvshop"
CONTACT_MAIL = "contact.gvshop@gmail.com"
EMAIL_USE_SSL = True
# fixtures directories
FIXTURE_DIRS = ['fixtures']
# Application definition


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

INSTALLED_APPS = [
    'cart.apps.CartConfig',
    'catalog.apps.CatalogConfig',
    'accounts.apps.AccountsConfig',
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api.apps.ApiConfig',
    'order.apps.OrderConfig',
    'contact.apps.ContactConfig',
    'wishlist.apps.WishlistConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'demosite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.contrib.messages.context_processors.messages',
                'utils.context_processors.demosite',
            ],
            'builtins':[

            ],
        },
    },
]

WSGI_APPLICATION = 'demosite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'TEST': {
                'NAME': 'test_db.sqlite3',
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "staticfiles"),
)
STATIC_URL = '/static/'
