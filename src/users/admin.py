from django.contrib import admin
from users.models import HackitaUser
from django.utils.translation import ugettext_lazy as _


class HackitaUserAdmin(admin.ModelAdmin):

    search_fields = (
        'first_name',
        'last_name',
        'email',
        'city',
        'hebrew_first_name',
        'hebrew_last_name',
        'english_first_name',
        'english_last_name',
    )
    list_filter = (
        'community_member',
        'program_leader',
        'is_staff',
        'is_superuser',
        'is_active',
    )
    list_display = (
        '__unicode__',
        'is_active',
        'community_member',
        'program_leader',
        'is_staff',
    )

    fieldsets = (
        (_('Personal info'), {'fields': (
            'email',
            ('first_name', 'last_name'),
            ('hebrew_first_name', 'hebrew_last_name'),
            ('english_first_name', 'english_last_name'),
        )}),
        (_('Permissions'), {'fields': (
            (
                'is_active',
                'community_member',
                'program_leader',
            ),
            (
                'is_staff',
                'is_superuser',
            )
        )}),
        (_('Profile info'), {'fields': (
            'phone',
            ('street_address', 'city'),
            'birthday',
            'blurb',
        )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    readonly_fields = (
                        'username',
                        'email',
                        'last_login',
                        'date_joined'
                        )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(HackitaUser, HackitaUserAdmin)
