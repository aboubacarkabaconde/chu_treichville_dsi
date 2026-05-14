# apps/urgences/models.py

from django.db import models
from apps.core.models import Rapport


class Urgence(Rapport):
    """Rapport des urgences - hérite de Rapport"""
    
    # Service en saisie libre
    service_nom = models.CharField(max_length=200, default="Service des Urgences")
    
    # Tableau 1: Capacité d'accueil
    nb_lits = models.IntegerField(default=0, verbose_name="Nombre de lits")
    nb_lits_fonctionnels = models.IntegerField(default=0, verbose_name="Nombre de lits fonctionnels")
    nb_journees_theoriques = models.IntegerField(default=0, verbose_name="Nombre de journées théoriques")
    nb_journees_realisees = models.IntegerField(default=0, verbose_name="Nombre de journées réalisées")
    taux_occupation = models.FloatField(default=0, verbose_name="Taux d'occupation (%)")
    delai_moyen_pec = models.FloatField(default=0, verbose_name="Délai moyen de prise en charge (heures)")
    
    # Assurances globales
    assurance_cmu = models.IntegerField(default=0, verbose_name="Patients CMU")
    assurance_privee = models.IntegerField(default=0, verbose_name="Assurance privée")
    
    class Meta:
        verbose_name = "Rapport des urgences"
        verbose_name_plural = "Rapports des urgences"
    
    def __str__(self):
        return f"Urgences - {self.service_nom} - {self.periode_str}"
    
    def save(self, *args, **kwargs):
        # Calcul automatique du taux d'occupation
        if self.nb_journees_theoriques > 0:
            self.taux_occupation = (self.nb_journees_realisees / self.nb_journees_theoriques) * 100
        super().save(*args, **kwargs)


class FrequentationUrgence(models.Model):
    """Tableau 2: Fréquentation par tranche d'âge et sexe"""
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
    
    urgence = models.ForeignKey(Urgence, on_delete=models.CASCADE, related_name='frequentations')
    tranche_age = models.CharField(max_length=10, choices=TRANCHES_AGE)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    
    # Données de fréquentation
    nb_admis = models.IntegerField(default=0, verbose_name="Patients admis")
    nb_observes = models.IntegerField(default=0, verbose_name="Patients en observation/hospitalisés")
    nb_refere = models.IntegerField(default=0, verbose_name="Patients référé")
    nb_retour_domicile = models.IntegerField(default=0, verbose_name="Retours à domicile")
    nb_deces = models.IntegerField(default=0, verbose_name="Décès")
    
    class Meta:
        unique_together = ['urgence', 'tranche_age', 'sexe']
    
    def __str__(self):
        return f"{self.get_tranche_age_display()} - {self.get_sexe_display()}"


class MorbiditeUrgence(models.Model):
    """Tableau 3: Morbidité par tranche d'âge et sexe"""
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
    
    urgence = models.ForeignKey(Urgence, on_delete=models.CASCADE, related_name='morbidites')
    tranche_age = models.CharField(max_length=10, choices=TRANCHES_AGE)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    pathologie = models.CharField(max_length=255, verbose_name="Pathologie")
    nombre = models.IntegerField(default=0, verbose_name="Nombre")
    
    def __str__(self):
        return f"{self.pathologie} - {self.get_tranche_age_display()} - {self.get_sexe_display()}"


class CauseDecesUrgence(models.Model):
    """Tableau 4: Causes des décès par tranche d'âge et sexe"""
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
    
    urgence = models.ForeignKey(Urgence, on_delete=models.CASCADE, related_name='causes_deces')
    tranche_age = models.CharField(max_length=10, choices=TRANCHES_AGE)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    cause = models.CharField(max_length=255, verbose_name="Cause probable du décès")
    nombre = models.IntegerField(default=0, verbose_name="Nombre")
    
    def __str__(self):
        return f"{self.cause} - {self.get_tranche_age_display()} - {self.get_sexe_display()}"