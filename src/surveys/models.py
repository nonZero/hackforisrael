from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django_extensions.db.fields.json import JSONField
from h4il.base_models import random_slug
from h4il.mail import send_html_mail
from q13es.forms import get_pretty_answer, parse_form
import logging

logger = logging.getLogger(__name__)


class Survey(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    email_subject = models.CharField(max_length=250)
    email_content = models.TextField(null=True, blank=True)
    q13e = models.TextField()

    def __unicode__(self):
        return self.email_subject

    def get_form_class(self):
        return parse_form(self.q13e)

    def add_user(self, user):
        return SurveyAnswer.objects.get_or_create(survey=self, user=user)

    @models.permalink
    def get_absolute_url(self):
        return "survey", (self.pk,)


class SurveyAnswer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(default=random_slug)
    survey = models.ForeignKey(Survey, related_name='answers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='survey_answers')
    answered_at = models.DateTimeField(null=True, blank=True)
    data = JSONField(null=True, blank=True)

    class Meta:
        unique_together = (('survey', 'user'),)

    def __unicode__(self):
        return u"%s: %s (%s)" % (self.survey, self.user, self.created_at)

    def get_pretty(self):
        dct = get_pretty_answer(self.survey.get_form_class(), self.data)
        dct['answer'] = self
        return dct

    @models.permalink
    def get_absolute_url(self):
        return "survey_answer", (self.slug,)

    def send(self, base_url=""):
        """ sends an email to user  """

        context = {'base_url': base_url, 'object': self}

        html_message = render_to_string("surveys/survey_email.html", context)

        logger.info("Sending survey (#%d) for survey #%d to user #%d at %s"
                    % (self.id, self.survey.id, self.user.id, self.user.email))

        send_html_mail(self.survey.email_subject, html_message, self.user.email)

        return True
