from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import HackitaUser
from django.utils.translation import ugettext_lazy as _


class HackitaUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
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
