from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr_name):
    """Estrae un attributo da un oggetto in modo dinamico."""
    return getattr(obj, attr_name, "")

@register.filter
def class_name(obj):
    """Restituisce il nome della classe di un oggetto."""
    return obj.__class__.__name__
