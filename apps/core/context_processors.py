# apps/core/context_processors.py

from .models import UserProfile


def user_service(request):
    """Context processor pour ajouter le service de l'utilisateur à tous les templates"""
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            return {
                'user_service': profile.service,
                'user_fonction': profile.fonction,
                'user_profile': profile,
            }
        except UserProfile.DoesNotExist:
            pass
    return {}