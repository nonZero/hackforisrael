from django.conf.urls import patterns,  url
import views

urlpatterns = patterns('',
    url(r'^$', views.HashmabirListView.as_view(), name='hashmabir_list'),
    url(r'^add/$', views.HashmabirCreateView.as_view(), name='hashmabir_create'),
    url(r'^(?P<pk>\d+)/$', views.HashmabirDetailView.as_view(), name='hashmabir_detail'),
)
