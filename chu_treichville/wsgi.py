# WSGI configuration file (pythonanywhere.com)
import os
import sys

path = '/home/votre_nom/chu_treichville'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'chu_treichville.settings_production'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()