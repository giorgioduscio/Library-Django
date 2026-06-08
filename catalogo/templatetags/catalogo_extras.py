from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr_name):
    """Estrae un attributo da un oggetto in modo dinamico."""
    return getattr(obj, attr_name, "")
