from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone
import random
import string


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


class HackitaUser(AbstractUser):

    objects = HackitaUserManager()

    def __unicode__(self):
        return self.email
