from .settings import *

# Sekrety pobierane z zmiennych środowiskowych
SECRET_KEY = os.environ.get('SECRET_KEY')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Ustawienia bezpieczeństwa
DEBUG = True
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['*']

# Konfiguracja bazy danych
# DATABASE = os.environ.get('AZURE_POSTGRESQL_DATABASE')
# HOST = os.environ.get('AZURE_POSTGRESQL_HOST')
# PASSWORD = os.environ.get('AZURE_POSTGRESQL_PASSWORD')
# PORT = os.environ.get('AZURE_POSTGRESQL_PORT')
# USERNAME = os.environ.get('AZURE_POSTGRESQL_USERNAME')
# NAME = os.environ.get('AZURE_POSTGRESQL_NAME')

NAME = os.getenv('AZURE_POSTGRESQL_NAME'),
USER = os.getenv('AZURE_POSTGRESQL_USERNAME'),
PASSWORD = os.getenv('AZURE_POSTGRESQL_PASSWORD'),
HOST = os.getenv('AZURE_POSTGRESQL_HOST'),
PORT = int(os.environ.get('AZURE_POSTGRESQL_PORT', 5432))
if NAME and USER and PASSWORD and HOST and PORT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': NAME,
            'USER': USER,
            'PASSWORD': PASSWORD,
            'HOST': HOST,
            'PORT': PORT,
            'OPTIONS': {
                'sslmode': 'require'
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Middleware
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

# Ustawienia plików statycznych dla produkcji
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Ustawienia Azure Storage
AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = os.environ.get('AZURE_ACCOUNT_KEY')
AZURE_CONTAINER = 'ecommerceprojectww512-group_8_efe72e0a'
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'

if AZURE_ACCOUNT_NAME and AZURE_ACCOUNT_KEY:
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'

    MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Dodatkowe ustawienia
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
