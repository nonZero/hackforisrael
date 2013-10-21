from django.db import models
from django.utils.translation import ugettext_lazy as _
from users.models import HackitaUser


class UserNote(models.Model):
    user = models.ForeignKey(HackitaUser, related_name="notes")
    author = models.ForeignKey(HackitaUser, related_name="notes_sent")
    visible_to_user = models.BooleanField(_("Visible to the user"), default=True)
    created_at = models.DateField(_("Creation time"), auto_now_add=True)
    content = models.TextField(_("Content"))
    read = models.BooleanField(_("Was read"), default=False)
    archived = models.BooleanField(_("Was archived"), default=False)
