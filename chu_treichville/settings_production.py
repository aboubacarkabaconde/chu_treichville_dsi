# chu_treichville/settings_production.py

from .settings import *
import os

DEBUG = False

ALLOWED_HOSTS = ['votre-nom.pythonanywhere.com', 'www.votre-nom.pythonanywhere.com']

# Base de données MySQL (PythonAnywhere utilise MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'votre_nom$chu_treichville',
        'USER': 'votre_nom',
        'PASSWORD': 'VOTRE_MOT_DE_PASSE',
        'HOST': 'votre_nom.mysql.pythonanywhere-services.com',
        'PORT': '3306',
    }
}

# Fichiers statiques
STATIC_ROOT = '/home/votre_nom/chu_treichville/staticfiles'
STATIC_URL = '/static/'

MEDIA_ROOT = '/home/votre_nom/chu_treichville/media'
MEDIA_URL = '/media/'

# Sécurité
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True