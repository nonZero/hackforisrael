from django.views.generic import TemplateView

from blog.models import AllPosts


class BlogPostListView(TemplateView):
    template_name = 'blog/post_list.html'

    #TODO paging to show only 5 posts in each page, starting from most recent
    def get_context_data(self, **kwargs):
        context = super(BlogPostListView, self).get_context_data(**kwargs)
        context['posts'] = AllPosts()
        return context


class BlogPostDetailView(TemplateView):
    template_name = 'blog/post_detail.html'

    def get_context_data(self, slug, **kwargs):
        context = super(BlogPostDetailView, self).get_context_data(**kwargs)
        context['post'] = AllPosts()[slug]
        return context
