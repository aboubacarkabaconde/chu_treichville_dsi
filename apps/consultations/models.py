# apps/consultations/models.py

from django.db import models
from apps.core.models import Rapport


class Consultation(Rapport):
    """Rapport de consultation - hérite de Rapport"""
    
    # Service en saisie libre
    service_nom = models.CharField(max_length=200, default="Service non spécifié")
    
    # Provenance des patients
    provenance_secondaire = models.IntegerField(default=0)
    provenance_tertiaire = models.IntegerField(default=0)
    non_refere = models.IntegerField(default=0)
    
    # Assurances
    assurance_cmu = models.IntegerField(default=0)
    assurance_privee = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Rapport de consultation"
        verbose_name_plural = "Rapports de consultation"
    
    def __str__(self):
        return f"Consultation - {self.service_nom} - {self.periode_str}"


class TrancheAgeActivite(models.Model):
    TRANCHES_AGE = [
        ('0-4', '0-4 ans'),
        ('5-9', '5-9 ans'),
        ('10-14', '10-14 ans'),
        ('15-19', '15-19 ans'),
        ('20-24', '20-24 ans'),
        ('25-49', '25-49 ans'),
        ('50+', '50 ans et plus'),
    ]
    SEXE_CHOICES = [('M', 'Masculin'), ('F', 'Féminin')]
    
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='activites')
    tranche_age = models.CharField(max_length=10, choices=TRANCHES_AGE)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    nombre = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['consultation', 'tranche_age', 'sexe']


class MotifConsultation(models.Model):
    TRANCHES_AGE = [
        ('0-4', '0-4 ans'),
        ('5-9', '5-9 ans'),
        ('10-14', '10-14 ans'),
        ('15-19', '15-19 ans'),
        ('20-24', '20-24 ans'),
        ('25-49', '25-49 ans'),
        ('50+', '50 ans et plus'),
    ]
    SEXE_CHOICES = [('M', 'Masculin'), ('F', 'Féminin')]
    
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='motifs')
    tranche_age = models.CharField(max_length=10, choices=TRANCHES_AGE)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    libelle_motif = models.CharField(max_length=255)
    nombre = models.IntegerField(default=0)


class DiagnosticRetenu(models.Model):
    TRANCHES_AGE = [
        ('0-4', '0-4 ans'),
        ('5-9', '5-9 ans'),
        ('10-14', '10-14 ans'),
        ('15-19', '15-19 ans'),
        ('20-24', '20-24 ans'),
        ('25-49', '25-49 ans'),
        ('50+', '50 ans et plus'),
    ]
    SEXE_CHOICES = [('M', 'Masculin'), ('F', 'Féminin')]
    
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='diagnostics')
    tranche_age = models.CharField(max_length=10, choices=TRANCHES_AGE)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    code_diagnostic = models.CharField(max_length=50, blank=True, null=True)
    libelle_diagnostic = models.CharField(max_length=255)
    nombre = models.IntegerField(default=0)