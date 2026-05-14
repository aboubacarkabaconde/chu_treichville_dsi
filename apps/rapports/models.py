from django.db import models

from apps.core.models import Service

# Create your models here.
# apps/core/models.py - Modifie la classe Rapport

class Rapport(models.Model):
    """Rapport de base - Parent pour tous les rapports"""
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('soumis', 'Soumis'),
        ('valide', 'Validé'),
    ]
    
    # Rendre service optionnel (null=True, blank=True)
    service = models.ForeignKey(
        Service, 
        on_delete=models.SET_NULL,  # Changé de CASCADE à SET_NULL
        null=True, 
        blank=True,  # Ajouté blank=True
        related_name='rapports'
    )
    mois = models.IntegerField(verbose_name="Mois", choices=[(i, i) for i in range(1, 13)])
    annee = models.IntegerField(verbose_name="Année")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='rapports')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Signatures
    coordinateur_nom = models.CharField(max_length=100, blank=True, null=True)
    coordinateur_prenom = models.CharField(max_length=100, blank=True, null=True)
    surveillant_nom = models.CharField(max_length=100, blank=True, null=True)
    surveillant_prenom = models.CharField(max_length=100, blank=True, null=True)
    chef_service_nom = models.CharField(max_length=100, blank=True, null=True)
    chef_service_prenom = models.CharField(max_length=100, blank=True, null=True)
    
    observations = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['service', 'mois', 'annee']
        ordering = ['-annee', '-mois', 'service__nom']
    
    def __str__(self):
        service_name = self.service.nom if self.service else "Sans service"
        return f"{service_name} - {self.mois:02d}/{self.annee}"
    
    @property
    def periode_str(self):
        return f"{self.mois:02d}/{self.annee}"