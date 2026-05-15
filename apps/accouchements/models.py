# apps/accouchements/models.py

from django.db import models
from apps.core.models import Rapport


class Accouchement(Rapport):
    """Rapport des accouchements - hérite de Rapport"""
    
    # Service en saisie libre
    service_nom = models.CharField(max_length=200, default="Service de Gynécologie-Obstétrique")
    
    # Types d'accouchements
    accouchements_domicile = models.IntegerField(default=0, verbose_name="Accouchements à domicile")
    accouchements_normal = models.IntegerField(default=0, verbose_name="Accouchement normal (voie basse)")
    accouchements_cesarienne = models.IntegerField(default=0, verbose_name="Accouchement par césarienne")
    autres_accouchements = models.IntegerField(default=0, verbose_name="Autres types d'accouchements")
    
    # Issues
    mort_nes = models.IntegerField(default=0, verbose_name="Mort-nés")
    naissances_vivantes = models.IntegerField(default=0, verbose_name="Naissances vivantes")
    hypotrophie = models.IntegerField(default=0, verbose_name="Hypotrophie à la naissance (poids < 2500g)")
    
    # Décès
    deces_maternel = models.IntegerField(default=0, verbose_name="Décès maternel")
    deces_neonatal = models.IntegerField(default=0, verbose_name="Décès néonatal")
    
    class Meta:
        verbose_name = "Rapport d'accouchement"
        verbose_name_plural = "Rapports d'accouchements"
    
    def __str__(self):
        return f"Accouchements - {self.service_nom} - {self.periode_str}"
    
    @property
    def total_accouchements(self):
        """Total des accouchements dans l'établissement"""
        return self.accouchements_normal + self.accouchements_cesarienne + self.autres_accouchements
    
    @property
    def total_accouchements_global(self):
        """Total des accouchements (domicile + établissement)"""
        return self.accouchements_domicile + self.total_accouchements