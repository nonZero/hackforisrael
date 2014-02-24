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

)

