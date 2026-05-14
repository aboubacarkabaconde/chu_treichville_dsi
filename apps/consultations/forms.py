# apps/consultations/forms.py

from django import forms
from .models import Consultation, TrancheAgeActivite, MotifConsultation, DiagnosticRetenu


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['service', 'mois', 'annee', 'provenance_secondaire', 'provenance_tertiaire', 
                  'non_refere', 'assurance_cmu', 'assurance_privee', 'observations',
                  'coordinateur_nom', 'coordinateur_prenom', 'surveillant_nom', 'surveillant_prenom',
                  'chef_service_nom', 'chef_service_prenom']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-select'}),
            'mois': forms.Select(attrs={'class': 'form-select'}),
            'annee': forms.NumberInput(attrs={'class': 'form-control', 'value': '2024'}),
            'provenance_secondaire': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
            'provenance_tertiaire': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
            'non_refere': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
            'assurance_cmu': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
            'assurance_privee': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
            'observations': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'coordinateur_nom': forms.TextInput(attrs={'class': 'form-control'}),
            'coordinateur_prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'surveillant_nom': forms.TextInput(attrs={'class': 'form-control'}),
            'surveillant_prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'chef_service_nom': forms.TextInput(attrs={'class': 'form-control'}),
            'chef_service_prenom': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TrancheAgeActiviteForm(forms.ModelForm):
    class Meta:
        model = TrancheAgeActivite
        fields = ['tranche_age', 'sexe', 'nombre']
        widgets = {
            'tranche_age': forms.Select(attrs={'class': 'form-select'}),
            'sexe': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
        }


class MotifConsultationForm(forms.ModelForm):
    class Meta:
        model = MotifConsultation
        fields = ['tranche_age', 'sexe', 'libelle_motif', 'nombre']
        widgets = {
            'tranche_age': forms.Select(attrs={'class': 'form-select'}),
            'sexe': forms.Select(attrs={'class': 'form-select'}),
            'libelle_motif': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
        }


class DiagnosticRetenuForm(forms.ModelForm):
    class Meta:
        model = DiagnosticRetenu
        fields = ['tranche_age', 'sexe', 'code_diagnostic', 'libelle_diagnostic', 'nombre']
        widgets = {
            'tranche_age': forms.Select(attrs={'class': 'form-select'}),
            'sexe': forms.Select(attrs={'class': 'form-select'}),
            'code_diagnostic': forms.TextInput(attrs={'class': 'form-control'}),
            'libelle_diagnostic': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
        }