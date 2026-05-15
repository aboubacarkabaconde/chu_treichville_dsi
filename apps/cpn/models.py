from django.db import models
from apps.core.models import Rapport


class ConsultationPrenatale(Rapport):
    service_nom = models.CharField(max_length=200, default='Service de Gynecologie-Obstetrique')
    cpn1 = models.IntegerField(default=0)
    cpn2 = models.IntegerField(default=0)
    cpn3 = models.IntegerField(default=0)
    cpn4 = models.IntegerField(default=0)
    cpn5_plus = models.IntegerField(default=0)
    consultations_postnatales = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Rapport CPN'
        verbose_name_plural = 'Rapports CPN'

    def __str__(self):
        return f'CPN - {self.service_nom} - {self.periode_str}'

    @property
    def total_cpn(self):
        return self.cpn1 + self.cpn2 + self.cpn3 + self.cpn4 + self.cpn5_plus

    @property
    def total_consultations(self):
        return self.total_cpn + self.consultations_postnatales
