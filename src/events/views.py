from django.contrib import messages
from django.core.mail import mail_managers
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from events import forms
from events.models import EventInvitation, EventInvitationStatus, Event
from h4il.base_views import StaffOnlyMixin


class EventListView(StaffOnlyMixin, ListView):
    model = Event


class EventDetailView(StaffOnlyMixin, DetailView):
    model = Event


class InvitationDetailView(DetailView):
    model = EventInvitation

    def post(self, request, *args, **kwargs):

        try:
            status = int(request.POST.get('status', '0'))
        except ValueError:
            status = 0
        if status not in [EventInvitationStatus.APPROVED,
                          EventInvitationStatus.DECLINED,
                          EventInvitationStatus.MAYBE]:
            return HttpResponseBadRequest("Bad status value")

        note = request.POST.get('note')

        o = self.get_object()

        if o.event.ends_at < timezone.now():
            messages.error(request, _("Event already finished."))

        else:
            if status != o.status or note != o.note:
                if o.registration_allowed():
                    o.status = status
                    o.note = note
                    o.save()
                    subject = u"%s: %s - %s" % (o.user, o.get_status_display(), o.event)
                    message = u"%s (%s): %s - %s\n%s" % (o.user, o.user.email,
                                                 o.get_status_display(), o.event,
                                                 o.note)
                    mail_managers(subject, message)
                    messages.success(request, _('Thank you!'))
                else:
                    messages.error(request, _('Registration already closed.'))
            else:
                messages.success(request, _('Thank you!'))

        return redirect(o)


class InvitationPreviewView(StaffOnlyMixin, DetailView):
    model = EventInvitation
    template_name = "emails/invitation.html"


class InvitationUpdateView(StaffOnlyMixin, UpdateView):
    model = EventInvitation
    form_class = forms.EventInvitationForm

    def form_valid(self, form):
        d = super(InvitationUpdateView, self).form_valid(form)
        messages.success(self.request, _("Invitation updated successfully"))
        return d

    def get_success_url(self):
        if 'from' in self.request.POST:
            return self.request.POST['from']
        return self.get_object().user.get_absolute_url()
