from django.contrib import admin
from lms import models


class TrailAdmin(admin.ModelAdmin):
    list_display = (
                    'title',
                    'ordinal',
                    'is_published',
                    )
    list_filter = (
                    'is_published',
                    )
    search_fields = (
                    'title',
                    )


class ItemAdmin(admin.ModelAdmin):
    list_display = (
                    'title',
                    'trail',
                    'ordinal',
                    'is_published',
                    'is_exercise',
                    )
    list_filter = (
                    'trail',
                    'is_published',
                    'is_exercise',
                    )
    search_fields = (
                    'title',
                    )

admin.site.register(models.Trail, TrailAdmin)
admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.ItemComment)
admin.site.register(models.Solution)
