from django.contrib import messages
from events.models import Event
from surveys.models import Survey
from users.models import HackitaUser
from django.utils.translation import ugettext_lazy as _


class UsersOperationsMixin(object):
    def get_context_data(self, **kwargs):
        d = super(UsersOperationsMixin, self).get_context_data(**kwargs)
        d['surveys'] = Survey.objects.all()
        d['events'] = Event.objects.filter(is_active=True)
        return d

    def get_base_url(self):
        return self.request.build_absolute_uri('/')[:-1]

    def get_user_ids(self):
        return [int(x) for x in self.request.POST.getlist('users')]

    def send_survey(self, request):
        survey = Survey.objects.get(pk=int(request.POST['survey']))
        for uid in self.get_user_ids():
            user = HackitaUser.objects.get(pk=uid)
            o, created = survey.add_user(user)
            if created:
                o.send(self.get_base_url())
            messages.success(request, u"%s: %s" % (user,
                                                   _("Sent") if created else _("Already sent")))
        return survey

    def send_invites(self, request):
        event = Event.objects.get(pk=int(request.POST['event']))

        for uid in self.get_user_ids():
            user = HackitaUser.objects.get(pk=uid)
            o, created = event.invite_user(user, request.user, self.get_base_url())
            messages.success(request, u"%s: %s" % (user,
                                                   _("Invited") if created else _("Already invited")))

        return event


