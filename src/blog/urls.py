from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
    url(r'^$', views.BlogPostListView.as_view(), name='blogs'),
    url(r'^(?P<slug>[-_\w\d]+)/$', views.BlogPostDetailView.as_view(), name='blog'),

)
