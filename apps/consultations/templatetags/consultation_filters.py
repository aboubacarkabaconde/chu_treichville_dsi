# apps/consultations/templatetags/consultation_filters.py

# apps/consultations/templatetags/consultation_filters.py

from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Récupère un élément d'un dictionnaire par sa clé"""
    if dictionary is None:
        return None
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None


@register.filter
def get_attr(obj, attr_name):
    """Récupère un attribut d'un objet"""
    if obj is None:
        return None
    return getattr(obj, attr_name, None)


