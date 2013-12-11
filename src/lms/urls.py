from django.conf.urls import patterns, url
from lms import views

urlpatterns = patterns('',

    url(r'^$', views.TrailListView.as_view(), name='trails'),

    url(r'^add-trail/$', views.AddTrailView.as_view(),
        name='trail_add'),

    url(r'^(?P<slug>[-_\w\d]+)/$', views.TrailDetailView.as_view(),
        name='trail'),

    url(r'^(?P<slug>[-_\w\d]+)/edit/$', views.EditTrailView.as_view(),
        name='trail_edit'),


    url(r'^item/add/(?P<slug>[-_\w\d]+)/$', views.LMSItemAddView.as_view(),
        name='lms_item_add'),
    url(r'^item/(?P<pk>\d+)/$', views.LMSItemDetailView.as_view(),
        name='lms_item'),
    url(r'^item/(?P<pk>\d+)/edit/$', views.LMSItemEditView.as_view(),
        name='lms_item_edit'),
    url(r'^item/(?P<item_pk>\d+)/post-solution/$',
        views.SolutionCreateView.as_view(),
        name='lms_post_solution'),

)
