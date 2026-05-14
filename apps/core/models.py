# apps/core/models.py

from django.db import models
from django.contrib.auth.models import User


class CategorieService(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    ordre = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return self.nom


class Service(models.Model):
    TYPE_RAPPORT_CHOICES = [
        ('consultation', 'Consultation'),
        ('urgence', 'Urgences'),
    ]
    
    categorie = models.ForeignKey(CategorieService, on_delete=models.CASCADE, null=True, blank=True)
    nom = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    type_rapport = models.CharField(max_length=50, choices=TYPE_RAPPORT_CHOICES, blank=True, null=True)
    actif = models.BooleanField(default=True)
    ordre = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['categorie', 'ordre', 'nom']
    
    def __str__(self):
        return self.nom


class UserProfile(models.Model):
    FONCTION_CHOICES = [
        ('coordinateur', 'Coordinateur'),
        ('surveillant', 'Surveillant Chef'),
        ('chef_service', 'Chef de Service'),
        ('agent', 'Agent'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    fonction = models.CharField(max_length=50, choices=FONCTION_CHOICES, default='agent')
    telephone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        service_nom = self.service.nom if self.service else "Aucun service"
        return f"{self.user.username} - {service_nom}"


# apps/core/models.py - Modifie la classe Rapport

# apps/core/models.py - Modifie la classe Rapport

class Rapport(models.Model):
    """Rapport de base - Parent pour tous les rapports"""
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('termine', 'Terminé'),
        ('valide', 'Validé'),
        ('en_ligne', 'En ligne'),
    ]
    
    service = models.ForeignKey(
        Service, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
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
        ordering = ['-annee', '-mois']
    
    def __str__(self):
        service_name = self.service.nom if self.service else "Sans service"
        return f"{service_name} - {self.mois:02d}/{self.annee}"
    
    @property
    def periode_str(self):
        return f"{self.mois:02d}/{self.annee}"
    
    def get_statut_badge(self):
        """Retourne la classe CSS pour le badge de statut"""
        badges = {
            'brouillon': ('secondary', 'fa-pen', 'Brouillon'),
            'termine': ('success', 'fa-check-circle', 'Terminé'),
            'valide': ('primary', 'fa-check-double', 'Validé'),
            'en_ligne': ('info', 'fa-globe', 'En ligne'),
        }
        return badges.get(self.statut, ('secondary', 'fa-clock', self.get_statut_display()))