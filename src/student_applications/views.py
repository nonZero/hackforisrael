from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from q13es.forms import parse_form
from q13es.models import Answer
import logging
import os.path

FORMS_DIR = os.path.join(os.path.dirname(__file__), 'forms')
logger = logging.getLogger(__name__)


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


def get_user_forms(user):
    return user.answers.values_list('q13e_slug', flat=True)


def get_user_next_form(user):

    filled = get_user_forms(user)

    for f in FORM_NAMES:
        if f not in filled:
            return f

    return None


class Dashboard(TemplateView):
    template_name = 'dashboard.html'


class FillFormView(FormView):
    template_name = 'fill-form.html'

    def get_form_class(self):
        form_name = get_user_next_form(self.request.user)
        assert form_name
        return FORMS[form_name]

    def form_valid(self, form):
        form_name = get_user_next_form(self.request.user)
        logger.info("User %s filled %s" % (self.request.user, form_name))
        Answer.objects.create(user=self.request.user, q13e_slug=form_name,
                              data=form.cleaned_data)
        messages.info(self.request, _("'%s' was saved.") % form.form_title)
        return redirect('fill_form')


class AllFormsView(TemplateView):
    template_name = 'all-forms.html'

    def get_context_data(self, **kwargs):
        d = super(AllFormsView, self).get_context_data(**kwargs)
        d['forms'] = [(k, FORMS[k]) for k in FORM_NAMES]
        return d
