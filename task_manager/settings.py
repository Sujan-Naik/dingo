"""
Django settings for task_manager project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from django.contrib.messages import constants as messages
from dotenv import load_dotenv
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&$dln5wpgorppuw&(gintxm573v2ks+zq4o$(4*lapguixf^+2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", ".vercel.app", ".now.sh"]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'tasks',
    'formtools'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tasks.middleware.TimezoneMiddleware',
    'tasks.middleware.AllowIframeMiddleware'
]

CSRF_TRUSTED_ORIGINS = ['https://sujan-naik.github.io']
CSRF_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SECURE = True

ROOT_URLCONF = 'task_manager.urls'

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
                'tasks.context_processors.timezone_form',
            ],
        },
    },
]

WSGI_APPLICATION = 'task_manager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }

    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'mydb',
    #     'USER': 'myuser',
    #     'PASSWORD': 'mypass',
    #     'HOST': 'localhost',
    #     'PORT': '5432',
    # }

    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DATABASE', 'postgres'),  # Default to 'mydb' if the env variable is not set
        'USER': os.environ.get('POSTGRES_USER', 'myuser'),     # Default to 'myuser'
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'mypass'), # Default to 'mypass'
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),   # Default to 'localhost'
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),        # Default to '5432'
        'OPTIONS': {
            'connect_timeout': 10,  # Optional: Set a connection timeout
            'sslmode': 'require',     # Ensure SSL is required
            'host': '127.0.0.1',      # Force IPv4
        },
    }
}

print("Database Name:", os.environ.get('POSTGRES_DATABASE'))
print("Database User:", os.environ.get('POSTGRES_USER'))
print("Database Password:", os.environ.get('POSTGRES_PASSWORD'))
print("Database Host:", os.environ.get('POSTGRES_HOST'))
print("Database Port:", os.environ.get('POSTGRES_PORT'))


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# User model for authentication and login purposes
AUTH_USER_MODEL = 'tasks.User'

# Login URL for redirecting users from login protected views
LOGIN_URL = 'log_in'

# URL where @login_prohibited redirects to
REDIRECT_URL_WHEN_LOGGED_IN = 'dashboard'

# Convert Django ERROR messages to Bootstrap DANGER messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}
