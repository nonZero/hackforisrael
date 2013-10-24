from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Cohort(models.Model):
    ordinal = models.IntegerField(unique=True)
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)


class UserCohortStatus(object):
    INVITED = 1

    UNAVAILABLE = 2

    AVAILABLE = 10

    INVITED_TO_INTERVIEW = 50

    REJECTED = 99
    ACCEPTED = 100

    REGISTERED = 110
    IN_PROCESS = 200
    GRADUATED = 300

    choices = (
                    (INVITED, _('Invited')),
                    (UNAVAILABLE, _('Unavailable')),
                    (AVAILABLE, _('Available')),
                    (INVITED_TO_INTERVIEW, _('Invited to interview')),
                    (REJECTED, _('Rejected')),
                    (ACCEPTED, _('Accepted')),
                    (REGISTERED, _('Registered')),
                    (IN_PROCESS, _('In process')),
                    (GRADUATED, _('Graduated')),
               )

    IGNORED = [INVITED, UNAVAILABLE, REJECTED]


class UserCohort(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="cohorts")
    cohort = models.ForeignKey(Cohort, related_name="users")
    status = models.IntegerField(choices=UserCohortStatus.choices)

    class Meta:
        unique_together = (
                           ('user', 'cohort'),
                          )

