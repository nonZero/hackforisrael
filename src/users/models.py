from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _
import random
import string
import student_applications.models


def random_username():
    return "".join([random.choice(string.lowercase) for _ in range(20)])


class HackitaUserManager(UserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """

        if self.filter(email__iexact=email).exists():
            raise Exception("User already exists")

        now = timezone.now()
        username = random_username()
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user


class Gender(object):
    MALE = 1
    FEMALE = 2
    choices = (
               (MALE, _('Male')),
               (FEMALE, _('Female')),
              )


class HackitaUser(AbstractUser):

    gender = models.IntegerField(choices=Gender.choices, null=True)

    hebrew_first_name = models.CharField(_('Hebrew first name'), max_length=50,
                                         null=True, blank=True)
    hebrew_last_name = models.CharField(_('Hebrew last name'), max_length=50,
                                        null=True, blank=True)

    english_first_name = models.CharField(_('English first name'),
                                          max_length=50, null=True, blank=True)
    english_last_name = models.CharField(_('English last name'), max_length=50,
                                         null=True, blank=True)

    # denormalize for queries
    forms_filled = models.IntegerField(default=0, db_index=True)
    last_form_filled = models.DateTimeField(null=True, blank=True,
                                            db_index=True)

    objects = HackitaUserManager()

    def __unicode__(self):
        if self.hebrew_first_name and self.hebrew_last_name:
            return u"%s %s" % (self.hebrew_first_name, self.hebrew_last_name)
        return self.email

    def all_cohorts(self):
        all_cohorts = student_applications.models.Cohort.objects.order_by(
                                              'ordinal').values_list('ordinal',
                                                                     flat=True)
        cohorts = SortedDict([(k, None) for k in all_cohorts])
        for o in self.cohorts.all():
            cohorts[o.cohort.ordinal] = o

        return cohorts


def update_personal_details(user, data):
    if data['gender'] == _('Male'):
        user.gender = Gender.MALE
    elif data['gender'] == _('Female'):
        user.gender = Gender.FEMALE
    for k in [
        'hebrew_first_name',
        'hebrew_last_name',
        'english_first_name',
        'english_last_name']:
        setattr(user, k, data[k][:50])


