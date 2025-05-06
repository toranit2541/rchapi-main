# Description: This file contains the settings for the Django project.
#   - The `DEBUG` variable is set to `False` by default.
#   - The `BASE_DIR` variable is set to the base directory of the project.      
from pathlib import Path
import os

DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "https://www.ruamchai.com",
    "http://www.ruamchai.com",
    "https://ruamchai.com",   
    "http://ruamchai.com",
]

CSRF_TRUSTED_ORIGINS = [
    "http://www.ruamchai.com",
    "http://ruamchai.com",
    "https://www.ruamchai.com",
    "https://ruamchai.com",
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]
CORS_ALLOW_CREDENTIALS = True
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback-key-change-this')
# DEBUG = False
ALLOWED_HOSTS = ["ruamchai.com", "www.ruamchai.com","171.103.208.149"]
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account.apps.AccountConfig',
    'rchdata.apps.RchdataConfig',
    'rchnews.apps.RchnewsConfig',
    'rchpopulation.apps.RchpopulationConfig',
    'rchpackage.apps.RchpackageConfig',
    'rcharticle.apps.RcharticleConfig',
    'rcheven.apps.RchevenConfig',
    'rchpromotion.apps.RchpromotionConfig',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'versatileimagefield',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

ROOT_URLCONF = 'rchapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'rchapi.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "mssql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD",""),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", "1433"),
        "OPTIONS": {
            "driver": "ODBC Driver 17 for SQL Server",
        },
    },
}

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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
APPEND_SLASH = False
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
