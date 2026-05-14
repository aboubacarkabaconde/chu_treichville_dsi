# apps/core/apps.py

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Gestion centrale'

    def ready(self):
        try:
            import apps.core.signals
        except ImportError:
            pass