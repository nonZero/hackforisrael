from django.db import models
from django.utils.translation import ugettext_lazy as _

class Hashmabir(models.Model):

    title = models.CharField(_('Title'),max_length=255,null=False)
    description = models.TextField(_('Description'),null=False)
    contact_info = models.TextField(_('Contact info'),null=False)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ("hashmabir_detail", str(self.id))
