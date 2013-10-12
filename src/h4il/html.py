from django.db import models
from django.utils.translation import ugettext_lazy as _
import bleach

TAGS = [
    'a',
    'abbr',
    'acronym',
    'b',
    'blockquote',
    'code',
    'em',
    'i',
    'li',
    'ol',
    'strong',
    'ul',
    'p',
    'br',
    'span',
]

ATTRIBUTES = {
    'a': ['href', 'title'],
    'abbr': ['title'],
    'acronym': ['title'],
    'span': ['style'],
}

STYLES = ['text-decoration']


def clean_html(s):
    return bleach.clean(s, TAGS, ATTRIBUTES, STYLES)


def enhance_html(s):
    return bleach.linkify(clean_html(s))


class HTMLField(models.TextField):
    """
    A string field for HTML content.
    """
    description = _("HTML content")

    def formfield(self, **kwargs):
        ff = super(HTMLField, self).formfield(**kwargs)
        if 'class' in ff.widget.attrs:
            ff.widget.attrs['class'] += " wysiwyg"
        else:
            ff.widget.attrs['class'] = "wysiwyg"
        return ff

    def clean(self, value, model_instance):
        value = super(HTMLField, self).clean(value, model_instance)
        return enhance_html(value)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^h4il\.html\.HTMLField"])
except ImportError:
    pass
