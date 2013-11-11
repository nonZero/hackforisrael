from django.conf.urls import patterns, url
from surveys import views

urlpatterns = patterns('',
    url(r'^$', views.SurveyListView.as_view(), name='survies'),
    url(r'^(?P<pk>[\d]+)/$', views.SurveyDetailView.as_view(),
        name='survey'),
    url(r'^(?P<slug>[a-z]+)/$', views.SurveyAnswerView.as_view(),
        name='survey_answer'),

)
