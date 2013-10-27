from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
import logging
import random
import string
logger = logging.getLogger(__name__)


def send_html_mail(subject, html_message, email):

    alts = [(html_message, 'text/html')]

    m = EmailMultiAlternatives(subject, to=[email], alternatives=alts)
    return m.send()


class Event(models.Model):
    title = models.CharField(_('Title'), max_length=400)
    slug = models.SlugField()
    is_active = models.BooleanField(_("Active"), default=True)
    is_open = models.BooleanField(_("Invitations open"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name="events_created")
    starts_at = models.DateTimeField(_("Starts at"))
    ends_at = models.DateTimeField(_("Ends at"))
    location = models.CharField(_('Location'), max_length=400, null=True)
    description = models.TextField(null=True)

    def __unicode__(self):
        return self.title

    def invite_user(self, user, created_by=None, base_url=None):

        try:
            o = EventInvitation.objects.get(event=self, user=user)
            created = False
        except EventInvitation.DoesNotExist:
            o = EventInvitation.objects.create(event=self, user=user,
                                               created_by=created_by)
            o.send(base_url)
            created = True

        return o, created


class EventInvitationStatus(object):
    NEW = 1
    SENT = 2
    APPROVED = 3
    MAYBE = 4
    DECLINED = 5

    choices = (
               (NEW, _('New invitation')),
               (SENT, _('Invitation sent')),
               (APPROVED, _('Invitation approved')),
               (MAYBE, _('Invitation maybe')),
               (DECLINED, _('Invitation declined')),
               )


def random_slug(length=40):
    return "".join([random.choice(string.lowercase) for _ in range(length)])


class EventInvitation(models.Model):
    event = models.ForeignKey(Event)
    slug = models.SlugField(default=random_slug)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name="event_invitations_created",
                                   null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="invitations")
    status = models.IntegerField(choices=EventInvitationStatus.choices,
                                 default=EventInvitationStatus.NEW)
    note = models.TextField(null=True)

    statuses = EventInvitationStatus

    class Meta:
        unique_together = (
                           ('event', 'user'),
                          )

    @models.permalink
    def get_absolute_url(self):
        return "invitation", (self.slug,)

    def send(self, base_url=""):
        """ sends an email to user and updated the invitaiton status """
        assert self.status == EventInvitationStatus.NEW

        context = {'base_url': base_url, 'object': self}

        subject = "%s: %s" % (_("Invitation"), self.event.title)

        html_message = render_to_string("emails/invitation.html", context)

        logger.info("Sending invitation #%d for event #%d to user #%d at %s"
                    % (self.id, self.event.id, self.user.id, self.user.email))

        send_html_mail(subject, html_message, self.user.email)

        self.status = EventInvitationStatus.SENT
        self.save()

        return True

