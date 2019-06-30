"""
Django settings for LeaveOnline project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i#c6%*x6z$5cil-c!cb5s#u_^)gd+z%0=vwtsf#ilpr+n_3t=z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'users.apps.UsersConfig',# new
    'managedb.apps.ManagedbConfig',# new
    'managedbtrans.apps.ManagedbtransConfig',# new
    # 'account.apps.AccountConfig',# new
    'frontend.apps.FrontendConfig', # new
    'apileaveonline.apps.ApileaveonlineConfig', #new

    'allauth',     
    'allauth.account',   
    'allauth.socialaccount',
    'allauth.socialaccount.providers.discord',
    'customprovider',  # Our custom provider  
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

ROOT_URLCONF = 'LeaveOnline.urls'

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
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LeaveOnline.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

APPEND_SLASH = False

LOGIN_URL = '/account/login/'
# LOGIN_REDIRECT_URL = '/user/'
LOGIN_REDIRECT_URL = '/account/bypass/'

CSRF_COOKIE_SECURE = True

SITE_ID = 1
# email
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "unix.leave.online@gmail.com "
EMAIL_HOST_PASSWORD = "tt054202249"

WEB_NAME = "http://127.0.0.1:3200/"

CHANNEL_ACCESS_TOKEN_LINE = "mSQoRJuk1pDM53Slc2VU/tRSosvDnr1siO6BrIhoWoA1/sTGjUGMUXXywOm00Pfc63lBjiG8pzMpA9t1HtuXszE2ASvojo3Xl4gVM2w+1jAOBkCKrOqc1g/fc2iTJH+DSRZ+hGsB5C9NNHvj6ooYPgdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET_LINE = "ab4b118069fd48f426342c0fd63bd7e4"

FERNET_KEY = 'bIiriIwsz3CI3gMUYovXMHqBg1jvYx-hjCqw8pxIIgs='

# AUTHENTICATION_BACKENDS = ["account.backends.EmailBackend"]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# SESSION_COOKIE_DOMAIN = "127.0.0.1:3200"

UNIX_PROVIDER_URL = "http://localhost:5200"
