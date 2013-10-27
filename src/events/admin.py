from django.contrib import admin
from events import models


class EventInvitationAdmin(admin.ModelAdmin):
    list_display = (
                    'id',
                    'event',
                    'user',
                    'status',
                    )

admin.site.register(models.Event)
admin.site.register(models.EventInvitation, EventInvitationAdmin)