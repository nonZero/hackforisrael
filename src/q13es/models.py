from django.conf import settings
from django.db import models
from django_extensions.db.fields.json import JSONField
from q13es.forms import get_pretty_answer


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='answers')
    q13e_slug = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    data = JSONField()

    class Meta:
        unique_together = (('user', 'q13e_slug'),)

    def __unicode__(self):
        return u"%s: %s (%s)" % (self.user, self.q13e_slug, self.created_at)

    def get_pretty(self, form):
        dct = get_pretty_answer(form, self.data)
        dct['answer'] = self
        return dct
