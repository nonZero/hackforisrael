from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from events.models import Event
from surveys.models import Survey
from users.models import HackitaUser
from django.utils.translation import ugettext_lazy as _


def user_test_required(test_function, login_url=None):
    """
    Decorator for views that checks whether a user is logged in and has a particular permission
    """
    def check_perms(user):

        # redirect to login only if not logged in.
        if not user.is_authenticated():
            return False

        # show 403 if user has no permissions for page
        if not test_function(user):
            raise PermissionDenied()

        return True

    return user_passes_test(check_perms, login_url=login_url)

community_member_required = user_test_required(lambda u: u.is_superuser or u.community_member)


class CommunityOnlyMixin(object):

    @method_decorator(community_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CommunityOnlyMixin, self).dispatch(request, *args, **kwargs)


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


