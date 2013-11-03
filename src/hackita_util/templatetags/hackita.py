from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(needs_autoescape=True)
def u(instance, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    result = '<a href="%s">%s</a>' % (esc(instance.get_absolute_url()),
                                      esc(unicode(instance)))
    return mark_safe(result)
