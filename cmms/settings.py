"""
Django settings for cmms project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-w^6&lqw()^ewp64be*nx!uk!zx3u1p^=3_1)w7(-!u&^gf%miz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    'push_notifications',
   
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # 'django.middleware.locale.LocaleMiddleware', 
]

# Add the languages you support
# LANGUAGES = [
#     ('en', 'English'),
#     ('ml', 'Malayalam'),
# ]

LANGUAGE_CODE = 'en-us'

# Path to translation files
LOCALE_PATHS = [
    BASE_DIR / 'locale',  # Adjust path based on your project's structure
]

ROOT_URLCONF = 'cmms.urls'

TEMPLATES = [
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

WSGI_APPLICATION = 'cmms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cmms',
        'USER': 'root',
        'PASSWORD': 'Chithra@123',
        'HOST':'localhost',
        'PORT':'3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/



#TIME_ZONE = 'UTC'

# USE_I18N = True

#USE_TZ = True

# settings.py
TIME_ZONE = 'Asia/Kolkata'  # Set to your local time zone
USE_TZ = True  # Ensures times are stored in UTC and converted to the local time zone


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'myapp.CustomUser'


# To serve static files during development (for local testing)
STATICFILES_DIRS = [BASE_DIR / 'myapp/static']

# In production, you may also want to configure this:
#STATIC_ROOT = BASE_DIR / 'staticfiles'

# settings.py

import os

# URL to use when referring to media files (e.g., images uploaded by users)
MEDIA_URL = '/media/'

# Absolute path to the directory where media files are stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


PUSH_NOTIFICATIONS_SETTINGS = {
    "FCM_API_KEY": "BHuFbcQqQdHqfnUuow0sG4nZHl4aE2B3bG7wI6IFQd_s5mcNBUu8Yl8RB4N-Moj2Zt2uAKvVSdE1mxqIayTGays",
   
}

# settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Use SMTP backend
EMAIL_HOST = 'smtp.gmail.com'  # Gmail SMTP server
EMAIL_PORT = 587  # Use 587 for TLS, 465 for SSL
EMAIL_USE_TLS = True  # Enable TLS for secure connection
EMAIL_USE_SSL = False  # Disable SSL since TLS is enabled
EMAIL_HOST_USER = 'cfmms07@gmail.com'  # Replace with your email
EMAIL_HOST_PASSWORD = 'idxt tvla opwx gpnf'  
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # Default from email


# SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Default: store sessions in the database
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_COOKIE_AGE = 3600  # 1 hour

LOGIN_URL = '/'

