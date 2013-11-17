from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import mail_managers
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import SingleObjectMixin, DetailView, \
    SingleObjectTemplateResponseMixin
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from h4il.base_views import ProtectedMixin, StaffOnlyMixin
from q13es.forms import get_pretty_answer
from surveys.models import SurveyAnswer, Survey


class SurveyListView(StaffOnlyMixin, ListView):
    model = Survey


class SurveyDetailView(StaffOnlyMixin, DetailView):
    model = Survey


class SurveyAnswerView(ProtectedMixin, SingleObjectTemplateResponseMixin,
                       SingleObjectMixin, FormView):
    model = SurveyAnswer

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.answered_at:
            return redirect('dashboard')
        if self.object.user != self.request.user:
            messages.warning(request,
               _("Wrong user! Please login with the correct user to continue"))
            return redirect('dashboard')
        return super(SurveyAnswerView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(SurveyAnswerView, self).get_context_data(
                                                object=self.object, **kwargs)

    def get_form_class(self):
        return self.get_object().survey.get_form_class()

    def form_valid(self, form):
        u = self.request.user
        data = form.cleaned_data

        o = self.get_object()
        o.data = data
        o.answered_at = timezone.now()
        o.save()

        message = "\n\n".join(u"{label}:\n {html}".format(**fld) for fld in
                            get_pretty_answer(form, data)['fields'])

        url = self.request.build_absolute_uri(o.survey.get_absolute_url())

        message += "\n%s" % url

        mail_managers(u"{}: {}".format(form.form_title, u), message)

        messages.success(self.request, _("Thank you!"))

        return redirect('register')

    def form_invalid(self, form):
        messages.warning(self.request,
                         _("Problems detected in form. "
                           "Please fix your errors and try again."))
        return FormView.form_invalid(self, form)
