from django.contrib import messages
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from events.models import EventInvitation, EventInvitationStatus
from h4il.base_views import StaffOnlyMixin
from django.utils.translation import ugettext as _


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

        o = self.get_object()
        o.status = status
        o.save()

        messages.success(request, _('Thank you!'))

        return redirect(o)


class InvitationPreviewView(StaffOnlyMixin, DetailView):
    model = EventInvitation
    template_name = "emails/invitation.html"
