from django.conf.urls import patterns, include, url
from website import views
from student_applications import views as sa_views
from users import views as users_views
from events import views as events_views

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

    url(r'^$', views.website_view('home'), name='home'),
    url(r'^faq/$', views.FAQView.as_view(), name='faq'),
    url(r'^program/$', views.website_view('program'), name='program'),
    url(r'^ideas/$', views.website_view('ideas'), name='ideas'),

    url(r'^hashmabirs/', include('hashmabir.urls')),

    url(r'^dashboard/$', sa_views.Dashboard.as_view(), name='dashboard'),
    url(r'^register/$', sa_views.RegisterView.as_view(), name='register'),
    #url(r'^all-forms/$', sa_views.AllFormsView.as_view(), name='all_forms'),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^event/$',
        events_views.EventListView.as_view(), name='events'),

    url(r'^event/(?P<slug>[-_\w\d]+)/$',
        events_views.EventDetailView.as_view(), name='event'),

    url(r'^invitation/(?P<slug>[a-z]+)/$',
        events_views.InvitationDetailView.as_view(), name='invitation'),

    url(r'^invitation/(?P<slug>[a-z]+)/preview/$',
        events_views.InvitationPreviewView.as_view(), name='invitation_preview'),

    url(r'^invitation/(?P<slug>[a-z]+)/edit/$',
        events_views.InvitationUpdateView.as_view(), name='invitation_edit'),


    # STAFF ONLY
    url(r'^users/$', users_views.UsersListView.as_view(), name='users'),
    url(r'^users/(?P<pk>\d+)/$', users_views.UserView.as_view(),
        name='user_dashboard'),
    url(r'^users/(?P<pk>\d+)/add-note/$', users_views.CreateUserNoteView.as_view(),
        name='user_add_note'),
    url(r'^users/(?P<pk>\d+)/edit/$', sa_views.UserCohortUpdateView.as_view(),
        name='user_edit'),
    url(r'^users/log/$', users_views.AllUsersLogView.as_view(),
        name='users_log'),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^hadmin/', include(admin.site.urls)),
)
