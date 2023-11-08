from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(env_file=BASE_DIR / '.env')

DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])
SITE_URL = env.str('SITE_URL', default='http://127.0.0.1')
SECRET_KEY = env('SECRET_KEY')
SALT = env('SALT')
API_SALT = env('API_SALT')
API_SECRET_KEY = env('API_SECRET_KEY')
ROOT_URLCONF = 'server.urls'
WSGI_APPLICATION = 'server.wsgi.application'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.parent / 'static'
INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'server',
    'auth_service',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'auth_service.middleware.DecodeEncodeMiddleware'
]

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / '.sqlite3.db',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / '.debug.log',
            'formatter': 'main',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'API сервера авторизации',
    'DESCRIPTION': (
        'Сервер предоставляет доступ к управлению авторизацией пользователей\n\n'
        'Алгоритм работы следующий:\n'
        '- через метод категории "1. Ключ" получаем публичный ключ\n'
        '- через один из методов категории "2. Временный токен" получаем временный токен.\n'
        '- через один из методов категории "3. Пользователь" манипулируем данными пользователя.\n\n'
        'Запросы категории 2 и 3 должны быть зашифрованы ключом, полученным из запроса категории 1. '
        'В тело запроса категории 2 и 3 также нужно вставить сгенерированный публичный ключ, которым '
        'сервер авторизации зашифрует ответ. В тело запроса категории 3 нужно вставить временный токен.'
    ),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': True,
    'SCHEMA_PATH_PREFIX_INSERT': 'api',
    #'SCHEMA_PATH_PREFIX': '/api/v[0-9]',
    'SERVE_URLCONF': 'server.urls_api',
    'SERVERS': [{'url': f'{SITE_URL}'}],
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# External auth

AUTH_USER_MODEL = 'auth_service.AuthUser'
MICROSERVICES_TOKENS = {
    'from_platform': env('MICROSERVICE_TOKEN_FROM_PLATFORM'),
    'from_faci': env('MICROSERVICE_TOKEN_FROM_FACI'),
    'from_notes': env('MICROSERVICE_TOKEN_FROM_NOTES'),
    'from_social': env('MICROSERVICE_TOKEN_FROM_SOCIAL'),
}
MICROSERVICES_URLS = {
}


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
