from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _, gettext_noop

gettext_noop("projects")

PROJECT_SLUG_RE = r"[-\w]{3,20}"


class Project(models.Model):
    title = models.CharField(_("title"), max_length=400)
    slug = models.CharField(_("slug"), max_length=60, validators=[
        RegexValidator(PROJECT_SLUG_RE)])
    is_published = models.BooleanField(_("published"), default=False)
    main_url = models.URLField(_("main url"), null=True, blank=True)
    github_url = models.URLField(_("github url"), null=True, blank=True)
    summary = models.TextField(_("summary"), null=True, blank=True)
    description = models.TextField(_("description"), null=True, blank=True)
    launch_date = models.DateField(_("launch date"), null=True, blank=True)

    def get_absolute_url(self):
        return reverse('project:view', kwargs={'slug': self.slug})

    def get_edit_url(self):
        return reverse('project:edit', kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, related_name="members")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="projects",
                             limit_choices_to={'community_member': True})
    is_leader = models.BooleanField(default=False)
    role = models.CharField(max_length=500, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.user)

    class Meta:
        verbose_name = _('project member')
        verbose_name_plural = _('project members')
        order_with_respect_to = 'project'
