from django.conf.urls import patterns, url
from projects import views
from projects.models import PROJECT_SLUG_RE


urlpatterns = patterns(
    '',

    url(r'^$', views.ProjectListView.as_view(), name='list'),

    url(r'^(?P<slug>{})/$'.format(PROJECT_SLUG_RE),
        views.ProjectDetailView.as_view(), name='view'),

    url(r'^(?P<slug>{})/edit/$'.format(PROJECT_SLUG_RE),
        views.ProjectUpdateView.as_view(), name='edit'),

    url(r'^(?P<slug>{})/admin/$'.format(PROJECT_SLUG_RE),
        views.ProjectAdminView.as_view(), name='admin'),

    url(r'^(?P<project>{})/create-post/$'.format(PROJECT_SLUG_RE),
        views.ProjectPostCreateView.as_view(), name='create_post'),


    url(r'^(?P<project>{})/post/(?P<pk>\d+)/$'.format(PROJECT_SLUG_RE),
        views.ProjectPostDetailView.as_view(), name='post'),

    url(r'^(?P<project>{})/post/(?P<pk>\d+)/edit/$'.format(PROJECT_SLUG_RE),
        views.ProjectPostUpdateView.as_view(), name='edit_post'),


    url(r'^(?P<project>{})/post/(?P<pk>\d+)/delete/$'.format(PROJECT_SLUG_RE),
        views.ProjectPostDeleteView.as_view(), name='delete_post'),


)

