from django.conf.urls import patterns, url
from lms import views

urlpatterns = patterns('',
    url(r'^$', views.TrailListView.as_view(), name='trails'),
    url(r'^(?P<slug>[-_\w\d]+)/$', views.TrailDetailView.as_view(),
        name='trail'),
    url(r'^item/(?P<pk>\d+)/$', views.LMSItemDetailView.as_view(),
        name='lms_item'),

)
