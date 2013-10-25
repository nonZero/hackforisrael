# coding: utf8

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import mail_managers
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Count, Max
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from h4il.base_views import ProtectedMixin, StaffOnlyMixin
from q13es.forms import parse_form, FIELD_TYPES, get_pretty_answer
from q13es.models import Answer
from student_applications.models import UserCohortStatus, Cohort, UserCohort, \
    Tag, UserTag
from users.models import HackitaUser, update_personal_details
import floppyforms as forms
import logging
import os.path
from django.db.utils import IntegrityError

REQUIRED_FIELD = _("Required field")  # override floppyforms-foundation i18n

FORMS_DIR = os.path.join(os.path.dirname(__file__), 'forms')
logger = logging.getLogger(__name__)


def read_file(k):
    with open(os.path.join(FORMS_DIR, k + '.txt')) as f:
        return f.read()

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


class UserViewMixin(ProtectedMixin):

    def get_context_data(self, **kwargs):
        d = super(UserViewMixin, self).get_context_data(**kwargs)

        d['filled_count'], d['total_count'] = get_user_progress(
                                                            self.request.user)
        d['progress'] = int(100 * (d['filled_count'] + 1) /
                             (d['total_count'] + 1))

        return d


def get_user_pretty_answers(u):
    return [a.get_pretty(FORMS[a.q13e_slug]) for a in
            u.answers.order_by('created_at')]


class Dashboard(UserViewMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        d = super(Dashboard, self).get_context_data(**kwargs)

        d['registered'] = get_user_next_form(self.request.user) is None

        if d['registered']:
            d['answers'] = get_user_pretty_answers(self.request.user)

        return d


class RegisterView(UserViewMixin, FormView):
    template_name = 'register.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        form = self.get_form_class()
        if form is None:
            return redirect('dashboard')

        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get_form_class(self):
        form_name = get_user_next_form(self.request.user)
        if not form_name:
            return None

        return FORMS[form_name]

    def form_valid(self, form):
        u = self.request.user
        data = form.cleaned_data
        form_name = get_user_next_form(u)

        logger.info("User %s filled %s" % (u, form_name))

        a = Answer.objects.create(user=u, q13e_slug=form_name, data=data)

        # Save personal information
        if form_name == FORM_NAMES[0]:
            if not u.first_name:
                u.first_name = data['hebrew_first_name']
            if not u.last_name:
                u.last_name = data['hebrew_last_name']
            update_personal_details(u, data)
            u.save()  # keep it on the safe side

            message = "\n".join(u"{label}: {html}".format(**fld) for fld in
                                get_pretty_answer(form, data)['fields'])
            mail_managers(u"{}: {hebrew_last_name} {hebrew_first_name}".format(
                               _("New User").decode('utf8'), **data), message)

        elif form_name == 'cohort1':
            COHORTS = (
                        ('group_monday_morning', 1),
                        ('group_thursday_morning', 2),
                        ('group_evenings', 3),
                      )
            cohorts = {x[1]: Cohort.objects.get(ordinal=x[1]) for x in COHORTS}
            for k, ordinal in COHORTS:
                v = data[k] == u"כן"
                UserCohort.objects.create(user=u, cohort=cohorts[ordinal],
                          status=UserCohortStatus.AVAILABLE if v else
                          UserCohortStatus.UNAVAILABLE)

        # update denormalized index fields
        u.forms_filled = u.answers.count()
        u.last_form_filled = a.created_at
        u.save()

        if get_user_next_form(u) is None:
            messages.success(self.request,
                             _("Registration completed! Thank you very much!"))
            url = self.request.build_absolute_uri(reverse('user_dashboard', args=(u.id,)))
            mail_managers(_("User registered: %s") % u.email, url)
            return redirect('dashboard')

        messages.success(self.request, _("'%s' was saved.") % form.form_title)

        return redirect('register')

    def form_invalid(self, form):
        messages.warning(self.request,
                         _("Problems detected in form. "
                           "Please fix your errors and try again."))
        return FormView.form_invalid(self, form)


class AllFormsView(TemplateView, ProtectedMixin):
    template_name = 'all-forms.html'

    def get_context_data(self, **kwargs):
        d = super(AllFormsView, self).get_context_data(**kwargs)
        d['forms'] = [(k, FORMS[k]) for k in FORM_NAMES]
        return d


class UsersListView(StaffOnlyMixin, ListView):

    def get_cohort(self):
        if 'cohort' not in self.request.GET:
            return None

        if not hasattr(self, '_cohort'):
            try:
                self._cohort = Cohort.objects.get(ordinal=int(self.request.GET['cohort']))
            except ValueError, Cohort.DoesNotExist:
                self._cohort = None

        return self._cohort

    def get_context_data(self, **kwargs):
        d = super(UsersListView, self).get_context_data(**kwargs)
        d['cohort'] = self.get_cohort()
        d['cohorts'] = Cohort.objects.order_by('ordinal')
        return d

    def get_queryset(self):
        qs = HackitaUser.objects.order_by('-forms_filled', '-last_form_filled')

        cohort = self.get_cohort()
        if cohort:
            qs = qs.filter(cohorts__cohort=cohort,
                           cohorts__status__in=[
                                    UserCohortStatus.AVAILABLE,
                                    UserCohortStatus.INVITED_TO_INTERVIEW,
                                    UserCohortStatus.ACCEPTED,
                                    ])

        return qs


class UserDashboard(StaffOnlyMixin, DetailView):
    model = HackitaUser

    def get_context_data(self, **kwargs):
        d = super(UserDashboard, self).get_context_data(**kwargs)
        user = self.get_object()
        d['answers'] = get_user_pretty_answers(user)
        d['tagged'] = user.tags.filter(created_by=self.request.user)
        tagged_ids = [ut.tag.id for ut in d['tagged']]
        d['all_tags'] = [(tag, tag.id in tagged_ids) for tag in Tag.objects.all()]

        return d

    def post(self, request, *args, **kwargs):
        try:
            tag_id = int(request.POST.get('tag', ''))
        except ValueError:
            return HttpResponseBadRequest("Tag field is missing or invalid")

        tag = get_object_or_404(Tag, pk=tag_id)

        u = self.get_object()

        if request.POST.get('delete'):
            UserTag.objects.untag(u, tag, request.user)
        else:
            UserTag.objects.tag(u, tag, request.user)

        return redirect('user_dashboard', pk=u.id)
