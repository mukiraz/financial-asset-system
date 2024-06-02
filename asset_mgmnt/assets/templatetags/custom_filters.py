from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def add_class(field, prefix):
    return field.as_widget(attrs={"id": f"{prefix}_{field.id_for_label}"})