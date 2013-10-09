import floppyforms as forms
from django.utils.datastructures import SortedDict
from django.utils.translation import gettext as _
import re

FIELD_TYPES = {
            _("general"): forms.CharField,
            _("text"): (forms.CharField, {
                                           'widget': forms.Textarea,
                                          }),
            _("radio"): (forms.ChoiceField, {
                                           'widget': forms.RadioSelect,
                                          }),
         }


PARAGRAPHS_RE = re.compile(r'\n\s*\n(?:\s*\n)*')


def process_choice(s):
    assert s.strip()[0] in ['*', '-']
    return s.strip()[1:].strip()


def normalize_whitespace(s):
    return re.sub('\s+', ' ', s.strip())


def parse_field(text, **kwargs):
    """ parses a block of text, composed of:
      -  title
      -  blank line
      -  type
      -  blank line
      -  help text

      type is :
         - a string,
         - with optional ':' for choices following immedietly,
           one per line starting with an asterick and a space.
    """
    d = kwargs.copy()
    l = [s.strip() for s in PARAGRAPHS_RE.split(text.strip())]
    assert l, "Field definition must contain at least a title"

    d['label'] = normalize_whitespace(l.pop(0))

    if l:

        field_def = l.pop(0).splitlines()

        # check if choices exist
        if field_def[0][-1] == ':':
            field_def[0] = field_def[0][:-1]
            choices = [process_choice(s) for s in field_def[1:]]
            d['choices'] = [(x, x) for x in choices]

        field_type = field_def[0]
    else:
        field_type = None

    d['help_text'] = "\n".join(normalize_whitespace(s) for s in l)

    return field_type, d


FIELD_RE = re.compile('^\[([a-zA-Z_]\w*)(\??)\]\s*$', re.M)


def split_form_file(text):
    """ splits a file with field names in brackets """

    blocks = [s.strip() for s in FIELD_RE.split(text.strip())]

    # blocks[0] is text before first field
    # blocks[1] is name of first field
    # blocks[2] is "?" if first field is optional
    # blocks[3] is content of first field
    # blocks[4] is name of second field...

    is_optional = lambda x: x != "?"

    head, fields = blocks[0], zip(blocks[1::3],
                                  [is_optional(x) for x in blocks[2::3]],
                                  blocks[3::3])
    return head, fields


def lookup_field_class_and_args(field_type, info, field_types=FIELD_TYPES):
    """ lookups field definition and composes a tuple of:
        (field_class, kwargs)
    """

    field_def = field_types[field_type if field_type else _('general')]

    field_class, base_args = field_def if isinstance(field_def, tuple) \
                                        else (field_def, {})
    args = base_args.copy()
    args.update(info)

    return field_class, args


def create_form(info):
    """
    Dynamically creates a form class from the supplied info.
    info is a list of tuples in the form (field_name, (field_class, kwargs))
    """

    fields = SortedDict((k, fld_class(**kw)) for k, (fld_class, kw) in info)

    form_class = type("CustomForm", (forms.BaseForm,), {'base_fields': fields})

    return form_class


def parse_form_head(text):
    l = [s.strip() for s in PARAGRAPHS_RE.split(text.strip())]

    title = l.pop(0) if l else None
    description = "\n".join(normalize_whitespace(s) for s in l)

    return title, description


def parse_form(text, field_types=FIELD_TYPES):

    head, fields = split_form_file(text)

    title, description = parse_form_head(head)

    get_field = lambda info, required: lookup_field_class_and_args(
                              *parse_field(info, required=required), 
                              field_types=field_types)

    fields_def = [(k, get_field(info, required)) for
                                k, required, info in fields]

    form_class = create_form(fields_def)
    form_class.form_title = title
    form_class.form_description = description

    return form_class


def get_pretty_answer(form_class, data):
    return {
            "title": form_class.form_title,
            "fields": [{
                        "label": form_class.base_fields[k].label,
                        "html": v
                       } for (k, v) in data.items()]
           }
