from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
import markdown


class MarkdownContent(object):
    """
    Assumes two fields, content (markdown) and content_html (compiled to
    html
    """
    def save(self, *args, **kwargs):
        self.content_html = markdown.markdown(self.content, safe_mode='escape',
                                                extensions=['codehilite'])
        return super(MarkdownContent, self).save(*args, **kwargs)


class Trail(MarkdownContent, models.Model):
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
#                                    related_name="trails")
    ordinal = models.IntegerField(default=0)
    title = models.CharField(max_length=300)
    slug = models.CharField(max_length=300)
    content = models.TextField(null=True, blank=True)
    content_html = models.TextField(null=True, blank=True)
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

    def user_items(self, user):

        qs = self.items.all()
        if not user.is_staff:
            qs = qs.filter(is_published=True)

        def get_user_item(item):
            if not user.id:
                return None
            try:
                return item.users.get(user=user)
            except UserItem.DoesNotExist:
                return None

        return [(x, get_user_item(x)) for x in qs]


class Language(object):
    TEXT = 0
    PYTHON = 100
    JAVASCRIPT = 101

    choices = (
               (TEXT, 'Text'),
               (PYTHON, 'Python'),
               (JAVASCRIPT, 'Javasript'),
               )

    lexers = {
               PYTHON: 'python',
               JAVASCRIPT: 'javasript',
             }

    @classmethod
    def highlight(cls, lang, code):
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import HtmlFormatter

        lexer = get_lexer_by_name(cls.lexers[lang], stripall=True)
        formatter = HtmlFormatter(linenos=True, cssclass="codehilite")
        return highlight(code, lexer, formatter)


class Item(MarkdownContent, models.Model):
    trail = models.ForeignKey(Trail, related_name="items")
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
#                                    related_name="lms_items")
    ordinal = models.IntegerField(default=0)
    title = models.CharField(max_length=300)
    content = models.TextField(null=True, blank=True)
    content_html = models.TextField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    is_exercise = models.BooleanField(default=False)
    language = models.IntegerField(choices=Language.choices,
                                   default=Language.TEXT)
    languages = Language
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('ordinal',)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return "lms_item", (self.pk,)

    def users_solved(self):
        return self.solutions.distinct('author').count()


class UserItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, related_name='users')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    liked = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)
    checked_at = models.DateTimeField(null=True, blank=True)
    is_mentor = models.BooleanField(default=False)


class ItemComment(MarkdownContent, models.Model):
    item = models.ForeignKey(Item, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    content_html = models.TextField()


class SolutionPrivacy(object):
    PRIVATE = 1
    FRIENDS = 10
    COMMUNITY = 50
    PUBLIC = 100

    choices = (
               (PRIVATE, _("Personal (only me and the instructors)")),
               (COMMUNITY, _("Community members")),
               (PUBLIC, _("World visible")),
               )


class Solution(models.Model):
    item = models.ForeignKey(Item, related_name="solutions")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="solutions")
    created_at = models.DateTimeField(auto_now_add=True)
    privacy = models.IntegerField(choices=SolutionPrivacy.choices,
                                  default=SolutionPrivacy.PUBLIC)
    language = models.IntegerField(choices=Language.choices,
                                   default=Language.TEXT)
    languages = Language
    content = models.TextField()
    content_html = models.TextField()
