from django.contrib import admin
from surveys import models

admin.site.register(models.Survey)
admin.site.register(models.SurveyAnswer)
