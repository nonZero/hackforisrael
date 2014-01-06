from django.views.generic import TemplateView

from codecs import open  # fix opening unicode files
import markdown
import dateutil.parser
import os

from uni_meta import uni_meta  # our modified unicode metadata markdown extension

POSTS_PATH = "blog/posts"


#TODO actually load all the posts into memory
# I still think that abusing the Model interface to provide precached file persistence will be elegant
def list_posts():
    posts_dir_files = (os.path.splitext(f) for f in  os.listdir(POSTS_PATH))
    return [slug for (slug, ext) in posts_dir_files if ext == ".md"]


def load_post(slug):
    with open('%s/%s.md' % (POSTS_PATH, slug), encoding='utf-8') as md_file:
        md = markdown.Markdown(extensions=[uni_meta, 'codehilite'])
        html = md.convert(md_file.read())

    return md.Meta, html


class BlogPostListView(TemplateView):
    template_name = 'blog/post_list.html'

    #TODO paging to show only 5 posts in each page, starting from most recent
    def get_context_data(self, **kwargs):
        context = super(BlogPostListView, self).get_context_data(**kwargs)
        context['posts'] = list_posts()
        return context


class BlogPostDetailView(TemplateView):
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        slug = kwargs['slug']
        metadata, html = load_post(slug)

        context = super(BlogPostDetailView, self).get_context_data(**kwargs)
        context['slug'] = slug
        #TODO internationalize the metadata fields
        context['author'] = metadata['author'][0]
        context['created_date'] = dateutil.parser.parse(metadata['date'][0])
        context['html'] = html
        return context
