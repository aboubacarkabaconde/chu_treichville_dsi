# apps/core/signals.py

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crée automatiquement un profil utilisateur à la création d'un compte"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Sauvegarde automatiquement le profil utilisateur"""
    if hasattr(instance, 'profile'):
        instance.profile.save()