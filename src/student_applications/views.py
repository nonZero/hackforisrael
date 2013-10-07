from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from q13es.forms import parse_form
from student_applications import forms
import os.path

FORMS_DIR = os.path.join(os.path.dirname(__file__), 'forms')


def read_file(k):
    with open(os.path.join(FORMS_DIR, k + '.txt')) as f:
        return f.read()
        return f.read().decode('utf8')

FORM_NAMES = (
    'personal-details',
    'about',
    'public-profiles',
    'work-experience',
    'programming-langs',
    'software-development',
    'web-technologies',
    'social-activity',
    'program',
    )

FORMS = {k: parse_form(read_file(k)) for k in FORM_NAMES}


class Dashboard(FormView):
    template_name = 'dashboard.html'
    # form_class = forms.PersonalDetailsForm
    # form_class = forms.ApplicationForm

    def get_form_class(self):
        return  forms.ApplicationForm


class AllFormsView(TemplateView):
    template_name = 'all-forms.html'

    def get_context_data(self, **kwargs):
        d = super(AllFormsView, self).get_context_data(**kwargs)
        d['forms'] = [(k, FORMS[k]) for k in FORM_NAMES]
        return d
