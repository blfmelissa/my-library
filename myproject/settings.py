import environ
from pathlib import Path
from django.utils.translation import gettext_lazy as _
from azure.identity import DefaultAzureCredential

# Initialisation de django-environ
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / ".env")  

ROOT_URLCONF = 'myproject.urls'

# Secret Key
SECRET_KEY = env('SECRET_KEY')

# Debug mode
DEBUG = env('DEBUG')

# Allowed Hosts and CSRF Trusted Origins
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS')

# Applications installées
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'books',
    'storages',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuration des templates
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

# Configuration des bases de données
DATABASES = {
    'default': {
        'ENGINE': env('DATABASE_ENGINE'),
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
        'OPTIONS': {
            'ssl': {'disabled': True},
        }
    }
}

# Configuration du stockage Azure
AZURE_ACCOUNT_NAME = env('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = env('AZURE_ACCOUNT_KEY')
AZURE_CONTAINER = env('AZURE_CONTAINER')
AZURE_URL = env('AZURE_URL')

DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "token_credential": DefaultAzureCredential(),
            "account_name": AZURE_ACCOUNT_NAME,
            "azure_container": AZURE_CONTAINER,
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "token_credential": DefaultAzureCredential(),
            "account_name": AZURE_ACCOUNT_NAME,
            "azure_container": AZURE_CONTAINER,
        },
    },
}

MEDIA_URL = AZURE_URL
MEDIA_ROOT = None

# Configuration des messages d'erreur pour les champs de formulaire
FORM_FIELD_ERRORS = {
    'required': _("Ce champ est obligatoire."),
    'max_length': _("Ce champ est trop long."),
}

# Configuration de la langue
LANGUAGE_CODE = 'fr'
