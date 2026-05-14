# apps/consultations/admin.py

from django.contrib import admin
from .models import Consultation, TrancheAgeActivite, MotifConsultation, DiagnosticRetenu


class TrancheAgeActiviteInline(admin.TabularInline):
    model = TrancheAgeActivite
    extra = 14
    fields = ['tranche_age', 'sexe', 'nombre']


class MotifConsultationInline(admin.TabularInline):
    model = MotifConsultation
    extra = 1
    fields = ['tranche_age', 'sexe', 'libelle_motif', 'nombre']


class DiagnosticRetenuInline(admin.TabularInline):
    model = DiagnosticRetenu
    extra = 1
    fields = ['tranche_age', 'sexe', 'code_diagnostic', 'libelle_diagnostic', 'nombre']


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ['service', 'periode_str', 'statut', 'total_consultations', 'created_by']
    list_filter = ['service', 'statut', 'mois', 'annee']
    search_fields = ['service__nom', 'observations']
    inlines = [TrancheAgeActiviteInline, MotifConsultationInline, DiagnosticRetenuInline]
    readonly_fields = ['created_at', 'updated_at']
    
    def total_consultations(self, obj):
        return obj.total_consultations
    total_consultations.short_description = "Total consultations"