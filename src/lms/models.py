from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe
import markdown


class Trail(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name="trails")
    ordinal = models.IntegerField(default=0)
    title = models.CharField(max_length=300)
    slug = models.CharField(max_length=300)
    content = models.TextField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('ordinal',)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return "trail", (self.slug,)

    def md(self):
        return mark_safe(markdown.markdown(self.content))


class Item(models.Model):
    trail = models.ForeignKey(Trail, related_name="items")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name="lms_items")
    ordinal = models.IntegerField(default=0)
    title = models.CharField(max_length=300)
    content = models.TextField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    is_exercise = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('ordinal',)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return "lms_item", (self.pk,)

    def md(self):
        return mark_safe(markdown.markdown(self.content))


class UserItem(models.Model):
    item = models.ForeignKey(Item)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    liked = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)


class ItemComment(models.Model):
    item = models.ForeignKey(Item, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()


class Solution(models.Model):
    item = models.ForeignKey(Item, related_name="solutions")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="solutions")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
