from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import UserProfile
from bridge.models import Minera


class BridgeFilter(admin.SimpleListFilter):
    title = _("Bridge")
    parameter_name = 'bridge'

    def lookups(self, request, model_admin):
        return [(m.id, m.name) for m in Minera.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            users_profiles = UserProfile.objects.filter(bridge__id__exact=self.value())
            users_ids = [u.user_id for u in users_profiles]
            return queryset.filter(id__in=users_ids)
        else:
            return queryset


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    verbose_name_plural = 'Datos'


class UserAdmin(BaseUserAdmin):

    def bridge(self, inst):
        return UserProfile.objects.get(user=inst).bridge

    list_filter = ['is_staff', 'is_superuser', 'is_active', BridgeFilter]
    list_display = ('username', 'email', 'is_staff', 'bridge')
    inlines = (UserProfileInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
