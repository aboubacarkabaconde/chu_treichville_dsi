# apps/accouchements/admin.py

from django.contrib import admin
from .models import Accouchement


@admin.register(Accouchement)
class AccouchementAdmin(admin.ModelAdmin):
    list_display = ['service_nom', 'periode_str', 'statut', 'total_accouchements', 'created_by']
    list_filter = ['statut', 'mois', 'annee']
    search_fields = ['service_nom', 'observations']
    readonly_fields = ['created_at', 'updated_at']