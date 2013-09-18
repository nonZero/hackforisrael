from django.db import models
from django.utils.translation import ugettext_lazy as _


class Hashmabir(models.Model):

    title = models.CharField(_('Title'), max_length=255, null=False)
    content_domain = models.TextField(_('Content domain'), null=False)
    vision = models.TextField(_('Vision'), null=False)
    target_audience = models.TextField(_('Target audience'), null=False)
    similar_projects = models.TextField(_('Similar projects'), null=False, blank=True)
    contact_info = models.TextField(_('Contact info'), null=False)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ("hashmabir_detail", str(self.id))
