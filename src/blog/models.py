"""This isn't a regular models file.
The blog entries are loaded from static markdown files in the repo

In the future, it may benefit us to implement the full model interface, but it may prove to much work
See: http://django-nonrel.org/
and: http://www.allbuttonspressed.com/blog/django/2010/04/Writing-a-non-relational-Django-backend
"""

from django.utils.translation import ugettext as _

import dateutil.parser
from codecs import open  # fix opening unicode files
import markdown
import os
import UserDict

from uni_meta import uni_meta  # our modified unicode metadata markdown extension

POSTS_PATH = "blog/posts"


class Post(object):
    """A pseudo-model for a blog post loaded from a single markdown file with its metadata"""
    def __init__(self, slug):
        with open('%s/%s.md' % (POSTS_PATH, slug), encoding='utf-8') as md_file:
            md = markdown.Markdown(extensions=[uni_meta, 'codehilite'])
            html = md.convert(md_file.read())

        missing_fields = {_('author'), _('date')}.difference(md.Meta)
        if missing_fields:
            raise RuntimeError("Blog post metadata is missing for '%s'. Please add: %s" % (
                                slug, ', '.join(missing_fields)))

        self.slug = slug
        self.html = html
        self.author = md.Meta[_('author')][0]
        self.created_date = dateutil.parser.parse(md.Meta[_('date')][0])


def list_posts():
    posts_dir_files = (os.path.splitext(f) for f in os.listdir(POSTS_PATH))
    return [slug for (slug, ext) in posts_dir_files if ext == ".md"]


def get_posts():
    return {slug: Post(slug) for slug in list_posts()}


class AllPosts(UserDict.IterableUserDict):
    """A singleton class to hold the posts lazily loaded from disk"""
    __posts = None

    def __init__(self, *args, **kwargs):
        UserDict.IterableUserDict.__init__(self)
        if not self.__posts:
            AllPosts.__posts = get_posts()
        self.data = AllPosts.__posts


#TODO: add preloading of the posts (instantiate AllPosts) when in production mode?
