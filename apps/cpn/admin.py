from django.contrib import admin
from .models import ConsultationPrenatale


@admin.register(ConsultationPrenatale)
class ConsultationPrenataleAdmin(admin.ModelAdmin):
    list_display = ['service_nom', 'periode_str', 'statut', 'total_cpn', 'created_by']
    list_filter = ['statut', 'mois', 'annee']
    search_fields = ['service_nom', 'observations']
