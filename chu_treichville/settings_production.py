# chu_treichville/settings_production.py

from .settings import *

DEBUG = False

ALLOWED_HOSTS = [
    'dsi-chutreichville.pythonanywhere.com',
    'chutreichville.pythonanywhere.com',
    '.pythonanywhere.com',
]

# Base de données MySQL (si tu utilises MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chutreichville$chu_treichville',
        'USER': 'chutreichville',
        'PASSWORD': 'TON_MOT_DE_PASSE',
        'HOST': 'chutreichville.mysql.pythonanywhere-services.com',
        'PORT': '3306',
    }
}

# Fichiers statiques
STATIC_ROOT = '/home/chutreichville/chu_treichville_dsi/staticfiles'
STATIC_URL = '/static/'

MEDIA_ROOT = '/home/chutreichville/chu_treichville_dsi/media'
MEDIA_URL = '/media/'

# Sécurité
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True