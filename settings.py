import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
SECRET_KEY = 'django'
DEBUG = True
STATIC_URL = 'static/'
ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]
DATABASES = {'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}}
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': {
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    }}
}]
INSTALLED_APPS = ['django.contrib.' + app for app in 'admin,auth,contenttypes,sessions,messages,staticfiles'.split(',')]
