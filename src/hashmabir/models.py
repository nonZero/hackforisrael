from django.db import models
from django.utils.translation import ugettext_lazy as _
from h4il.html import HTMLField
from users.models import HackitaUser


class Hashmabir(models.Model):

    created_by = models.ForeignKey(HackitaUser)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(_('Title'), max_length=255, null=False)
    content = HTMLField(_('Content'), null=False)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ("hashmabir_detail", str(self.id))
