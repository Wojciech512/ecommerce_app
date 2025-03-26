import os
from pathlib import Path
from decouple import config, Csv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='temp-key')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=Csv())
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "store",
    "cart",
    "account",
    "payment",
    "mathfilters",
    "crispy_forms",
    "storages",
]

CRISPY_TEMPLATE_PACK = "bootstrap4"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ecommerce.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "store.views.categories",
                "cart.context_processors.cart",
            ],
        },
    },
]

WSGI_APPLICATION = "ecommerce.wsgi.application"

AZURE_NAME = os.getenv('AZURE_POSTGRESQL_NAME')
AZURE_USER = os.getenv('AZURE_POSTGRESQL_USERNAME')
AZURE_PASSWORD = os.getenv('AZURE_POSTGRESQL_PASSWORD')
AZURE_HOST = os.getenv('AZURE_POSTGRESQL_HOST')
AZURE_PORT = os.environ.get('AZURE_POSTGRESQL_PORT', 5432)

GOOGLE_NAME = os.getenv('GOOGLE_POSTGRESQL_NAME')
GOOGLE_USER = os.getenv('GOOGLE_POSTGRESQL_USERNAME')
GOOGLE_PASSWORD = os.getenv('GOOGLE_POSTGRESQL_PASSWORD')
GOOGLE_HOST = os.getenv('GOOGLE_POSTGRESQL_HOST')
GOOGLE_PORT = os.environ.get('GOOGLE_POSTGRESQL_PORT', 5432)

if AZURE_NAME and AZURE_USER and AZURE_PASSWORD and AZURE_HOST and AZURE_PORT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': AZURE_NAME,
            'USER': AZURE_USER,
            'PASSWORD': AZURE_PASSWORD,
            'HOST': AZURE_HOST,
            'PORT': AZURE_PORT,
            'OPTIONS': {
                'sslmode': 'require'
            },
        }
    }
elif GOOGLE_NAME and GOOGLE_USER and GOOGLE_PASSWORD and GOOGLE_HOST and GOOGLE_PORT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': GOOGLE_NAME,
            'USER': GOOGLE_USER,
            'PASSWORD': GOOGLE_PASSWORD,
            'HOST': GOOGLE_HOST,
            'PORT': GOOGLE_PORT,
            'OPTIONS': {
                'sslmode': 'disable'
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'db',
            'PORT': 5432,
            'OPTIONS': {
                'sslmode': 'disable'
            },
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"
