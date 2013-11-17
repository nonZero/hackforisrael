from django.utils.translation import ugettext as _
from q13es.forms import FIELD_TYPES, parse_form
import codecs
import floppyforms as forms
import os.path

REQUIRED_FIELD = _("Required field")  # override floppyforms-foundation i18n

FORMS_DIR = os.path.join(os.path.dirname(__file__), 'forms')


CUSTOM_FIELD_TYPES = FIELD_TYPES.copy()


class ControlSelect(forms.RadioSelect):
    template_name = 'student_applications/control.html'


CUSTOM_FIELD_TYPES[_("control")] = (forms.ChoiceField, {
       'widget': ControlSelect,
       'choices': (
                   (0, _('0 - No knowledge')),
                   (1, _('1')),
                   (2, _('2 - Some knowledge')),
                   (3, _('3')),
                   (4, _('4 - Good informal knowledge or Formal Education')),
                   (5, _('5')),
                   (6, _('6 - Some parctical work experience')),
                   (7, _('7')),
                   (8, _('8 - Considerable work experience (2+ years)')),
                   (9, _('9')),
                   (10, _('10 - Full control of the technology')),
                   ),
      }
)

FORM_NAMES = (
    'personal-details',
    'about',
    'public-profiles',
    'work-experience',
    'programming-langs',
    'software-development',
    'web-technologies',
    'social-activity',
    'cohort1',
    'program',
    )


def read_file(k):
    with codecs.open(os.path.join(FORMS_DIR, k + '.txt'), 'r', 'utf-8') as f:
        return f.read()

FORMS = {k: parse_form(read_file(k), CUSTOM_FIELD_TYPES) for k in FORM_NAMES}


def get_user_forms(user):
    return user.answers.values_list('q13e_slug', flat=True)


def get_user_next_form(user):

    filled = get_user_forms(user)

    for f in FORM_NAMES:
        if f not in filled:
            return f

    return None


def get_user_progress(user):
    return len(get_user_forms(user)), len(FORMS)


def get_user_pretty_answers(u):
    return [a.get_pretty(FORMS[a.q13e_slug]) for a in
            u.answers.order_by('created_at')]
