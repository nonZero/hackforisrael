# coding: utf-8

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import mail_managers
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from events.models import Event
from extra_views.formsets import InlineFormSetView
from h4il.base_views import ProtectedMixin, StaffOnlyMixin
from q13es.forms import get_pretty_answer
from q13es.models import Answer
from student_applications.consts import get_user_progress, FORMS, \
    get_user_next_form, FORM_NAMES, get_user_pretty_answers
from student_applications.models import UserCohortStatus, Cohort, UserCohort
from surveys.models import Survey
from users.models import update_personal_details, HackitaUser
import logging

logger = logging.getLogger(__name__)


class UserViewMixin(ProtectedMixin):

    def get_context_data(self, **kwargs):
        d = super(UserViewMixin, self).get_context_data(**kwargs)

        d['filled_count'], d['total_count'] = get_user_progress(
                                                            self.request.user)
        d['progress'] = int(100 * (d['filled_count'] + 1) /
                             (d['total_count'] + 1))

        return d


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
                               _("New User"), **data), message)

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
            url = self.request.build_absolute_uri(reverse('user_dashboard',
                                                           args=(u.id,)))
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


class UserCohortUpdateView(StaffOnlyMixin, InlineFormSetView):
    model = HackitaUser
    inline_model = UserCohort
    template_name = 'student_applications/usercohort_formset.html'
    extra = 0
    can_delete = False
    fields = ('status',)

    def get_success_url(self):
        if 'from' in self.request.POST:
            return self.request.POST['from']
        return self.get_object().get_absolute_url()


class CohortListView(StaffOnlyMixin, ListView):
    model = Cohort


class CohortDetailView(StaffOnlyMixin, DetailView):
    model = Cohort
    slug_field = 'code'

    def get_context_data(self, **kwargs):
        d = super(CohortDetailView, self).get_context_data(**kwargs)
        d['surveys'] = Survey.objects.all()
        d['events'] = Event.objects.filter(is_active=True)
        d['statuses'] = UserCohortStatus.choices
        return d

    def post(self, request, *args, **kwargs):

        cohort = self.get_object()

        user_ids = [int(x) for x in request.POST.getlist('users')]
        base_url = request.build_absolute_uri('/')[:-1]

        if request.POST.get('status'):
            status = int(request.POST.get('status'))
            for uid in user_ids:
                user = HackitaUser.objects.get(pk=uid)
                uc = UserCohort.objects.get(user=user, cohort=cohort)
                if uc.status != status:
                    uc.status = status
                    uc.save()
                    messages.success(request, u"%s: %s" %
                                     (user, uc.get_status_display()))
            # fall thorugh.

        # Send surveys
        if request.POST.get('survey'):
            survey = Survey.objects.get(pk=int(request.POST['survey']))

            for uid in user_ids:
                user = HackitaUser.objects.get(pk=uid)
                o, created = survey.add_user(user)
                if created:
                    o.send(base_url)
                messages.success(request, u"%s: %s" % (user,
                                  _("Sent") if created else _("Already sent")))

            return redirect(survey)

        # send event invitations
        if request.POST.get('event'):
            event = Event.objects.get(pk=int(request.POST['event']))

            for uid in user_ids:
                user = HackitaUser.objects.get(pk=uid)
                o, created = event.invite_user(user, request.user, base_url)
                messages.success(request, u"%s: %s" % (user,
                           _("Invited") if created else _("Already invited")))

            return redirect(event)

        return redirect(cohort)
