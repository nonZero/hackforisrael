from django.contrib import admin
from surveys import models
from h4il.html import HTMLField, HTMLWidget


class SurveyAdmin(admin.ModelAdmin):
    formfield_overrides = {
       HTMLField: {'widget': HTMLWidget()},
    }

admin.site.register(models.Survey, SurveyAdmin)
admin.site.register(models.SurveyAnswer)
