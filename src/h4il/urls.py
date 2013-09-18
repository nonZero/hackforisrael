from django.conf.urls import patterns, include, url
from website import views
from student_applications.views import Dashboard

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.website_view('home'), name='home'),
    url(r'^faq/$', views.FAQView.as_view(), name='faq'),
    url(r'^program/$', views.website_view('program'), name='program'),
    url(r'^ideas/$', views.website_view('ideas'), name='ideas'),

    url(r'^hashmabirs/', include('hashmabir.urls')),

    # url(r'^h4il/', include('h4il.foo.urls')),

    url(r'^dash/$', Dashboard.as_view(), name='dashboard'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
