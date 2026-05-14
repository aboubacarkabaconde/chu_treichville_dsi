# apps/urgences/apps.py

from django.apps import AppConfig


class UrgencesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.urgences'
    verbose_name = 'Urgences'