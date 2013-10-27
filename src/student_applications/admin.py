from django.contrib import admin
from student_applications import models

admin.site.register(models.Cohort)
admin.site.register(models.Tag)
