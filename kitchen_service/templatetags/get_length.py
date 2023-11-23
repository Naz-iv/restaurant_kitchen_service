from django import template

register = template.Library()


@register.filter(name='get_length')
def get_length(obj):
    print(obj)
    try:
        return len(obj)
    except (TypeError, AttributeError):
        return 0
