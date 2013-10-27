from django.conf import settings
from django.db import models, transaction
from django.db.utils import IntegrityError
from django.utils.translation import ugettext_lazy as _
from users.models import UserLogOperation, UserLog


class Cohort(models.Model):
    ordinal = models.IntegerField(unique=True)
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['ordinal']


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


class TagGroup(object):

    NEGATIVE = -100
    NEUTRAL = 0
    BRONZE = 100
    SILVER = 200
    GOLD = 300

    choices = (
               (NEGATIVE, 'negative'),
               (NEUTRAL, 'neutral'),
               (BRONZE, 'bronze'),
               (SILVER, 'silver'),
               (GOLD, 'gold'),
              )


class Tag(models.Model):
    name = models.CharField(max_length=100)
    group = models.IntegerField(choices=TagGroup.choices,
                                default=TagGroup.NEUTRAL)

    class Meta:
        ordering = ['-group', 'name']

    def __unicode__(self):
        return self.name


class UserTagManager(models.Manager):

    def tag(self, user, tag, by):
        with transaction.commit_on_success():
            o, created = self.get_or_create(user=user, tag=tag, created_by=by)
            if created:
                UserLog.objects.create(user=user, created_by=by,
                                       content_object=tag,
                                       operation=UserLogOperation.ADD)
        return o

    def untag(self, user, tag, by):
        with transaction.commit_on_success():
            try:
                o = self.get(user=user, tag=tag, created_by=by)
                o.delete()
                UserLog.objects.create(user=user, created_by=by,
                                       content_object=tag,
                                       operation=UserLogOperation.REMOVE)
                return True
            except UserTag.DoesNotExist:
                return False


class UserTag(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="tags")
    tag = models.ForeignKey(Tag, related_name='users')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name="tags_created")

    objects = UserTagManager()

    class Meta:
        unique_together = (
                           ('user', 'tag', 'created_by'),
                          )

